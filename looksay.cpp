/*
The look-and-say sequence. Can we go backwards?

For testing some heuristic (which turns out to be wrong).
*/

#include <algorithm>
#include <iostream>
#include <vector>
#include <map>
#include <cassert>
using namespace std;

#define FCO(i,a,b) for(int i=a,_b=b;i<_b;++i)
#define FCC(i,a,b) for(int i=a,_b=b;i<=_b;++i)
#define FOR(i,n) FCO(i,0,n)
#define SZ(s) signed(s.size())
#define FOZ(i,s) FOR(i,SZ(s))

#define ALL(s) s.begin(),s.end()
#define LET(a,b) typeof(b) a=b
#define FOREACH(it,v) for(LET(it,v.begin());it!=v.end();++it)
#define MP make_pair
#define PB push_back

typedef vector<int> VI;
typedef long long ll;

VI next(VI v) {
  map<int,int> cnt; FOZ(i,v) ++cnt[v[i]];
  VI ret;
  FOREACH(it, cnt) {
    ret.PB(it->second);
    if(it->second > 9) {
      throw it->second;
    }
    ret.PB(it->first);
  }
  return ret;
}

VI digits(ll n) {
  VI ret;
  while(n) {
    ret.PB(n%10);
    if(n%10==0) throw 0;
    n/=10;
  }
  reverse(ALL(ret));
  return ret;
}

VI parent(VI v) {
  if(SZ(v)%2) {
    //assert(SZ(v)==1);
    return v;
  }
  VI ret;
  int N = SZ(v)/2;
  FOR(i,N) {
    FOR(j,v[2*i]) ret.PB(v[2*i+1]);
  }
  sort(ALL(ret));
  return ret;
}

map<VI, int> first;

int main() {
  FCO(n, 1, 100000) {
    cerr<<"Starting at "<<n<<endl;

    VI v;
    try {
      v = digits(n);
    }
    catch(int e) {
      continue;
    }
    for(;;) {
      if(first.count(v)) {
        assert(first[v]<=n);
        break;
      }
      FOZ(i,v) cout<<v[i]<<" "; cerr<<"\t\t: \t";
      first[v] = n;

      if(SZ(v)%2) { ; }
      else {
        VI w=v;
        for(;;) {
          VI x = parent(w);
          FOZ(i,x) cerr<<x[i]; cerr<<" ";
          if(x==w or SZ(x)>SZ(w) or SZ(x)==SZ(w) and x>w) break;
          if(first.count(x) and first[x]!=n) {
            // cerr<<"Parent of { ";
            // FOZ(i,w) cerr<<w[i]<<" ";
            // cerr<<"} is { ";
            // FOZ(i,x) cerr<<w[i]<<" ";
            cerr<<"} but firsts are "<<first[w]<<" and "<<first[x]<<" respectively"<<endl;
          }
          w = x;
        }
      }
      cerr<<endl;

      try {
        v = next(v);
      }
      catch (int e) {
        break;
      }
    }
  }
}
