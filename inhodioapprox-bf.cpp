/*
  Find powers of 2 that start with 2011, with brute force.
  http://math.stackexchange.com/questions/46100/fractional-part-of-b-log-a/
 */

#include <iostream>
using namespace std;

const int MAX = 1000000;
int d[MAX];

int main() {
  d[0] = 1; //Start with 2^0
  int l = 1;
  int cnt = 0;
  for(int n=1; n<MAX; ++n) {
    //Find 2^n
    int carry = 0;
    for(int i=0; i<l; ++i) {
      d[i] = d[i]*2 + carry;
      if(d[i]<10) carry = 0;
      else {
        carry = d[i]/10;
        d[i] %= 10;
      }
    }
    if(carry) {
      d[l] = carry;
      ++l;
    }
    // cerr<<n<<": ";
    // for(int i=l-1; i>=0; --i) cerr<<d[i]; cerr<<endl;

    const int wantlen = 4;
    int want[wantlen] = {2, 0, 1, 1};
    bool ok = (l>=wantlen);
    for(int i=0; i<wantlen; ++i) if(d[l-1-i]!=want[i]) ok=false;
    if(ok) {
      cout<<n<<endl;
      ++cnt;
    }
    if(n%10000==0) cout<<cnt<<" out of "<<n<<endl;
  }
  return 0;
}
