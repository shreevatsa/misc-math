#include <vector>
#include <iostream>
int main() {
  std::vector<int> v;
  v.push_back(0);
  for (int i = 0;; ++i) {
    std::cout << i << std::endl;
    int& n = v[0];
    v.push_back(0);
    n += 1;
  }
}
