public class User {
    String userId;
    String membershipTier;
    double walletBalance;
    boolean blocked;

    public User(String userId, String membershipTier, double walletBalance) {
        this.userId = userId;
        this.membershipTier = membershipTier;
        this.walletBalance = walletBalance;
        this.blocked = false;
    }

    public void displayUser() {
        System.out.println("User ID: " + userId);
        System.out.println("Membership: " + membershipTier);
        System.out.println("Wallet Balance: Rs. " + walletBalance);
        System.out.println("Blocked: " + blocked);
    }
}
