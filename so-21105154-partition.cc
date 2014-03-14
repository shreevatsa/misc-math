/*
  You want all **partitions** of a set of N elements into parts of size K each.

  To avoid overgeneration, let's decide on a "canonical form" for each
  partition: let's say it is to write each part in increasing order, and then
  write these parts themselves in increasing order of their smallest element.

  Now you can visualize generation of a partition as a process of dropping balls
  numbered 1 to N, one by one, into N/K bins. The constraint that each bin
  (part) must be in increasing order is then automatically satisfied (of course
  you should "read" each bin in the order in which elements were inserted), and
  the other constraint is satisfied if we make sure we don't skip an empty bin
  before populating the next one.

  Now to translate that into code.

  In general, when generating structures recursively (or coding any recursive
  algorithm), your recursive function is given a particular "state", and tries
  each incremental way of extending that state. Between different options, just
  make sure to bring the state back to what you were given.
 */

#include <iostream>
#include <vector>
#include <cassert>

std::vector< std::vector<int> > partition;
int N, K;
int num_partitions_found = 0;

void OutputPartition();

// Our recursive function takes a state in which balls up to n-1 have been
// placed in bins, and extends the state by placing ball n in all possible
// places.
void GeneratePartitions(int n) {
  // When we've placed all N elements, stop and output.
  if (n == N + 1) {
    OutputPartition();
    return;
  }
  // Place ball numbered n into each allowed bin.
  for (int i = 0; i < N / K; ++i) {
    // Cannot place into a full bin
    if (partition[i].size() == K) continue;
    // Cannot skip an empty bin
    if (i > 0 && partition[i-1].empty()) break;
    // Place the ball here: extending the state
    partition[i].push_back(n);
    // The recursive call
    GeneratePartitions(n + 1);
    // Make sure you restore state after each recursive call!
    partition[i].pop_back();
  }
}

void OutputPartition() {
  assert(partition.size() == N/K);
  ++num_partitions_found;
  for (int i = 0; i < N/K; ++i) {
    assert(partition[i].size() == K);
    std::cout << "{";
    for (int j = 0; j < K; ++j) {
      std::cout << partition[i][j] << (j == K - 1 ? "}" : ", ");
    }
    if (i < N/K - 1) std::cout << ", ";
  }
  std::cout << std::endl;
}

int main() {
  std::cin >> N >> K;
  assert(N % K == 0);
  partition.resize(N / K);
  GeneratePartitions(1);
  std::cout << num_partitions_found << " found" << std::endl;
}
