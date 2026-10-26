
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.Duration;

public class BillingService {

    private static final BigDecimal GST_RATE = new BigDecimal("0.18");
    private static final BigDecimal MINIMUM_CHARGE = new BigDecimal("20.00");
    private static final BigDecimal IDLE_RATE = new BigDecimal("2.00");
    private static final BigDecimal IDLE_CAP = new BigDecimal("300.00");

    public BigDecimal calculateEnergyCharge(Charger charger, Session session) {
        BigDecimal tariff;

        switch (charger.chargerType) {
            case "AC_7KW":
                tariff = new BigDecimal("12.00");
                break;
            case "DC_30KW":
                tariff = new BigDecimal("18.00");
                break;
            case "DC_60KW":
                tariff = new BigDecimal("22.00");
                break;
            default:
                throw new IllegalArgumentException("Invalid charger type");
        }

        return tariff.multiply(BigDecimal.valueOf(session.energyDelivered))
                .setScale(2, RoundingMode.HALF_UP);
    }

    public BigDecimal calculateTimeCharge(Charger charger, Session session) {
        if (charger.chargerType.equals("AC_7KW")) {
            return new BigDecimal("0.00");
        }

        long minutes = Duration.between(
                session.plugInTime,
                session.chargeCompleteTime
        ).toMinutes();

        long chargeableMinutes = Math.max(0, minutes - 60);

        return BigDecimal.valueOf(chargeableMinutes)
                .setScale(2, RoundingMode.HALF_UP);
    }

    public BigDecimal calculateIdleFee(Session session) {
        long idleMinutes = Duration.between(
                session.chargeCompleteTime,
                session.unplugTime
        ).toMinutes();

        long chargeableMinutes = Math.max(0, idleMinutes - 10);

        BigDecimal fee = IDLE_RATE.multiply(
                BigDecimal.valueOf(chargeableMinutes)
        );

        return fee.min(IDLE_CAP).setScale(2, RoundingMode.HALF_UP);
    }

    public BigDecimal calculateDiscount(User user, BigDecimal energyCharge) {
        BigDecimal discountRate;

        switch (user.membershipTier) {
            case "SILVER":
                discountRate = new BigDecimal("0.05");
                break;
            case "GOLD":
                discountRate = new BigDecimal("0.10");
                break;
            default:
                discountRate = BigDecimal.ZERO;
        }

        return energyCharge.multiply(discountRate)
                .setScale(2, RoundingMode.HALF_UP);
    }

    public BigDecimal calculateGST(BigDecimal amountBeforeGST) {
        return amountBeforeGST.multiply(GST_RATE)
                .setScale(2, RoundingMode.HALF_UP);
    }

    public BigDecimal calculateInvoiceTotal(
            BigDecimal energyCharge,
            BigDecimal timeCharge,
            BigDecimal idleFee,
            BigDecimal discount,
            boolean faulted,
            double energyDelivered
    ) {
        if (faulted && energyDelivered < 0.5) {
            return new BigDecimal("0.00");
        }

        BigDecimal taxableAmount = energyCharge
                .add(timeCharge)
                .add(idleFee)
                .subtract(discount)
                .max(BigDecimal.ZERO);

        BigDecimal gst = calculateGST(taxableAmount);

        BigDecimal total = taxableAmount.add(gst)
                .setScale(2, RoundingMode.HALF_UP);

        return total.max(MINIMUM_CHARGE);
    }
}
