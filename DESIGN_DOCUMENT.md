# EV Public Charging Session Billing and Wallet Engine

## Project Information

| Field | Details |
|---|---|
| Team ID | E008 |
| Problem ID | ECE-025 |
| Project Title | EV Public Charging Session Billing and Wallet Engine |
| Team Members | Deekshith S and Deepika P |
| Section | ECM A |
| Programming Language | Python 3.10+ |
| Testing Framework | Python unittest |

---

## 1. Problem Statement

Electric vehicle public charging stations require a reliable system to calculate charging costs, manage customer wallet balances, process payments and maintain transaction records.

Different charger types have different energy rates. Additional charges may apply for charging duration and idle time. Membership discounts, GST, wallet top-ups and blocked-user conditions must also be handled correctly.

The objective of this project is to develop a Python-based backend billing and wallet engine that processes charging session events, calculates invoices, manages wallet transactions and generates revenue reports.

## 2. Project Overview

The EV Public Charging Session Billing and Wallet Engine is a backend system developed using Python.

It processes charger details, user information, charging sessions and wallet top-ups from CSV files. It calculates the final invoice for each charging session according to predefined business rules.

The system also maintains wallet balances, records every wallet transaction, identifies blocked users and generates daily revenue reports for individual chargers.

The application is command-driven and does not require a graphical user interface.

## 3. Project Objectives

The main objectives are:

1. Register and manage EV charging stations.
2. Store user information and membership details.
3. Read charging session records from CSV files.
4. Calculate energy, time and idle charges.
5. Apply membership discounts and GST.
6. Generate invoices for charging sessions.
7. Manage wallet balances and top-ups.
8. Apply bonus amounts for eligible top-ups.
9. Identify and manage blocked users.
10. Maintain a wallet transaction ledger.
11. Generate daily revenue reports for each charger.
12. Validate the system using automated test cases.

## 4. Scope and System Boundaries

### Included in the Project

- Charger registration and charger information management.
- User registration and membership information.
- CSV-based input processing.
- Charging session billing.
- Energy, time and idle charge calculations.
- Membership discounts and GST.
- Wallet balance management.
- Wallet top-ups and bonus calculations.
- Blocked-user management.
- Invoice and ledger generation.
- Daily revenue reporting.
- Automated testing.

### Outside the Project Scope

- Graphical user interface.
- Online payment gateway integration.
- Real-time communication with physical EV chargers.
- Mobile application development.
- Live sensor-based charger monitoring.

The project focuses on backend billing and wallet processing.

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Main programming language |
| CSV | Input and output data storage |
| Python datetime | Timestamp and time calculations |
| Python unittest | Automated testing |
| VS Code | Development environment |
| Git and GitHub | Version control and project repository |

## 6. System Architecture and Workflow

The system follows a modular backend architecture.

### System Workflow

```text
       Input CSV Files
              |
              v
       Command Processor
              |
              v
        Data Loading
              |
              v
        Event Processor
              |
              v
       Session Validation
              |
              v
       Billing Calculator
              |
              v
       Wallet Management
              |
              v
       Wallet Ledger
              |
              v
       Output Generation
              |
       +------+------+
       |      |      |
       v      v      v
    Invoices Ledger Reports
              |
              v
       Blocked Users List
```

### Workflow Explanation

1. Charger, user, session and top-up details are loaded from CSV files.
2. The command processor reads the commands from `commands.txt`.
3. Events are arranged and processed according to timestamp and event priority.
4. The system validates user wallet balance and blocked status.
5. The billing module calculates the session charges.
6. The wallet module updates the user's balance.
7. Every wallet transaction is recorded in the ledger.
8. The system generates invoices, daily revenue reports and blocked-user reports.

## 7. System Modules

