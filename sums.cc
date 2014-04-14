// Given N, S, K, find K numbers that add up to N and whose squares add up to S.
// (Brute force.)

#include <vector>
#include <cassert>
#include <iostream>
using namespace std;

int N, S, K;
vector<int> a;
int csum, ssum;

void search(int i) {
  assert(a.size() == i);
  if (i == 0) {
    csum = 0;
    ssum = 0;
  }
  if (i == K - 1) {
    int last = N - csum;
    if (last < a[i - 1] or ssum + last * last != S) return;
    a.push_back(last); csum += last; ssum += last * last;
    search(i + 1);
    a.pop_back(); csum -= last; ssum -= last * last;
    return;
  }
  if (i == K) {
    assert (csum == N);
    assert (ssum == S);
    for (int j = 0; j < i; ++j) cout << a[j] << " ";
    cout << endl;
    return;
  }
  int last = 1;
  if (i > 0) last = a[i - 1];
  for (int c = last; csum + (K - i) * c <= N and ssum + (K-i) * c*c <= S; ++c) {
    a.push_back(c); csum += c; ssum += c * c;
    search(i + 1);
    a.pop_back(); csum -= c; ssum -= c * c;
  }
}

int main() {
  cin >> N >> S;
  for (K = 2; K <= N; ++K) {
    cout << endl << "K = " << K << endl;
    search(0);
  }
}
