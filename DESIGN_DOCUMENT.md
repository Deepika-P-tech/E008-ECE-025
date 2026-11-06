# EV Public Charging Session Billing and Wallet Engine

**Team ID:** E008  
**Problem ID:** ECE-025  
**Team Members:** Deekshith S and Deepika P  
**Section:** ECM A

## 1. Project Overview

The EV Public Charging Session Billing and Wallet Engine is a Python-based backend application that processes EV charging sessions, calculates invoices, manages user wallets, and generates daily revenue reports.

## 2. Objectives

- Manage EV chargers and users.
- Process charging sessions from CSV files.
- Calculate energy, time, and idle charges.
- Apply membership discounts and GST.
- Maintain wallet balances and transaction history.
- Block users with negative balances.
- Generate daily revenue reports.

## 3. Technology Stack

- Python 3.10+
- CSV files
- Visual Studio Code
- Python unittest

## 4. System Modules

1. Charger Management
2. User Management
3. Session Processing
4. Invoice Calculation
5. Wallet Management
6. Top-up Management
7. Revenue Reporting
8. Automated Testing

## 5. Glossary

| Term | Meaning |
|---|---|
| AC | Alternating Current |
| DC | Direct Current |
| kWh | Kilowatt-hour |
| GST | Goods and Services Tax |
| Invoice | Final charging bill |
| Wallet | User's available money balance |
| Ledger | Record of wallet transactions |
| Idle time | Time between charging completion and unplugging |

## 6. Class Diagram

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
| energy_charge    |
| time_charge      |
| idle_charge      |
| discount         |
| GST              |
| total            |
+------------------+

+------------------+
|       User       |
+------------------+
| user_id          |
| user_name        |
| tier             |
| wallet_balance   |
+------------------+
         |
         | has
         |
+------------------+
|   WalletLedger   |
+------------------+
| timestamp        |
| entry_type       |
| amount           |
| balance          |
+------------------+

User also makes TopUps.
```

## 7. Session State Diagram

```text
       NEW SESSION
            |
            v
     CHECK WALLET
            |
       +----+----+
       |         |
   Balance     Balance
   below 100   at least 100
       |         |
       v         v
    REFUSED    ACTIVE
                 |
                 v
             SESSION END
                 |
          +------+------+
          |             |
       Fault true    Normal session
       and kWh<0.5       |
          |             |
          v             v
      FREE_FAULT     COMPLETED
          |             |
          v             v
       ₹0 BILL       CALCULATE BILL
                        |
                        v
                   DEBIT WALLET
                        |
                 Negative balance?
                        |
                       YES
                        |
                        v
                     BLOCKED
```

## 8. Business Rule Register

| Rule ID | Business Rule |
|---|---|
| BR-01 | AC_7KW: ₹12/kWh, DC_30KW: ₹18/kWh, DC_60KW: ₹22/kWh |
| BR-02 | DC time charge is ₹1/minute beyond 60 minutes |
| BR-03 | First 10 idle minutes are free; later ₹2/minute, maximum ₹300 |
| BR-04 | SILVER discount 5%, GOLD discount 10%, on energy only |
| BR-05 | GST is 18%; minimum final invoice is ₹20 |
| BR-06 | Faulted sessions below 0.5 kWh are free |
| BR-07 | Minimum wallet balance to start is ₹100 |
| BR-08 | Top-ups below ₹100 are rejected; top-ups of ₹1,000 or more get 3% bonus |

## 9. Input Files

- chargers.csv
- users.csv
- sessions.csv
- topups.csv
- commands.txt

## 10. Output Files

- invoices.csv
- wallet_ledger.csv
- daily_revenue.csv
- blocked_users.csv

## 11. Testing

The project uses Python's unittest framework to test the billing calculations and important edge cases, including time charges, idle charges, fault conditions, and membership discounts.

## 12. Conclusion

The system provides an automated backend solution for EV public charging billing, wallet management, transaction tracking, and revenue reporting.