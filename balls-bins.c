/*
  Balls go one-by-one into B buckets at random.
  What is the first time at which some bucket fills up to size S?
  Asked on http://math.stackexchange.com/questions/171179
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main(int argc, char **argv) {
  if (argc != 3) {
    printf("Usage: %s <number of buckets> <size of each bucket>\n", argv[0]);
    return 1;
  }
  int B = atoi(argv[1]);
  int S = atoi(argv[2]);
  int *size = malloc(B * sizeof(int));

  int ntrials, T, i;
  double sum_T = 0, sum_T_sq = 0;
  srandom(time(NULL));
  for (ntrials = 1;; ++ntrials) {
    for (i = 0; i < B; ++i) size[i] = 0;
    for (T = 1;; ++T) {
      int bucket = random() % B;
      ++size[bucket];
      if (size[bucket] > S) break;
    }
    double dT = T;
    sum_T += dT;
    sum_T_sq += dT * dT;
    if (ntrials % 100 == 0) {
      double mean = sum_T / ntrials;
      double std_dev = sqrt(sum_T_sq / ntrials - mean * mean);
      printf("Sample: %d Mean: %.2lf Standard deviation: %.2lf (after %d trials)\n",
             T, mean, std_dev, ntrials);
    }
  }
}
