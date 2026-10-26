
# EV Public Charging Session Billing and Wallet Engine

**Problem Statement:** ECE-025  
**Team ID:** E008  
**Language:** Java  
**Java Version:** Java 21

## 1. Project Overview

This project is a command-line application that calculates billing for electric vehicle (EV) charging sessions.

It calculates energy charges, charging time charges, idle fees, membership discounts, GST, and the final invoice amount. It also manages user wallets, top-ups, transaction records, and blocked-user status.

## 2. Main Features

- Register chargers and users.
- Read charging sessions from CSV files.
- Calculate invoices according to charger type.
- Apply membership discounts and GST.
- Manage wallet balances and top-ups.
- Maintain a transaction ledger.
- Generate daily revenue reports by charger.
- Generate a report of blocked users.
- Validate input records and test billing rules.

## 3. Charger Tariffs

| Charger Type | Rate |
|---|---:|
| AC_7KW | ₹12/kWh |
| DC_30KW | ₹18/kWh |
| DC_60KW | ₹22/kWh |

## 4. Billing Rules

- DC time charge: ₹1 per minute beyond 60 minutes.
- AC chargers: No time charge.
- Idle fee: ₹2 per minute after 10 free minutes, capped at ₹300 per session.
- SILVER membership: 5% discount on energy charges.
- GOLD membership: 10% discount on energy charges.
- GST: 18% on energy charge + time charge + idle fee − discount.
- Minimum invoice: ₹20 after GST.
- Faulted sessions delivering less than 0.5 kWh are free.

## 5. Wallet Rules

- A user needs at least ₹100 to start a session.
- Top-ups below ₹100 are rejected.
- Top-ups of ₹1,000 or more receive a 3% bonus.
- A negative wallet balance blocks the user.
- A blocked user can be unblocked when a top-up brings the balance to at least ₹0.

## 6. Project Files

- `Main.java` — Program entry point.
- `Charger.java` — Charger information.
- `User.java` — User and wallet information.
- `Session.java` — Charging session information.
- `BillingService.java` — Billing calculations.
- `E008_ECE025_Design_Document.pdf` — Project design document.

Additional classes, input files, reports, and tests will be added as development continues.

## 7. Requirements

- Java Development Kit (JDK) 17 or later.
- Visual Studio Code or another Java-compatible editor.

## 8. How to Run

1. Open the project folder in VS Code.
2. Open `Main.java`.
3. Click **Run** above the `main` method.

Alternatively, open a terminal in the project folder and run:

```bash
javac Main.java
java Main
```

The current starter program prints the project name and team ID. Full billing functionality is still under development.

## 9. Testing

The project will be tested for billing calculations, wallet transactions, top-ups, blocked-user status, CSV validation, and the required edge cases.

## 10. Project Status

**Current stage:** Initial Java setup and design documentation.  
**Next stage:** Implement and test the complete billing and wallet functionality.
