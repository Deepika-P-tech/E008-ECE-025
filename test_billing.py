
import unittest
from decimal import Decimal

from billing import calculate_invoice


class BillingTests(unittest.TestCase):

    def setUp(self):
        self.charger_ac = {"charger_type": "AC_7KW"}
        self.charger_dc = {"charger_type": "DC_30KW"}
        self.user = {"tier": "REGULAR"}

    def make_session(
        self,
        plug_in="2026-10-12 10:00:00",
        complete="2026-10-12 11:00:00",
        unplug="2026-10-12 11:10:00",
        kwh="5",
        fault="false"
    ):
        return {
            "plug_in_time": plug_in,
            "charge_complete_time": complete,
            "unplug_time": unplug,
            "kwh_delivered": kwh,
            "fault_flag": fault
        }

    def test_dc_exactly_60_minutes_no_time_fee(self):
        result = calculate_invoice(
            self.make_session(),
            self.charger_dc,
            self.user
        )
        self.assertEqual(result["time_rs"], Decimal("0.00"))

    def test_dc_61_minutes_one_rupee_time_fee(self):
        result = calculate_invoice(
            self.make_session(
                complete="2026-10-12 11:01:00"
            ),
            self.charger_dc,
            self.user
        )
        self.assertEqual(result["time_rs"], Decimal("1.00"))

    def test_exactly_10_idle_minutes_no_idle_fee(self):
        result = calculate_invoice(
            self.make_session(),
            self.charger_ac,
            self.user
        )
        self.assertEqual(result["idle_rs"], Decimal("0.00"))

    def test_11_idle_minutes_two_rupee_fee(self):
        result = calculate_invoice(
            self.make_session(
                unplug="2026-10-12 11:11:00"
            ),
            self.charger_ac,
            self.user
        )
        self.assertEqual(result["idle_rs"], Decimal("2.00"))

    def test_idle_fee_maximum_300(self):
        result = calculate_invoice(
            self.make_session(
                unplug="2026-10-12 14:30:00"
            ),
            self.charger_ac,
            self.user
        )
        self.assertEqual(result["idle_rs"], Decimal("300.00"))

    def test_fault_below_half_kwh_is_free(self):
        result = calculate_invoice(
            self.make_session(kwh="0.49", fault="true"),
            self.charger_ac,
            self.user
        )
        self.assertEqual(result["status"], "FREE_FAULT")
        self.assertEqual(result["total_rs"], Decimal("0.00"))

    def test_fault_at_half_kwh_is_billable(self):
        result = calculate_invoice(
            self.make_session(kwh="0.50", fault="true"),
            self.charger_ac,
            self.user
        )
        self.assertEqual(result["status"], "CHARGED")

    def test_fault_at_0_6_kwh_is_billable(self):
        result = calculate_invoice(
            self.make_session(kwh="0.60", fault="true"),
            self.charger_ac,
            self.user
        )
        self.assertEqual(result["status"], "CHARGED")
        self.assertEqual(result["total_rs"], Decimal("20.00"))

    def test_silver_discount_is_five_percent(self):
        silver_user = {"tier": "SILVER"}
        result = calculate_invoice(
            self.make_session(kwh="10"),
            self.charger_ac,
            silver_user
        )
        self.assertEqual(result["discount_rs"], Decimal("6.00"))

    def test_gold_discount_is_ten_percent(self):
        gold_user = {"tier": "GOLD"}
        result = calculate_invoice(
            self.make_session(kwh="10"),
            self.charger_ac,
            gold_user
        )
        self.assertEqual(result["discount_rs"], Decimal("12.00"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
