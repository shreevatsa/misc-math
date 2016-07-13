#include <iostream>
#include <vector>
#include <set>
#include <cassert>

const int MAXN = 100;
const int MINN = 1;
const int SIZE = 8;

bool used[MAXN];
std::vector<int> a;
std::set<int> known_sums;

bool ok(int n) {
  if (used[n]) return false;
  for (int s : known_sums) {
    if (known_sums.count(s + n)) {
      return false;
    }
  }
  return true;
}


void fill(int k) {
  assert(k == a.size());
  if (k == SIZE) {
    // Found a sum-free subset of size SIZE. Print it.
    for (int i = 0; i < a.size(); ++i) {
      std::cout << a[i] << " ";
    }
    std::cout << std::endl;
    return;
  }

  for (int n = MINN; n < MAXN; ++n) {
    if (ok(n)) {
      std::set<int> old_set = known_sums;

      a.push_back(n); used[n] = true;
      for (int s : old_set) {
        known_sums.insert(s + n);
      }

      fill(k + 1);

      known_sums = old_set;
      a.pop_back(); used[n] = false;
    }
  }
}

int main() {
  known_sums.insert(0);
  fill(0);
}
