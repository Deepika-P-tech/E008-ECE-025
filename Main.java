import java.math.BigDecimal;
import java.time.LocalDateTime;

public class Main {

    public static void main(String[] args) {

        // Project details
        System.out.println("EV Charging Billing Engine");
        System.out.println("Team ID: E008");
        System.out.println("Project: ECE-025");
        System.out.println("--------------------------------");

        // 1. Create a charger
        Charger charger = new Charger(
            "CH001",
            "AC_7KW",
            "Bengaluru"
        );

        charger.displayCharger();
        System.out.println("--------------------------------");

        // 2. Create a user
        User user = new User(
            "U001",
            "GOLD",
            500.00
        );

        user.displayUser();
        System.out.println("--------------------------------");

        // 3. Create a charging session
        Session session = new Session(
            "S001",
            "U001",
            "CH001",
            LocalDateTime.parse("2026-10-26T10:00:00"),
            LocalDateTime.parse("2026-10-26T10:45:00"),
            LocalDateTime.parse("2026-10-26T10:50:00"),
            5.0,
            false
        );

        session.displaySession();
        System.out.println("--------------------------------");

        // 4. Create the billing service
        BillingService billing = new BillingService();

        // 5. Calculate energy charge
        BigDecimal energyCharge =
            billing.calculateEnergyCharge(charger, session);

        System.out.println("Energy Charge: Rs. " + energyCharge);

        // 6. Create a DC charger for the time-charge test
        Charger dcCharger = new Charger(
            "CH002",
            "DC_30KW",
            "Bengaluru"
        );

        // 7. Calculate DC time charge
        BigDecimal timeCharge =
            billing.calculateTimeCharge(dcCharger, session);

        System.out.println("DC Time Charge: Rs. " + timeCharge);

        // 8. Calculate idle fee
        BigDecimal idleFee =
            billing.calculateIdleFee(session);

        System.out.println("Idle Fee: Rs. " + idleFee);

        // 9. Calculate membership discount
        BigDecimal discount =
            billing.calculateDiscount(user, energyCharge);

        System.out.println("Membership Discount: Rs. " + discount);

        // 10. Calculate taxable amount
        BigDecimal taxableAmount = energyCharge
            .add(timeCharge)
            .add(idleFee)
            .subtract(discount)
            .max(BigDecimal.ZERO);

        System.out.println("Taxable Amount: Rs. " + taxableAmount);

        // 11. Calculate GST
        BigDecimal gst = billing.calculateGST(taxableAmount);

        System.out.println("GST: Rs. " + gst);

        // 12. Calculate final invoice
        BigDecimal total = billing.calculateInvoiceTotal(
            energyCharge,
            timeCharge,
            idleFee,
            discount,
            session.faulted,
            session.energyDelivered
        );

        System.out.println("--------------------------------");
        System.out.println("FINAL INVOICE");
        System.out.println("--------------------------------");
        System.out.println("Energy Charge: Rs. " + energyCharge);
        System.out.println("Time Charge: Rs. " + timeCharge);
        System.out.println("Idle Fee: Rs. " + idleFee);
        System.out.println("Discount: Rs. " + discount);
        System.out.println("GST: Rs. " + gst);
        System.out.println("Final Invoice: Rs. " + total);
        System.out.println("--------------------------------");
    }
}