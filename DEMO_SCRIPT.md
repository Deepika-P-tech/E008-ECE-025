# 5-MINUTE PROJECT DEMONSTRATION
## EV Public Charging Session Billing and Wallet Engine

### 1. Introduction (30 seconds)
Good morning everyone. Our project title is **EV Public Charging Session Billing and Wallet Engine**. Our team ID is E008, and our problem ID is ECE-025.

The project is designed to automate billing and wallet management for electric vehicle public charging stations.

### 2. Problem Statement (40 seconds)
Manual billing can cause calculation errors and difficulty in tracking payments. Charging stations also need to manage idle fees, membership discounts, GST, wallet balances, and faulty charging sessions.

Our system handles these operations automatically.

### 3. Technologies Used (30 seconds)
We developed the project using Python. We use CSV files for input data and output reports. Python's Decimal module supports accurate money calculations, and the unittest framework is used for testing.

### 4. Working of the System (1 minute 30 seconds)
First, the system loads charger details, user details, charging sessions, and wallet top-ups from CSV files.

Next, it processes events in chronological order.

When a user starts charging, the system checks whether the wallet has at least ₹100 and whether the user is blocked.

After charging, the system calculates:
- Energy charges
- Time charges for DC chargers
- Idle charges
- Membership discounts
- GST

Finally, the system generates the invoice and updates the wallet ledger.

### 5. Special Features (1 minute)
Our system supports:
- Three charger types: AC 7 kW, DC 30 kW, and DC 60 kW.
- SILVER and GOLD membership discounts.
- Idle fee limits of ₹300.
- GST calculation at 18%.
- Fault handling for sessions below 0.5 kWh.
- Wallet top-ups and bonus credits.
- Automatic blocking of users with negative wallet balances.

### 6. Testing and Outputs (40 seconds)
We created 10 automated test cases using Python unittest.

The system generates four output files:
1. invoices.csv
2. wallet_ledger.csv
3. daily_revenue.csv
4. blocked_users.csv

These files help track billing, wallet transactions, daily revenue, and blocked users.

### 7. Conclusion (10 seconds)
In conclusion, our project provides an automated and organized solution for EV charging billing and wallet management.

Thank you.