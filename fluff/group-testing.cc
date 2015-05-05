// Copyright 2011 Google Inc. All Rights Reserved.
// Author: shreevatsa@google.com (Shreevatsa Rajagopalan)

// Ignore the below comment block
/*
  The goal is to find a family of subsets of [n] such that if A U B = C U D,
  then {A, B} = {C, D} -- i.e.,
  being given the the union of two sets lets you determine which two sets.

  Horrible brute-force: Try all subsets of 2^[n].
  So there are 2^(2^n)) choices to test.
  For n=4, 2^16 is ok.
  For n=5, 2^32 may be a bit too much.
  For n=6, forget about 2^64.
*/

#include <iostream>
#include <cassert>
#include <vector>
#include <map>
#include <set>
using namespace std;

typedef long long ll;
const int MAX_SIZE = 32;
int size(ll x) {
  int ans = 0;
  for(int i = 0; i < MAX_SIZE; ++i) if(x&(ll(1)<<i)) ++ans;
  return ans;
}

bool suf(vector<int> F) {
  map<int, bool> seen;
  bool ok = true;
  for(int i=0; i < F.size(); ++i) {
    for(int j=i+1; j < F.size(); ++j) {
      int u = F[i]|F[j];
      if(seen[u]) {
        ok = false;
        break;
      } else {
        //cerr << "Not yet seen: " << u << endl;
      }
      seen[u] = true;
    }
  }
  return ok;
}

int main() {
  int N; cin >> N;
  int tN = 1<<N;   // 0 to tN-1 are the subsets of [N]
  ll ttN = ll(1)<<tN;
  vector<int> bF;

  int best = 0;
  for(ll w=0; w < ttN; ++w) {
    // The sets we pick are those in W
    vector<int> F;
    for(int i=0; i < tN; ++i) if(w&(ll(1)<<i)) F.push_back(i);
    assert(F.size() == size(w));
    // Now check if F is strongly union-free
    if(suf(F) and best<F.size()) {
      best = F.size();
      bF = F;
    }
  }
  // int a[] = {0, 1, 2, 4, 8};
  // bF = vector<int>(a, a+5);

  cout << best << " " << boolalpha << suf(bF) << endl;
  for(int i=0; i<bF.size(); ++i) {
    cout << bF[i] << " ";
  }
  cout << endl;

  return 0;
}