| Module | Description |
|---|---|
| Charger Management | Loads and stores charger details. |
| User Management | Loads user information, membership tiers and opening balances. |
| Session Management | Reads and processes charging session details. |
| Event Processing | Processes top-ups and session events in the required order. |
| Billing Module | Calculates energy, time, idle, discount, GST and final invoice amounts. |
| Wallet Management | Manages wallet balances, payments and top-ups. |
| Ledger Management | Maintains a record of wallet transactions. |
| Report Generation | Generates invoices, daily revenue and blocked-user reports. |
| Testing Module | Validates billing and wallet business rules. |

## 8. Glossary

| Term | Meaning |
|---|---|
| AC | Alternating Current |
| DC | Direct Current |
| kWh | Kilowatt-hour, a unit of electrical energy |
| GST | Goods and Services Tax |
| Invoice | Final bill for a charging session |
| Wallet | User's available money balance |
| Ledger | Record of wallet transactions |
| Idle Time | Time between charging completion and unplugging |
| Top-up | Money added to a user's wallet |
| Membership Tier | User category such as BASIC, SILVER or GOLD |
| Blocked User | User who cannot start a new session because of a negative wallet balance |

## 9. Conceptual Class Diagram

The following diagram represents the main entities and their relationships.

```text
+------------------+
|      Charger     |
+------------------+
| charger_id       |
| charger_type     |
| location         |
| city             |
+------------------+
         |
         | 1 to many
         |
+------------------+
| ChargingSession  |
+------------------+
| session_id       |
| user_id          |
| charger_id       |
| plug_in_time     |
| complete_time    |
| unplug_time      |
| kwh_delivered    |
| fault_flag       |
+------------------+
         |
         | creates
         |
+------------------+
|     Invoice      |
+------------------+
| energy_rs        |
| time_rs          |
| idle_rs          |
| discount_rs      |
| gst_rs           |
| total_rs         |
+------------------+

+------------------+
|       User       |
+------------------+
| user_id          |
| user_name        |
| mobile           |
| tier             |
| wallet_balance   |
| status           |
+------------------+
         |
         | has
         |
+------------------+
|   WalletLedger   |
+------------------+
| timestamp        |
| entry_type       |
| reference_id     |
| amount_rs        |
| balance_rs       |
+------------------+

         User
          |
          | makes
          v
+------------------+
|      TopUp       |
+------------------+
| topup_id         |
| user_id          |
| timestamp        |
| amount_rs        |
+------------------+
```

### Explanation

- **Charger:** Stores charger identification, type and location.
- **User:** Stores customer information, membership tier and wallet balance.
- **ChargingSession:** Stores charging session details and timestamps.
- **Invoice:** Stores the calculated charges for each session.
- **WalletLedger:** Maintains wallet transaction history.
- **TopUp:** Stores money added to a user's wallet.

## 10. Session State Diagram

A charging session moves through different states during its lifecycle.

```text
        +-------------+
        |   CREATED   |
        +-------------+
               |
               v
        +-------------+
        | VALIDATION  |
        +-------------+
          /         \
         /           \
   Valid              Invalid
      |                  |
      v                  v
+-------------+   +-------------+
|   STARTED   |   |   REFUSED   |
+-------------+   +-------------+
      |
      v
+-------------+
| CHARGING    |
+-------------+
      |
      v
+-------------+
| COMPLETED   |
+-------------+
      |
      v
+-------------+
|   UNPLUGGED |
+-------------+
      |
      v
+-------------+
|   INVOICED  |
+-------------+
      |
      v
+-------------+
|   CHARGED   |
+-------------+
```

A qualifying faulted session with delivered energy below 0.5 kWh is recorded as `FREE_FAULT` and charged ₹0.00.

### Explanation

- **CREATED:** A session record is received.
- **VALIDATION:** The system checks the user's wallet balance and blocked status.
- **STARTED:** The session is allowed to start.
- **CHARGING:** The vehicle receives energy.
- **COMPLETED:** Charging is completed.
- **UNPLUGGED:** The charging cable is disconnected.
- **INVOICED:** The final invoice is calculated.
- **CHARGED:** The wallet is debited.
- **REFUSED:** The session is rejected because of low balance or blocked status.

