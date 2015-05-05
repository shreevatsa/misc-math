/*
Cows and bulls, without the cows. http://blog.tanyakhovanova.com/?p=386

There are n items, each true or false.
Attempt: query a particular set of them, and be told how many are true.
How many attempts do you need to identify all?

Strategy:
First attempt is any of the 2^n sets.
There are n+1 possible answers, each constraining which set our "true" set is.
Repeat
*/

#include <algorithm>
#include <cassert>
#include <map>
#include <set>
#include <iostream>
using namespace std;
#define LET(a,b) typeof(b) a = b
#define FOREACH(it, s) for(LET(it, s.begin()); it != s.end(); ++it)

typedef long long ll;

int bitcount(ll n) {
  int ans = 0;
  while (n) {
    ans += n%2;
    n /= 2;
  }
  return ans;
}

string buf(int depth) {
  string s(depth*8, ' ');
  return s;
}

map<ll, int> cache;
int attempts(int depth, int n, ll poss_sets) {
  if (cache.count(poss_sets)) return cache[poss_sets];
  if (bitcount(poss_sets) == 1) {
    return 1;
  }

  ll t = ll(1)<<n;

  cerr << buf(depth) << "Attempts needed for " << n << " starting with possible sets ";
  for (ll s = 0; s < t; ++s) {
    if (poss_sets&(ll(1)<<s)) cerr << s << ", ";
  }
  cerr << endl;

  int ret = 0;
  for (ll q = 0; q < t; ++q) {
    // Let's ask "q" as our question. What answers could we get?
    cerr << buf(depth) << "Asking " << q << ": " << endl;
    map< int, set<int> > sets_for_answer;
    for (ll s = 0; s < t; ++s) {
      if (not(poss_sets & (1<<s))) continue;
      // If s could be one of the sets that are "true"
      ll c = s & q;
      sets_for_answer[bitcount(c)].insert(s);
    }
    int q_ok = true;
    int worst_with_q = 0;
    for (int i = 0; i <= n; ++i) {
      if (sets_for_answer[i].size() == 0) continue;
      cerr << buf(depth) << "Possible answer " << i << " leads to " <<endl;
      ll new_poss_sets = 0;
      FOREACH(jt, sets_for_answer[i]) {
        new_poss_sets |= (ll(1)<<(*jt));
        if (new_poss_sets == poss_sets) {
          // Let's not ask this q; it's stupid anyway
          q_ok = false;
          continue; //break;
        }
        worst_with_q = max(worst_with_q, attempts(depth+1, n, new_poss_sets));
      }
    }
    if (!q_ok) {
      cerr << buf(depth) << "Not ok" << endl;
    }
    else {
      ret = min(ret, 1 + worst_with_q);
      cerr << buf(depth) << "Needs " << 1 + worst_with_q << endl;
    }
  }
  cache[poss_sets] = ret;
  return ret;
}

int a(int n) {
  cerr << "Finding a(" << n << ")" <<endl;
  ll t = ll(1)<<n;
  ll tt = ll(1) << t; assert(tt > 0);
  --tt; assert(tt > 0);
  int ans = n+1;
  for (int i = 0 ; i < t; ++i) {
    ans = min(ans, 1 + attempts(0, n, tt));
  }
  return ans;
}

int main() {
  for (int i = 1; i <= 1; ++i) {
    cout << i << ": " << a(i) << endl;
  }
  return 0;
}
