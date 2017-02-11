/*
  Problem: You are given k, and a list (set) L of size 2k.

  A pair-partition (aka 1-factor aka perfect matching) of L is
  a partition of L into unordered pairs (sets of size 2).
  That is, it is a set of k pairs, whose disjoint union is L.

  Let S denote the set of all pairs of elements of L.
  Note that S contains (2k choose 2) = k(2k-1) pairs.

  A 1-factorization is a partition of S into (2k-1) sets,
  each of which (having k pairs) is itself a pair-partition of L.

  Enumerate all 1-factorizations.

  In other words, enumerate all ways of partitioning the set of pairs of
  elements of L, such that the disjoint union of the pairs in each part is L.
*/

#include <iostream>
#include <vector>
#include <utility>
#include <map>
#include <bitset>
#include <cassert>
#include <iomanip>
using std::vector;
using std::pair;
using std::make_pair;
using std::map;

/*
  Algorithm:

  - First, generate all factors (pair-partitions), and represent each as a
    bitstring. There are (2k)!/(k!2^k) of them. For k = 0, 1, 2, 3, 4, 5, this
    number is 1, 1, 3, 15, 105, 945.

    This part can afford to be slow and inefficient.
*/

vector<vector<pair<char,char>>> factors(const vector<char>& list) {
  vector<vector<pair<char,char>>> ret;
  if (list.size() == 0) {
    vector<pair<char,char>> factor;
    ret.push_back(factor);
    return ret;
  }
  // Decide on the first part: it is (list[0], list[i]) for some i >= 1
  for (unsigned i = 1; i < list.size(); ++i) {
    pair<char, char> p = make_pair(list[0], list[i]);
    vector<char> rest;
    for (unsigned j = 1; j < list.size(); ++j) {
      if (j != i) rest.push_back(list[j]);
    }
    auto factors_of_rest = factors(rest);
    for (const auto& factor_of_rest : factors_of_rest) {
      vector<pair<char,char>> factor;
      factor.push_back(p);
      for (pair<char,char> pare : factor_of_rest) {
        factor.push_back(pare);
      }
      ret.push_back(factor);
    }
  }
  return ret;
}

/*
  For the next part, we assume k <= 5, as otherwise there are too many
  1-factorizations to enumerate on a computer.

  The size of S = k(2k-1) <= 45.

  As 45 < 64, we can represent any subset of S (in particular, any
  pair-partition aka 1-factor, henceforth "factor") by a 64-bit word. (Elements
  of S, which are pairs, correspond to bit positions.)

  Note that any set of disjoint (2k-1) factors forms a 1-factorization. This is
  because, if we have (2k-1) disjoint sets of size k each, their union
  necessarily has size k(2k-1). So they will cover S.
*/

map<pair<char,char>, int> map_pairs_to_positions(const vector<char>& list) {
  map<pair<char,char>, int> ret;
  int count = 0;
  for (unsigned i = 0; i < list.size(); ++i)
    for (unsigned j = i + 1; j < list.size(); ++j)
      ret[make_pair(list[i], list[j])] = count++;
  return ret;
}

typedef long long pairset;

// pairset

int main() {
  vector<char> list = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'};

  map<pair<char,char>, int> position_for_pair = map_pairs_to_positions(list);
  for (const auto& key : position_for_pair) {
    std::cout << key.first.first << "-" << key.first.second << " -> " << key.second << std::endl;
  }

  vector<vector<pair<char,char>>> fs = factors(list);
  const short num_partitions = fs.size();
  std::cout << "The number of 1-factors (pair-partitions / perfect matchings) is " << num_partitions << ". They are: " << std::endl;

  // We can denote each 1-factor by a pairset (a bit string).
  pairset d[num_partitions];

  for (unsigned i = 0; i < fs.size(); ++i) {
    std::cout << std::setw(3) << i << ": ";
    auto factor = fs[i];
    pairset tmp = 0;
    for (const auto& pare :factor) {
      std::cout << pare.first << "-" << pare.second << "(" << std::setw(2) << position_for_pair[pare] << ") ";
      tmp |= (pairset(1) << position_for_pair[pare]);
    }
    d[i] = tmp;
    std::cout << "which can be represented as " << std::setw(14) << d[i] << " = " << std::bitset<64>(d[i]) << std::endl;
  }

  /*
  - Now, we just need to find all sets of 2k-1 factors that are pairwise
    disjoint. We do this with backtracking, using the bitstring representation
    to efficiently determine disjointness.

  Backtracking: We follow TAOCP 7.2.2 (Pre-fascicle 5B) "Algorithm B".
  In its terminology (its k not to be confused with our k),
  - each xk comes from the domain Dk = D = <set of all factors>
  - Property P_l(x1, x2, ..., xl) = [<the numbers x1, ..., xl> are disjoint]
    If we already know that the previous one holds,
    and we have prev_union = (x[1] | x[2] | ... x[l-1]) stored,
    then we can test this efficiently by verifying that x[l] & prev_union is 0.
  */

  const short max_partition_index = num_partitions - 1;
  const short factorization_length = list.size() - 1;
  short x_index[factorization_length + 1]; x_index[0] = -1;
  pairset x[factorization_length + 1];
  pairset x_union[factorization_length + 1]; x_union[0] = 0;

  int count = 0; // Enough for k=5: count 1225566720
 // b1:
  short l = 1;
 b2:
  // Beginning of level l
  if (l > factorization_length) {
    // We have a solution; do something with it.
    // std::cout << "Found a factorization" << std::endl;
    ++count;
    // And then
    goto b5;
  }
  x_index[l] = x_index[l - 1] + 1;
  // std::cout << "For level " << l - 1 << " we were using index " << x_index[l - 1] << " so for level " << l << " trying with " << x_index[l] << std::flush;
  // assert(0 <= x_index[l]);
  // assert(x_index[l] < num_partitions);
  x[l] = d[x_index[l]];
  // std::cout << " (value " << x[l] << ")" << std::endl;
 b3:
  // Try current value of [l]
  if (l == 1) {
    std::cout << "Trying value " << std::setw(14) << x[l] << " for position " << l << " (have found " << std::setw(10) << count << " so far)" << std::endl;
  }
  if ((x[l] & x_union[l - 1]) == 0 && !(x_index[l] == max_partition_index and l < factorization_length)) {
    x_union[l] = x_union[l - 1] | x[l];
    ++l;
    goto b2;
  }
 b4:
  // Try next option for x[l], if possible
  if (x_index[l] < max_partition_index) {
    ++x_index[l];
    x[l] = d[x_index[l]];
    goto b3;
  }
 b5:
  // Backtrack: We've run out of options for x[l]. So we need to try next values of x[l-1].
  --l;
  if (l > 0) {
    goto b4;
  }

  std::cout << "The backtracking gave " << count << " factorizations" << std::endl;
  return 0;
}