## 11. Wallet State Diagram

```text
        +-------------+
        |   ACTIVE    |
        +-------------+
               |
               v
        +-------------+
        |   SESSION   |
        |   PAYMENT   |
        +-------------+
               |
               v
       Is balance negative?
          /          \
        Yes           No
         |             |
         v             v
   +-----------+  +-----------+
   |  BLOCKED  |  |  ACTIVE   |
   +-----------+  +-----------+
         |
         v
    Wallet Top-up
         |
         v
   Is balance >= 0?
       /      \
     Yes       No
      |         |
      v         v
  +--------+ +---------+
  | ACTIVE | | BLOCKED |
  +--------+ +---------+
```

The wallet is not debited or held at plug-in. The final invoice is debited at unplug time.

## 12. Business Rule Register

The following business rules define how charging sessions, billing, wallet transactions and user access are handled.

| Rule ID | Business Rule |
|---|---|
| BR-01 | AC_7KW charging costs ₹12 per kWh. |
| BR-02 | DC_30KW charging costs ₹18 per kWh. |
| BR-03 | DC_60KW charging costs ₹22 per kWh. |
| BR-04 | DC chargers have a time charge of ₹1 per minute for connected time beyond 60 minutes. AC chargers have no time charge. |
| BR-05 | The first 10 minutes after charging completion are free. After that, idle time costs ₹2 per minute. |
| BR-06 | The maximum idle charge is ₹300 per session. |
| BR-07 | SILVER members receive a 5% discount and GOLD members receive a 10% discount on the energy charge only. |
| BR-08 | GST is 18% on the amount remaining after subtracting the membership discount from energy, time and idle charges. |
| BR-09 | The final session charge after GST must be at least ₹20, except for a free faulted session. |
| BR-10 | If the fault flag is true and delivered energy is below 0.5 kWh, the session is free. At 0.5 kWh or above, normal billing applies. |
| BR-11 | A user can start a session only when the wallet balance is at least ₹100 and the user is not blocked. |
| BR-12 | Top-ups below ₹100 are rejected. |
| BR-13 | A top-up of ₹1,000 or more receives an additional 3% bonus. |
| BR-14 | No money is held at plug-in. The invoice amount is debited from the wallet when the session ends at unplug time. |
| BR-15 | If the invoice is greater than the wallet balance, the wallet can become negative and the user is blocked. |
| BR-16 | A blocked user remains blocked until a top-up brings the wallet balance to ₹0 or more. |
| BR-17 | Events are processed in timestamp order. At the same timestamp, top-ups are processed first, then session ends, then session starts. Events of the same type are ordered by ID. |
| BR-18 | All monetary values are rounded to two decimal places using the round-half-up method. Daily revenue is assigned to the date on which the session is unplugged. |

### Additional Business Rule Notes

- Connected minutes are calculated from plug-in time to charge-complete time.
- Idle minutes are calculated from charge-complete time to unplug time.
- A session refused because of low balance or blocked status is not billed as a completed charging session.
- A free faulted session has a final charge of ₹0.00.
- Every wallet movement is recorded in the wallet ledger with its resulting balance.

## 13. Invoice Calculation

The billing engine calculates the final invoice using energy charges, time charges, idle charges, membership discounts and GST.

### 13.1 Energy Charge

Energy charge depends on the charger type.

**Formula:**

Energy Charge = Energy Consumed (kWh) × Rate per kWh

| Charger Type | Rate |
|---|---:|
| AC_7KW | ₹12/kWh |
| DC_30KW | ₹18/kWh |
| DC_60KW | ₹22/kWh |

### 13.2 Time Charge

Time charge applies only to DC chargers when connected time is more than 60 minutes.

**Formula:**

