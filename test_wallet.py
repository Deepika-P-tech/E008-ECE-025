
import unittest
from billing import process_events


class WalletTests(unittest.TestCase):

    def setUp(self):
        self.chargers = [
            {
                "charger_id": "CH001",
                "charger_type": "AC_7KW",
                "location": "Test",
                "city": "Bengaluru"
            }
        ]

        self.users = [
            {
                "user_id": "USR001",
                "user_name": "Test User",
                "mobile": "0000000000",
                "tier": "SILVER",
                "opening_balance_rs": "100.00"
            }
        ]

    def make_session(self, sid, start, end, kwh="10"):
        return {
            "session_id": sid,
            "user_id": "USR001",
            "charger_id": "CH001",
            "plug_in_time": f"2026-11-01 {start}:00",
            "charge_complete_time": f"2026-11-01 {end}:00",
            "unplug_time": f"2026-11-01 {end}:30",
            "kwh_delivered": kwh,
            "fault_flag": "false"
        }

    def test_wallet_exactly_100_can_start(self):
        sessions = [
            self.make_session("SES001", "10:00", "10:20", "1")
        ]

        balances, blocked, ledger, invoices, revenue = process_events(
            self.chargers, self.users, sessions, []
        )

        self.assertEqual(invoices["SES001"]["status"], "CHARGED")

    def test_wallet_below_100_is_refused(self):
        users = [dict(self.users[0], opening_balance_rs="99.99")]
        sessions = [
            self.make_session("SES002", "10:00", "10:20", "1")
        ]

        balances, blocked, ledger, invoices, revenue = process_events(
            self.chargers, users, sessions, []
        )

        self.assertEqual(invoices["SES002"]["reason"], "LOW_BALANCE")

    def test_topup_below_100_is_rejected(self):
        topups = [{
            "topup_id": "TOP001",
            "user_id": "USR001",
            "timestamp": "2026-11-01 09:00:00",
            "amount_rs": "50"
        }]

        balances, blocked, ledger, invoices, revenue = process_events(
            self.chargers, self.users, [], topups
        )

        self.assertEqual(balances["USR001"], 100)
        self.assertTrue(
            any(row["entry_type"] == "TOPUP_REJECTED" for row in ledger)
        )

    def test_topup_1000_adds_3_percent_bonus(self):
        topups = [{
            "topup_id": "TOP002",
            "user_id": "USR001",
            "timestamp": "2026-11-01 09:00:00",
            "amount_rs": "1000"
        }]

        balances, blocked, ledger, invoices, revenue = process_events(
            self.chargers, self.users, [], topups
        )

        self.assertEqual(balances["USR001"], 1130)

    def test_overdraft_blocks_user(self):
        sessions = [
            self.make_session("SES003", "10:00", "10:20", "10")
        ]

        balances, blocked, ledger, invoices, revenue = process_events(
            self.chargers, self.users, sessions, []
        )

        self.assertLess(balances["USR001"], 0)
        self.assertIn("USR001", blocked)

    def test_blocked_user_is_refused(self):
        sessions = [
            self.make_session("SES004", "10:00", "10:20", "10"),
            self.make_session("SES005", "11:00", "11:20", "1")
        ]

        balances, blocked, ledger, invoices, revenue = process_events(
            self.chargers, self.users, sessions, []
        )

        self.assertEqual(invoices["SES005"]["reason"], "BLOCKED")

    def test_topup_clears_block(self):
        sessions = [
            self.make_session("SES006", "10:00", "10:20", "10"),
            self.make_session("SES007", "11:00", "11:20", "1"),
            self.make_session("SES008", "13:00", "13:20", "1")
        ]

        topups = [{
            "topup_id": "TOP003",
            "user_id": "USR001",
            "timestamp": "2026-11-01 12:00:00",
            "amount_rs": "2000"
        }]

        balances, blocked, ledger, invoices, revenue = process_events(
            self.chargers, self.users, sessions, topups
        )

        self.assertEqual(invoices["SES007"]["reason"], "BLOCKED")
        self.assertEqual(invoices["SES008"]["status"], "CHARGED")
        self.assertNotIn("USR001", blocked)


if __name__ == "__main__":
    unittest.main()
