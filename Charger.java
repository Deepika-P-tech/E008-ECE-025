public class Charger {
    String chargerId;
    String chargerType;
    String location;

    public Charger(String chargerId, String chargerType, String location) {
        this.chargerId = chargerId;
        this.chargerType = chargerType;
        this.location = location;
    }

    public void displayCharger() {
        System.out.println("Charger ID: " + chargerId);
        System.out.println("Charger Type: " + chargerType);
        System.out.println("Location: " + location);
    }
}