Time Charge = Minutes beyond 60 × ₹1

If connected time is 60 minutes or less, the time charge is ₹0.

### 13.3 Idle Charge

The first 10 minutes after charging completion are free. Every additional minute costs ₹2.

**Formula:**

Idle Charge = Minimum of (Billable Idle Minutes × ₹2, ₹300)

### 13.4 Membership Discount

The discount applies only to the energy charge.

- SILVER: 5%
- GOLD: 10%
- BASIC: 0%

**Formula:**

Discount = Energy Charge × Membership Discount Rate

### 13.5 GST Calculation

GST is calculated at 18% after subtracting the membership discount.

**Formula:**

Taxable Amount = Energy Charge + Time Charge + Idle Charge − Discount

GST = Taxable Amount × 18%

### 13.6 Final Invoice

**Formula:**

Final Amount = Taxable Amount + GST

The minimum final charge is ₹20 for a billable session. A qualifying free faulted session is charged ₹0.

### 13.7 Example Calculation

Consider a DC_30KW charger with:

- Energy consumed = 10 kWh
- Connected time = 90 minutes
- Idle time = 15 minutes
- Membership = SILVER

Calculation:

1. Energy charge = 10 × ₹18 = ₹180
2. Time charge = (90 − 60) × ₹1 = ₹30
3. Idle charge = (15 − 10) × ₹2 = ₹10
4. Discount = 5% of ₹180 = ₹9
5. Taxable amount = ₹180 + ₹30 + ₹10 − ₹9 = ₹211
6. GST = 18% of ₹211 = ₹37.98
7. Final invoice = ₹211 + ₹37.98 = **₹248.98**

All monetary values are rounded to two decimal places using round-half-up.

## 14. Wallet and Top-up Management

The wallet module manages user balances, session payments, top-ups and blocked-user status.

### 14.1 Opening Wallet Balance

- Each user starts with the opening balance provided in `users.csv`.
- An OPENING entry is added to the wallet ledger.
- The wallet balance is updated after every transaction.

### 14.2 Session Payment

- The wallet balance is checked when a user plugs in.
- A minimum balance of ₹100 is required to start a session.
- No money is held at plug-in.
- The final invoice is debited at unplug time.
- If the invoice is greater than the available balance, the wallet may become negative.
- The user is then marked as BLOCKED.

### 14.3 Wallet Top-ups

- Top-ups below ₹100 are rejected.
- Top-ups of ₹100 or more are accepted.
- Top-ups of ₹1,000 or more receive a 3% bonus.
- Both the top-up amount and bonus are recorded separately in the ledger.

**Example:**

If a user adds ₹1,000:

- Top-up amount = ₹1,000
- Bonus = 3% of ₹1,000 = ₹30
- Total wallet increase = ₹1,030

### 14.4 Blocked User Management

- A user with a negative wallet balance is blocked.
- A blocked user cannot start another charging session.
- The user remains blocked until the wallet balance becomes ₹0 or more after a top-up.
- Once the balance reaches ₹0 or above, the user is unblocked.

### 14.5 Wallet Ledger

The wallet ledger maintains a record of every wallet transaction.

Each ledger entry contains:

- User ID
- Transaction timestamp
- Entry type
- Reference ID
- Transaction amount
- Wallet balance after the transaction

The ledger helps maintain a clear history of wallet activity and supports transaction tracking.

## 15. Event Processing and Timestamp Handling

The system processes all charging sessions and wallet top-ups in chronological order.

### 15.1 Event Processing Order

Events are processed according to the following priority when they have the same timestamp:

1. Wallet top-ups.
2. Session endings (unplug events).
3. Session starts (plug-in events).

If events have the same timestamp and type, they are ordered by their ID.

### 15.2 Time Calculations

- Connected time = Charge-complete time − Plug-in time.
- Idle time = Unplug time − Charge-complete time.
- Time charges apply only to DC chargers.
- All timestamps are provided in Indian Standard Time (IST).
- Timestamps are provided with whole-minute precision.

