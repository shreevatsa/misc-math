#include <vector>
#include <iostream>

struct node {
  int a, b, c, d;
};

int main() {
  std::vector<node> v;
  v.push_back({});
  for (int i = 0;; ++i) {
    std::cout << i << std::endl;
    node& n = v[0];
    v.push_back({});
    n.a += 1;
  }
}
