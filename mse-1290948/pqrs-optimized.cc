#include <iostream>

#include "primes-by-length.h"

const int MAXN = 2 * 10000 * 10000;
int number_of_representations[MAXN];

int main() {
  const int num_primes = sizeof(primes_of_length_4) / sizeof(primes_of_length_4[0]);
  std::cerr << num_primes << " primes of length 4" << std::endl;
  for (int a = 0; a < num_primes; ++a) {
    int p = primes_of_length_4[a];
    std::cerr << "Passing prime: " << p << std::endl;
    for (int b = a + 1; b < num_primes; ++b) {
      int q = primes_of_length_4[b];
      for (int c = a + 1; c < num_primes; ++c) if (c != b) {
          int r = primes_of_length_4[c];
          for (int d = c + 1; d < num_primes; ++d) if (d != b) {
            int s = primes_of_length_4[d];
            ++number_of_representations[p * q + r * s];
          }
      }
    }
  }
  for (int i = 0; i < MAXN; ++i) {
    if (number_of_representations[i] > 0) {
      std::cout << i << "," << number_of_representations[i] << std::endl;
    }
  }
}