### 15.3 Session Billing Time

The invoice is calculated and debited when the session ends at unplug time. Daily revenue is assigned to the date of unplugging.

## 16. Input File Design

The system uses CSV files as input. These files contain charger details, user information, charging sessions and wallet top-ups.

### 16.1 chargers.csv

Stores information about registered charging stations.

| Column | Description |
|---|---|
| charger_id | Unique charger ID |
| charger_type | AC_7KW, DC_30KW or DC_60KW |
| location | Charger location |
| city | City where the charger is located |

### 16.2 users.csv

Stores registered user details.

| Column | Description |
|---|---|
| user_id | Unique user ID |
| user_name | User name |
| mobile | Mobile number |
| tier | BASIC, SILVER or GOLD |
| opening_balance_rs | Initial wallet balance |

### 16.3 sessions.csv

Stores charging session information.

| Column | Description |
|---|---|
| session_id | Unique session ID |
| user_id | User using the charger |
| charger_id | Charger used |
| plug_in_time | Session start time |
| charge_complete_time | Charging completion time |
| unplug_time | Session end time |
| kwh_delivered | Energy delivered |
| fault_flag | Indicates whether a fault occurred |

### 16.4 topups.csv

Stores wallet top-up transactions.

| Column | Description |
|---|---|
| topup_id | Unique top-up ID |
| user_id | User adding money |
| timestamp | Top-up date and time |
| amount_rs | Top-up amount |

## 17. Command File Design

The system reads commands from `commands.txt`. Each command is written on a separate line, with fields separated by the pipe symbol (`|`).

### Sample Commands

```text
LOAD_CHARGERS|chargers.csv
LOAD_USERS|users.csv
LOAD_SESSIONS|sessions.csv
LOAD_TOPUPS|topups.csv
PROCESS_EVENTS
DAILY_REPORT|2026-10-12
DAILY_REPORT|2026-10-13
DAILY_REPORT|2026-10-14
DAILY_REPORT|2026-10-15
DAILY_REPORT|2026-10-16
BLOCKED_USERS
```

Blank lines and lines beginning with `#` are ignored.

### Command Descriptions

- LOAD_CHARGERS: Loads charger information.
- LOAD_USERS: Loads user information and opening balances.
- LOAD_SESSIONS: Loads charging session records.
- LOAD_TOPUPS: Loads wallet top-up records.
- PROCESS_EVENTS: Processes events and generates invoices and wallet transactions.
- DAILY_REPORT: Generates daily revenue information for each charger for the given date.
- BLOCKED_USERS: Generates the list of blocked users.

## 18. Output File Design

The system generates four CSV output files.

### 18.1 invoices.csv

Contains one invoice record for every session, including refused sessions.

**Column order:**

```text
session_id,user_id,charger_id,status,reason,kwh_delivered,energy_rs,time_rs,idle_rs,discount_rs,gst_rs,total_rs
```

Possible status values:

- CHARGED
- FREE_FAULT
- REFUSED

Possible reason values:

- NONE
- LOW_BALANCE
- BLOCKED

Money fields are recorded as 0.00 for refused and free-fault sessions.

Invoices are generated in the same order as the records in `sessions.csv`.

### 18.2 wallet_ledger.csv

Stores every wallet transaction and the balance after that transaction.

**Column order:**

```text
user_id,timestamp,entry_type,reference_id,amount_rs,balance_rs
```

Ledger entry types:

- OPENING
- SESSION
- TOPUP
- TOPUP_BONUS
- TOPUP_REJECTED

Session debits are recorded as negative amounts. A rejected top-up is recorded with an amount of 0.00.

Ledger entries are maintained in transaction processing order.

### 18.3 daily_revenue.csv

Contains daily revenue information for each charger.

**Column order:**

```text
date,charger_id,charger_type,sessions,kwh,revenue_rs
```

