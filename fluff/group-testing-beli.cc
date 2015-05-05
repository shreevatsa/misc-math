// Copyright 2011 Google Inc. All Rights Reserved.
// Author: shreevatsa@google.com (Shreevatsa Rajagopalan)

// Ignore the below comment block
/*
  S = {0, ... 999} -- 100 bottles of wine.
  We have n prisoners. (n is 43 or less.)
  For each bottle in S, we have some subset of the n prisoners who drank it.
  The goal is to find a family of subsets such that if A U B = C U D,
  then {A, B} = {C, D} -- i.e.,
  being given the the union of two sets lets you determine which two sets.
*/

// Beli's algorithm
/*
  Let N = 2M, and start with F = all sets of (N choose M).
  For k = M+1 to N,
    for each set S of size k,
      if there are two pairs in F whose union is S,
        drop (any) one of them.
  Stop.
*/

#include <iostream>
#include <vector>
#include <map>
#include <set>
using namespace std;

const int MAX_SIZE = 30;
int size(int x) {
  int ans = 0;
  for(int i = 0; i < MAX_SIZE; ++i) if(x&(1<<i)) ++ans;
  return ans;
}

int main() {
  int M; cin >> M;
  int N = 2*M;
  vector<int> F[N+1]; //F[i] = all sets of size i
  for (int x = 0; x < (1<<N); ++x) {
    F[size(x)].push_back(x);
  }
  vector<int> oF = F[M];
  cerr << "Currently, we have " << oF.size() << " sets" <<endl;

  map<int, bool> seen;
  for (int k = M+1; k <= N; ++k) {
    cerr << "Trying k = " << k << " with " << oF.size() << " sets" << endl;
    set<int> nF;
    for (int i = 0; i < oF.size(); ++i) {
      for (int j = i+1; j < oF.size(); ++j) {
        int u = oF[i] | oF[j];
        if (size(u)==k) {
          if (not(seen[u])) {
            nF.insert(oF[i]);
            nF.insert(oF[j]);
          } else {
            //cerr << "Duplicate: " << u << " is already seen" <<endl;
            continue;
          }
        }
        seen[u] = true;
      }
    }
    oF = vector<int>(nF.begin(), nF.end());
  }
  cout << oF.size() << endl;
  return 0;
}
