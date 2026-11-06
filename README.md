# EV Public Charging Session Billing and Wallet Engine

**Team ID:** E008  
**Problem ID:** ECE-025  
**Team Members:** Deekshith S and Deepika P  
**Section:** ECM A

## 1. Project Overview

The EV Public Charging Session Billing and Wallet Engine is a Python-based backend system that manages electric vehicle charging sessions, calculates billing amounts, maintains user wallets, and generates revenue reports.

The system processes charging session events and wallet top-ups from CSV files using commands provided in `commands.txt`.

## 2. Objectives

- Register and manage EV chargers.
- Manage users and their wallet balances.
- Calculate charging session bills automatically.
- Apply membership discounts and GST.
- Calculate time and idle charges.
- Process wallet top-ups and bonus amounts.
- Maintain wallet transaction history.
- Identify and block users with negative balances.
- Generate daily charger-wise revenue reports.

## 3. Technologies Used

- **Programming Language:** Python 3.10+
- **Data Storage:** CSV files
- **Editor:** Visual Studio Code
- **Testing:** Python unittest framework

## 4. Charger Tariffs

| Charger Type | Energy Rate |
|---|---:|
| AC_7KW | ₹12/kWh |
| DC_30KW | ₹18/kWh |
| DC_60KW | ₹22/kWh |

## 5. Business Rules

1. A user needs at least ₹100 in their wallet to start a session.
2. DC chargers charge ₹1 per connected minute beyond 60 minutes.
3. The first 10 idle minutes are free.
4. Additional idle time costs ₹2 per minute, capped at ₹300.
5. SILVER members receive a 5% energy discount.
6. GOLD members receive a 10% energy discount.
7. GST is 18% after applying the energy discount.
8. The minimum final session charge is ₹20.
9. Faulted sessions below 0.5 kWh are free.
10. Top-ups below ₹100 are rejected.
11. Top-ups of ₹1,000 or more receive a 3% bonus.
12. Users with negative wallet balances are blocked until their balance becomes zero or positive.

## 6. Input Files

- `chargers.csv` – Charger information.
- `users.csv` – User and wallet information.
- `sessions.csv` – Charging session information.
- `topups.csv` – Wallet top-up information.
- `commands.txt` – Commands for processing the input files.

## 7. Output Files

- `invoices.csv` – Session-wise billing details.
- `wallet_ledger.csv` – Wallet transaction history.
- `daily_revenue.csv` – Daily revenue for each charger.
- `blocked_users.csv` – List of blocked users.

## 8. How to Run the Project

1. Install Python 3.10 or later.
2. Open the project folder in Visual Studio Code.
3. Open the terminal.
4. Run the billing program:

```bash
python billing.py
```

5. Run the automated tests:

```bash
python -m unittest -v
```

## 9. Project Structure

```text
E008-ECE-025/
│
├── main.py
├── billing.py
├── test_billing.py
├── test_wallet.py
├── commands.txt
│
├── chargers.csv
├── users.csv
├── sessions.csv
├── topups.csv
│
├── invoices.csv
├── wallet_ledger.csv
├── daily_revenue.csv
├── blocked_users.csv
│
├── README.md
├── DESIGN_DOCUMENT.md
├── DECISION_LOG.md
├── TEST_REPORT.md
└── DEMO_SCRIPT.md
```

## 10. Expected Outcome

The system automates EV charging session billing, wallet management, transaction tracking, user blocking, and charger-wise revenue reporting using Python and CSV files.

It provides a structured and testable backend solution for managing public EV charging sessions.
