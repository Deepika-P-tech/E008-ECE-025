# Decision Log – E008-ECE-025

| No. | Decision | Reason |
|---:|---|---|
| 1 | Use Python | Simple backend implementation |
| 2 | Use CSV files | Required input and output format |
| 3 | Use command-driven execution | No graphical interface required |
| 4 | Separate charger data | Easier charger management |
| 5 | Separate user data | Easier wallet management |
| 6 | Use chronological event processing | Correct transaction ordering |
| 7 | Process top-ups first at equal timestamps | Required event priority |
| 8 | Process unplug events before plug-in events | Required event priority |
| 9 | Use Decimal for money | Avoid floating-point billing errors |
| 10 | Apply membership discount only to energy | Follows billing rules |
| 11 | Apply GST after discount | Follows billing formula |
| 12 | Limit idle fee to ₹300 | Prevent excessive idle charges |
| 13 | Use a ₹100 session-start requirement | Wallet eligibility rule |
| 14 | Block negative-balance users | Prevent further session starts |
| 15 | Give 3% bonus on qualifying top-ups | Wallet incentive rule |
| 16 | Use unittest | Automated validation |
| 17 | Generate separate output CSV files | Easier reporting |
| 18 | Keep input and output files separate | Better project organization |

