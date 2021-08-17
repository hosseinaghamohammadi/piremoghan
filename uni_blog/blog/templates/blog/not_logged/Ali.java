import java.util.Scanner;

public class Ali{
    public static void main(String[] args) {
        long bef = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        // System.out.println("Hello");
        Scanner scanner = new Scanner(System.in);
        int[] ali = new int[40000];

        long af = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        System.out.println(af - bef);
    }
}