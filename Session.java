import java.time.LocalDateTime;

public class Session {

    String sessionId;
    String userId;
    String chargerId;

    LocalDateTime plugInTime;
    LocalDateTime chargeCompleteTime;
    LocalDateTime unplugTime;

    double energyDelivered;
    boolean faulted;

    public Session(
            String sessionId,
            String userId,
            String chargerId,
            LocalDateTime plugInTime,
            LocalDateTime chargeCompleteTime,
            LocalDateTime unplugTime,
            double energyDelivered,
            boolean faulted) {

        this.sessionId = sessionId;
        this.userId = userId;
        this.chargerId = chargerId;
        this.plugInTime = plugInTime;
        this.chargeCompleteTime = chargeCompleteTime;
        this.unplugTime = unplugTime;
        this.energyDelivered = energyDelivered;
        this.faulted = faulted;
    }

    public void displaySession() {
        System.out.println("Session ID: " + sessionId);
        System.out.println("User ID: " + userId);
        System.out.println("Charger ID: " + chargerId);
        System.out.println("Energy Delivered: " + energyDelivered + " kWh");
        System.out.println("Faulted: " + faulted);
    }
}
