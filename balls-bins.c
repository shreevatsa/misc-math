/*
  Balls go one-by-one into B bucket at random.
  At what time does some bucket first fill up size S?
  Also asked on MSE, http://math.stackexchange.com/questions/171179
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define B 10000
const int S = 64;
int size[B];

int main(int argc, char** argv) {
  if (argc != 3) {
    printf("Usage: %s <number of buckets> <size of each bucket>\n", argv[0]);
    return 1;
  }
  int B = atoi(argv[1]);

  int ntrials, T, i;
  double sum_T = 0;
  double sum_T_sq = 0;
  for (ntrials = 1; ; ++ntrials) {
    for (i = 0; i < B; ++i) size[i] = 0;
    for (T = 1; ; ++T) {
      int bucket = random() % B;
      ++size[bucket];
      if (size[bucket] > S) break;
    }
    double dT = (double) T;
    sum_T += dT;
    sum_T_sq += dT * dT;
    if (ntrials % 100 == 0) {
      double mean = sum_T / ntrials;
      double std_dev = sqrt(sum_T_sq / ntrials - mean * mean);
      printf("Sample: %d Mean: %.2lf Standard deviation: %.2lf (after %d trials) \n",
             T, mean, std_dev, ntrials);
    }
  }
}
