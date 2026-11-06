
import csv
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict

# ==========================================
# EV PUBLIC CHARGING SESSION BILLING ENGINE
# Team E008 | Problem ECE-025
# ==========================================

TARIFFS = {
    "AC_7KW": Decimal("12"),
    "DC_30KW": Decimal("18"),
    "DC_60KW": Decimal("22")
}

GST_RATE = Decimal("0.18")
TIME_RATE = Decimal("1")
IDLE_RATE = Decimal("2")
IDLE_LIMIT = Decimal("300")
MINIMUM_CHARGE = Decimal("20")
MINIMUM_WALLET = Decimal("100")


def money(value):
    return Decimal(str(value)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def read_csv(filename):
    with open(filename, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def write_csv(filename, headers, rows):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def parse_time(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


# ==========================================
# INVOICE CALCULATION
# ==========================================

def calculate_invoice(session, charger, user):

    kwh = Decimal(session["kwh_delivered"])
    charger_type = charger["charger_type"]
    tier = user["tier"].upper()

    # Free faulted session below 0.5 kWh
    if (
        session["fault_flag"].strip().lower() == "true"
        and kwh < Decimal("0.5")
    ):
        return {
            "status": "FREE_FAULT",
            "reason": "NONE",
            "energy_rs": money(0),
            "time_rs": money(0),
            "idle_rs": money(0),
            "discount_rs": money(0),
            "gst_rs": money(0),
            "total_rs": money(0)
        }

    # Energy charge
    energy = money(kwh * TARIFFS[charger_type])

    plug_in = parse_time(session["plug_in_time"])
    complete = parse_time(session["charge_complete_time"])
    unplug = parse_time(session["unplug_time"])

    connected_minutes = int(
        (complete - plug_in).total_seconds() // 60
    )

    idle_minutes = int(
        (unplug - complete).total_seconds() // 60
    )

    # Time charge for DC chargers only
    time_charge = Decimal("0")

    if charger_type in ("DC_30KW", "DC_60KW"):
        extra_minutes = max(0, connected_minutes - 60)
        time_charge = money(extra_minutes * TIME_RATE)

    # Idle charge: first 10 minutes free
    billable_idle = max(0, idle_minutes - 10)

    idle_charge = min(
        money(billable_idle * IDLE_RATE),
        IDLE_LIMIT
    )

    # Membership discount on energy only
    discount_rate = {
        "SILVER": Decimal("0.05"),
        "GOLD": Decimal("0.10")
    }.get(tier, Decimal("0"))

    discount = money(energy * discount_rate)

    # GST after discount
    taxable = energy + time_charge + idle_charge - discount
    gst = money(taxable * GST_RATE)

    # Minimum invoice amount
    total = money(max(MINIMUM_CHARGE, taxable + gst))

    return {
        "status": "CHARGED",
        "reason": "NONE",
        "energy_rs": energy,
        "time_rs": time_charge,
        "idle_rs": idle_charge,
        "discount_rs": discount,
        "gst_rs": gst,
        "total_rs": total
    }


# ==========================================
# EVENT PROCESSING
# ==========================================

def process_events(chargers, users, sessions, topups):

    charger_map = {c["charger_id"]: c for c in chargers}
    user_map = {u["user_id"]: u for u in users}

    balances = {
        u["user_id"]: money(u["opening_balance_rs"])
        for u in users
    }

    blocked = set()
    ledger = []
    invoices = {}

    revenue = defaultdict(
        lambda: {
            "sessions": 0,
            "kwh": Decimal("0"),
            "revenue": Decimal("0")
        }
    )

    # Opening wallet entries
    all_times = (
        [parse_time(s["plug_in_time"]) for s in sessions]
        + [parse_time(s["unplug_time"]) for s in sessions]
        + [parse_time(t["timestamp"]) for t in topups]
    )

    opening_time = min(all_times)

    for user in users:
        uid = user["user_id"]

        ledger.append({
            "user_id": uid,
            "timestamp": opening_time.strftime("%Y-%m-%d %H:%M:%S"),
            "entry_type": "OPENING",
            "reference_id": "",
            "amount_rs": f'{balances[uid]:.2f}',
            "balance_rs": f'{balances[uid]:.2f}'
        })

    # Event priorities:
    # 0 = Top-up
    # 1 = Session end
    # 2 = Session start

    events = []

    for topup in topups:
        events.append((
            parse_time(topup["timestamp"]),
            0,
            topup["topup_id"],
            "TOPUP",
            topup
        ))

    for session in sessions:
        events.append((
            parse_time(session["unplug_time"]),
            1,
            session["session_id"],
            "END",
            session
        ))

        events.append((
            parse_time(session["plug_in_time"]),
            2,
            session["session_id"],
            "START",
            session
        ))

    events.sort(key=lambda e: (e[0], e[1], e[2]))

    accepted = set()
    refused = {}

    for event_time, priority, event_id, event_type, item in events:

        # ----------------------------------
        # TOP-UP EVENT
        # ----------------------------------

        if event_type == "TOPUP":

            uid = item["user_id"]
            amount = money(item["amount_rs"])

            if amount < Decimal("100"):
                ledger.append({
                    "user_id": uid,
                    "timestamp": item["timestamp"],
                    "entry_type": "TOPUP_REJECTED",
                    "reference_id": item["topup_id"],
                    "amount_rs": "0.00",
                    "balance_rs": f'{balances[uid]:.2f}'
                })
                continue

            balances[uid] += amount

            ledger.append({
                "user_id": uid,
                "timestamp": item["timestamp"],
                "entry_type": "TOPUP",
                "reference_id": item["topup_id"],
                "amount_rs": f'{amount:.2f}',
                "balance_rs": f'{balances[uid]:.2f}'
            })

            # 3% bonus for top-ups >= Rs.1000
            if amount >= Decimal("1000"):

                bonus = money(amount * Decimal("0.03"))
                balances[uid] += bonus

                ledger.append({
                    "user_id": uid,
                    "timestamp": item["timestamp"],
                    "entry_type": "TOPUP_BONUS",
                    "reference_id": item["topup_id"],
                    "amount_rs": f'{bonus:.2f}',
                    "balance_rs": f'{balances[uid]:.2f}'
                })

            if balances[uid] >= 0:
                blocked.discard(uid)

        # ----------------------------------
        # SESSION START EVENT
        # ----------------------------------

        elif event_type == "START":

            uid = item["user_id"]
            sid = item["session_id"]

            if uid in blocked:
                refused[sid] = "BLOCKED"

            elif balances[uid] < MINIMUM_WALLET:
                refused[sid] = "LOW_BALANCE"

            else:
                accepted.add(sid)

        # ----------------------------------
        # SESSION END EVENT
        # ----------------------------------

        elif event_type == "END":

            uid = item["user_id"]
            sid = item["session_id"]

            if sid in refused:

                invoice = {
                    "status": "REFUSED",
                    "reason": refused[sid],
                    "energy_rs": money(0),
                    "time_rs": money(0),
                    "idle_rs": money(0),
                    "discount_rs": money(0),
                    "gst_rs": money(0),
                    "total_rs": money(0)
                }

            elif sid in accepted:

                charger = charger_map[item["charger_id"]]
                user = user_map[uid]

                invoice = calculate_invoice(item, charger, user)

                total = invoice["total_rs"]

                # Debit wallet only for a charged invoice
                if invoice["status"] == "CHARGED":
                    balances[uid] -= total

                    ledger.append({
                        "user_id": uid,
                        "timestamp": item["unplug_time"],
                        "entry_type": "SESSION",
                        "reference_id": sid,
                        "amount_rs": f'{-total:.2f}',
                        "balance_rs": f'{balances[uid]:.2f}'
                    })

                    if balances[uid] < 0:
                        blocked.add(uid)

                # Revenue belongs to the unplug date
                date = item["unplug_time"][:10]
                key = (date, item["charger_id"])

                revenue[key]["sessions"] += 1
                revenue[key]["kwh"] += Decimal(item["kwh_delivered"])
                revenue[key]["revenue"] += total

            else:
                continue

            invoices[sid] = invoice

    return balances, blocked, ledger, invoices, revenue


# ==========================================
# OUTPUT FILE GENERATION
# ==========================================

def generate_outputs(
    chargers, users, sessions,
    balances, blocked, ledger, invoices,
    revenue, report_dates
):

    # Invoices in sessions.csv order
    invoice_rows = []

    for session in sessions:
        sid = session["session_id"]
        invoice = invoices[sid]

        invoice_rows.append({
            "session_id": sid,
            "user_id": session["user_id"],
            "charger_id": session["charger_id"],
            "status": invoice["status"],
            "reason": invoice["reason"],
            "kwh_delivered": session["kwh_delivered"],
            "energy_rs": f'{invoice["energy_rs"]:.2f}',
            "time_rs": f'{invoice["time_rs"]:.2f}',
            "idle_rs": f'{invoice["idle_rs"]:.2f}',
            "discount_rs": f'{invoice["discount_rs"]:.2f}',
            "gst_rs": f'{invoice["gst_rs"]:.2f}',
            "total_rs": f'{invoice["total_rs"]:.2f}'
        })

    write_csv(
        "invoices.csv",
        [
            "session_id", "user_id", "charger_id", "status", "reason",
            "kwh_delivered", "energy_rs", "time_rs", "idle_rs",
            "discount_rs", "gst_rs", "total_rs"
        ],
        invoice_rows
    )

    write_csv(
        "wallet_ledger.csv",
        [
            "user_id", "timestamp", "entry_type",
            "reference_id", "amount_rs", "balance_rs"
        ],
        ledger
    )

    # One row per charger for every requested report date
    daily_rows = []

    for date in sorted(set(report_dates)):
        for charger in sorted(chargers, key=lambda c: c["charger_id"]):

            key = (date, charger["charger_id"])
            data = revenue[key]

            daily_rows.append({
                "date": date,
                "charger_id": charger["charger_id"],
                "charger_type": charger["charger_type"],
                "sessions": data["sessions"],
                "kwh": f'{data["kwh"]:.2f}',
                "revenue_rs": f'{data["revenue"]:.2f}'
            })

    write_csv(
        "daily_revenue.csv",
        [
            "date", "charger_id", "charger_type",
            "sessions", "kwh", "revenue_rs"
        ],
        daily_rows
    )

    blocked_rows = []

    for uid in sorted(blocked):
        blocked_rows.append({
            "user_id": uid,
            "balance_rs": f'{balances[uid]:.2f}'
        })

    write_csv(
        "blocked_users.csv",
        ["user_id", "balance_rs"],
        blocked_rows
    )

    print("\nPROCESSING COMPLETED SUCCESSFULLY!")
    print("Invoices generated:", len(invoice_rows))
    print("Wallet ledger entries:", len(ledger))
    print("Daily revenue rows:", len(daily_rows))
    print("Blocked users:", len(blocked_rows))

    print("\nOutput files created:")
    print("1. invoices.csv")
    print("2. wallet_ledger.csv")
    print("3. daily_revenue.csv")
    print("4. blocked_users.csv")


# ==========================================
# COMMAND FILE PROCESSING
# ==========================================

def main():

    chargers = None
    users = None
    sessions = None
    topups = None

    processed = False
    report_dates = []
    blocked_report_requested = False

    print("EV PUBLIC CHARGING SESSION BILLING ENGINE")
    print("Team E008 | Problem ECE-025")
    print("------------------------------------------")

    try:
        with open("commands.txt", "r", encoding="utf-8-sig") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = [part.strip() for part in line.split("|")]
                command = parts[0]

                print("\nCommand:", line)

                if command == "LOAD_CHARGERS":
                    chargers = read_csv(parts[1])
                    print("Chargers loaded:", len(chargers))

                elif command == "LOAD_USERS":
                    users = read_csv(parts[1])
                    print("Users loaded:", len(users))

                elif command == "LOAD_SESSIONS":
                    sessions = read_csv(parts[1])
                    print("Sessions loaded:", len(sessions))

                elif command == "LOAD_TOPUPS":
                    topups = read_csv(parts[1])
                    print("Top-ups loaded:", len(topups))

                elif command == "PROCESS_EVENTS":

                    if None in (chargers, users, sessions, topups):
                        raise ValueError(
                            "Load all four CSV files before PROCESS_EVENTS."
                        )

                    if processed:
                        raise ValueError("PROCESS_EVENTS was called more than once.")

                    (
                        balances,
                        blocked,
                        ledger,
                        invoices,
                        revenue
                    ) = process_events(
                        chargers, users, sessions, topups
                    )

                    processed = True
                    print("All events processed.")

                elif command == "DAILY_REPORT":

                    if len(parts) != 2:
                        raise ValueError(
                            "DAILY_REPORT requires a date."
                        )

                    report_dates.append(parts[1])
                    print("Daily report requested for:", parts[1])

                elif command == "BLOCKED_USERS":
                    blocked_report_requested = True
                    print("Blocked users report requested.")

                else:
                    raise ValueError(
                        f"Unknown command on line {line_number}: {command}"
                    )

        if not processed:
            raise ValueError("PROCESS_EVENTS command is missing.")

        if not blocked_report_requested:
            print("Warning: BLOCKED_USERS command was not found.")

        generate_outputs(
            chargers, users, sessions,
            balances, blocked, ledger, invoices,
            revenue, report_dates
        )

    except FileNotFoundError as error:
        print("\nERROR: File not found:", error.filename)

    except Exception as error:
        print("\nERROR:", error)


if __name__ == "__main__":
    main()
