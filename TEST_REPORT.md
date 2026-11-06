# TEST REPORT

## EV Public Charging Session Billing and Wallet Engine

**Team ID:** E008  
**Problem ID:** ECE-025  
**Programming Language:** Python

### 1. Testing Objective

To verify that the billing engine correctly calculates charging costs, applies discounts and GST, handles wallet transactions, and processes fault conditions.

### 2. Testing Tool

Python `unittest` framework.

### 3. Test Cases

| No. | Test case | Expected result |
|---|---|---|
| 1 | DC charging for exactly 60 minutes | No time fee |
| 2 | DC charging for 61 minutes | ₹1 time fee |
| 3 | Idle time of 10 minutes | No idle fee |
| 4 | Idle time of 11 minutes | ₹2 idle fee |
| 5 | Idle fee exceeds ₹300 | Fee capped at ₹300 |
| 6 | Fault with less than 0.5 kWh | Free session |
| 7 | Fault with exactly 0.5 kWh | Billable session |
| 8 | Fault with 0.6 kWh | Billable session |
| 9 | SILVER membership | 5% energy discount |
| 10 | GOLD membership | 10% energy discount |
| 11 | Wallet balance exactly ₹100 | Session allowed |
| 12 | Wallet balance below ₹100 | Session refused |
| 13 | Top-up below ₹100 | Top-up rejected |
| 14 | Top-up of ₹1,000 | 3% bonus added |
| 15 | Wallet overdraft | User blocked |
| 16 | Blocked user starts another session | Session refused |
| 17 | Sufficient top-up after blocking | User unblocked |

### 4. Test Execution

Command:

`python -m unittest -v`

### 5. Test Result

- Total test cases executed: **17**
- Billing tests passed: **10**
- Wallet tests passed: **7**
- Failed tests: **0**
- Test framework: Python `unittest`
- Execution time: **0.012 seconds**

### 6. Conclusion

All 17 test cases passed successfully. The billing and wallet modules work as expected for the tested business rules and edge cases.
