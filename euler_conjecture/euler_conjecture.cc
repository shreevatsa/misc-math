#include <array>
#include <iostream>
#include <map>
#include <utility>

typedef long long Int;
constexpr Int fifth_power(Int x) { return x * x * x * x * x; }

std::map<Int, int> known_fifth_powers = {{0, 0}};
bool is_fifth_power(Int n) {
  while (n > known_fifth_powers.rbegin()->first) {
    int m = known_fifth_powers.rbegin()->second  + 1;
    known_fifth_powers[fifth_power(m)] = m;
  }
  return known_fifth_powers.count(n);
}

std::array<Int, 4> four_nums() {
  static std::array<Int, 4> x = {1, 1, 1, 0};
  int i = 3;
  while (i > 0 && x[i] == x[i - 1]) --i;
  x[i] += 1;
  while (++i < 4) x[i] = 1;
  return x;
}

std::ostream& operator<<(std::ostream& os, std::array<Int, 4> x) {
  os << "(" << x[0] << ", " << x[1] << ", " << x[2] << ", " << x[3] << ")";
  return os;
}

int main() {
  while (true) {
    std::array<Int, 4> get = four_nums();
    Int rhs = fifth_power(get[0]) + fifth_power(get[1]) + fifth_power(get[2]) + fifth_power(get[3]);
    if (is_fifth_power(rhs)) {
      std::cout << "Found: " << get << " " << known_fifth_powers[rhs] << std::endl;
      break;
    }
  }
}
