// Fixes to someone else's answer. 20x1 + 5x2 + 10x3 = 100, etc.
// http://stackoverflow.com/questions/6240770/how-can-i-program-a-large-number-of-for-loops/6240917#6240917
import java.util.Arrays;
class Diophantine {
            public static void findVariables(int[] constants, int sum, 
                                      int[] variables, int n, int result) {
                if (n == constants.length) { //your end condition for the recursion
                    if (result == sum) {
                        System.out.println(Arrays.toString(variables));
                    }
                } else if (result <= sum){ //keep going
                    for (int i = 0; constants[n]*i <= sum; i++) {
                        variables[n] = i;
                        findVariables(constants, sum, variables, n+1, result + constants[n]*i);
        
                    }
                }
            }

    public static void main(String[] args) {
        int sum = 100;
        int a1 = 20;
        int a2 = 5;
        int a3 = 10;
        int constants[] = new int[] {20, 5, 10};
        int variables[] = new int[] {0, 0, 0};
        findVariables(new int[] {20, 5, 10}, 100, new int[] {0,0,0}, 0, 0);
    }
}
