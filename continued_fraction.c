//Find all best rational approximations of x
//http://shreevatsa.wordpress.com/2011/01/10/not-all-best-rational-approximations-are-the-convergents-of-the-continued-fraction/
//There is a mistake which results in a few extra terms being printed (see post). To be fixed.

#include <math.h>
#include <stdio.h>
#include <assert.h>

// number of terms in continued fraction.
// 15 is the max without precision errors for M_PI
#define MAX 15
#define eps 1e-9

long p[MAX], q[MAX], a[MAX], len;
void find_cf(double x) {
  int i;
  //The first two convergents are 0/1 and 1/0
  p[0] = 0; q[0] = 1;
  p[1] = 1; q[1] = 0;
  //The rest of the convergents (and continued fraction)
  for(i=2; i<MAX; ++i) {
    a[i] = lrint(floor(x));
    p[i] = a[i]*p[i-1] + p[i-2];
    q[i] = a[i]*q[i-1] + q[i-2];
    printf("%ld:  %ld/%ld\n", a[i], p[i], q[i]);
    len = i;
    if(fabs(x-a[i])<eps) return;
    x = 1.0/(x - a[i]);
  }
}

void all_best() {
  int i, n;
  for(i=2; i<len; ++i) {
    for(n = (a[i+1]+1)/2; n<=a[i+1]; ++n) {
      printf("%ld/%ld, ", n*p[i]+p[i-1], n*q[i]+q[i-1]);
    }
  }
}

int main(int argc, char **argv) {
  double x;
  if(argc==1) { x = M_PI; } else { sscanf(argv[1], "%lf", &x); }
  assert(x>0); printf("%.15lf\n\n", x);

  find_cf(x); printf("\n");
  all_best(); printf("\n");
  return 0;
}
