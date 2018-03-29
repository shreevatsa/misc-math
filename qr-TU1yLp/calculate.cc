#include <cstdio>
#include "FJ64_16k.h" // For a fast `is_prime` function: http://ceur-ws.org/Vol-1326/020-Forisek.pdf

int main() {
  double ans = 0.5;
  for (uint64_t p = 0; ; ++p) {
    if (p % 1000000 == 0) {
      printf("%lld %.9f\n", p, ans);
    }
    if (!is_prime(p)) continue;
    double mul = -1;
    if (p % 3 == 1) mul = (p - 2.0) / (p - 1.0);
    if (p % 3 == 2) mul = p / (p - 1.0);
    if (p % 3 != 0) {
      ans *= mul;
      printf("%lld (%d) multiplying by %.2f to get %.9f\n", p, (p % 3), mul, ans);
    }
  }
}




