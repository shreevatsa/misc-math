#include <iostream>
#include <fstream>
#include <cmath>
typedef uint64_t ll;

/* For fast is_prime. See http://ceur-ws.org/Vol-1326/020-Forisek.pdf */
#include "FJ64_16k.h"

int main() {
  for (int i = 0; i < 200; ++i) if (is_prime(i)) std::cout << i << " "; std::cout << std::endl;

  std::ofstream bins1("bins-n2-n-1.txt"), bins2("bins-n2-21n-1.txt");
  ll limit = 1'000'000'00'0;
  const int BIN_SIZE = 100000;
  std::cout << "Will go up to " << limit << " in bins of size " << BIN_SIZE
            << " (so " << limit / BIN_SIZE << " bins in all)" << std::endl;

  int current_bin1 = 0;
  int current_bin2 = 0;
  for (ll n = 1; n <= limit; ++n) {
    current_bin1 += is_prime(n*n + n + 1);
    current_bin2 += is_prime(n*n + 21*n + 1);
    if (n % BIN_SIZE == 0) {
      bins1 << current_bin1 << std::endl;
      bins2 << current_bin2 << std::endl;
      current_bin1 = 0;
      current_bin2 = 0;
      std::cout << "Done up to " << n << std::endl;
    }
  }
}

