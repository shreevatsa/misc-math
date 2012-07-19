//All permutations of ".....CCCCCC". For correcting this wrong answer:
//http://math.stackexchange.com/questions/36851/how-many-permutations-of-a-word-do-not-contain-consecutive-vowels/36860#36860
#include <iostream>
using namespace std;

int main() {
  string s = ".....CCCCCC";
  do {
    bool ok = true;
    for(int i=1; i<s.length(); ++i)
      if(s[i]=='.' and s[i-1]=='.') {
        ok = false;
        break;
      }
    if(ok) cout<<s<<endl;
  } while(next_permutation(s.begin(),s.end()));
  return 0;
}