The report contains one row per charger per requested date. Revenue is assigned to the date of unplugging. Rows are ordered by date and charger ID.

### 18.4 blocked_users.csv

Contains users whose wallet balances are negative and who are blocked from starting new sessions.

**Column order:**

```text
user_id,balance_rs
```

Blocked users are listed in user ID order.

## 19. Sample Data Pack

The project uses a sample dataset to test the billing and wallet engine.

The dataset contains:

- 15 registered chargers.
- 60 registered users across three membership tiers.
- 400 charging sessions.
- 172 wallet top-up records.
- Five days of sample data from 12 October 2026 to 16 October 2026.

The sample dataset includes normal transactions and special cases to test the business rules.

### Important Test Scenarios

1. A DC session lasting exactly 60 minutes has no time charge.
2. A DC session lasting 61 minutes has a ₹1 time charge.
3. Unplugging exactly 10 minutes after charging completion has no idle charge.
4. Unplugging after 11 minutes results in a ₹2 idle charge.
5. Idle charges exceeding ₹300 are limited to ₹300.
6. A user with exactly ₹100 can start a session.
7. A user with less than ₹100 cannot start a session.
8. A faulted session below 0.5 kWh is free.
9. A faulted session with exactly 0.5 kWh is billable.
10. A top-up below ₹100 is rejected.
11. A top-up of ₹1,000 receives a 3% bonus.
12. A user with a negative wallet balance remains blocked until the balance reaches ₹0 or more.

These scenarios help verify that the billing engine follows the specified business rules.

## 20. Testing Strategy

Testing is performed using Python's built-in `unittest` framework.

The test cases cover:

- Energy charge calculation.
- DC time charge calculation.
- Idle charge calculation and maximum limit.
- Membership discount calculation.
- GST calculation.
- Minimum invoice amount.
- Fault-based free sessions.
- Wallet balance validation.
- Wallet top-ups and bonus calculation.
- Blocked-user handling.
- Negative wallet balances.
- Wallet ledger transactions.
- Event processing order.
- Invoice generation.
- Daily revenue reports.

### Test Execution Commands

To run all test cases:

```bash
python -m unittest -v
```

To run the billing program:

```bash
python billing.py
```

The project contains 17 automated test cases across the billing and wallet test files. All 17 tests passed in the latest test execution.

## 21. Assumptions and Data Conventions

The system follows these conventions:

1. All timestamps use IST and the format `YYYY-MM-DD HH:MM:SS`.
2. All timestamps have whole-minute precision.
3. Monetary values are rounded to two decimal places using round-half-up.
4. No wallet amount is held at plug-in.
5. The invoice is debited at unplug time.
6. Free faulted sessions have a charge of ₹0.00.
7. Refused sessions are included in the invoice output.
8. Top-ups are processed before session endings and session starts when timestamps are equal.
9. Daily revenue is based on the unplug date.
10. The minimum invoice amount does not apply to qualifying free faulted sessions.

## 22. Project Deliverables

The project includes the following deliverables:

- Python source code for the EV charging billing and wallet engine.
- Charger, user, session and top-up CSV input files.
- Command file for processing operations.
- Invoice generation module.
- Wallet management and ledger module.
- Daily revenue report.
- Blocked-user report.
- Automated test cases.
- README documentation.
- Design document.
- Decision log.
- Test report.
- Demo script.

### GitHub Repository

Project repository:

https://github.com/Deepika-P-tech/E008-ECE-025

## 23. Conclusion

The EV Public Charging Session Billing and Wallet Engine provides a structured way to manage public EV charging transactions. It calculates charging costs based on charger type, connected time, idle time, membership discounts and GST.

The system also manages wallet balances, top-ups, bonuses, blocked users and transaction history. Automated testing helps verify the business rules and important edge cases.

The project demonstrates how Python can be used to develop a reliable backend system for EV public charging operations.
