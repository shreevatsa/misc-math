#include <cassert>
#include <iostream>
#include <map>
#include <vector>

#include "primes-by-length.h"

// std::map<int, int> number_of_representations;
const int MAXN = 2 * 10000 * 10000;
int number_of_representations[MAXN];

int main() {
  std::cerr << "Have primes up to length: " << primes_by_length.size() << std::endl;
  for (int i = 3; i < 4; ++i) {
    assert(i < primes_by_length.size());
    std::cerr << primes_by_length[i].size() << " primes of length " << i + 1 << std::endl;
    // number_of_representations.clear();
    int np = 0;
    for (int p : primes_by_length[i]) {
      if (np++ % 10 == 0) std::cerr << "Passing prime: " << p << std::endl;
      for (int q : primes_by_length[i]) if (q > p) {
        for (int r : primes_by_length[i]) if (r > p && r != q) {
          for (int s : primes_by_length[i]) if (s > r && s != q) {
            ++number_of_representations[p * q + r * s];
          }
        }
      }
    }
    // for (const auto& num : number_of_representations) {
    //   std::cout << num.first << "," << num.second << std::endl;
    // }
    for (int i = 0; i < MAXN; ++i) {
      if (number_of_representations[i] > 0) {
        std::cout << i << "," << number_of_representations[i] << std::endl;
      }
    }
  }
}
