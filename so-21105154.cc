/*
  http://stackoverflow.com/questions/21105154/n-choose-k-k-n-k-2n-etc-recursion-within-recursion

  All partitions of a set of N elements into parts of size K each.

  Each partition is generated in "canonical form": write each part in increasing
  order, and then write these parts themselves in increasing order of their
  smallest element.
*/

#include <iostream>
#include <vector>
#include <cassert>

// We visualize generating a partition as a process of dropping balls numbered
// 1 to N, one by one, into N/K bins. So automatically each bin/part is sorted.
// We just make sure we don't skip an empty bin before populating the next one.
class PartitionGenerator {
 public:
  PartitionGenerator(int N, int K, bool print) : N(N), K(K), print_(print) {
    assert(N % K == 0);
    partition_.resize(N / K);
    num_partitions_found_ = 0;
  }

  // Recursive function takes a state in which balls 1 to n-1 have been placed
  // in bins, and extends the state by placing ball n in all possible bins.
  void GeneratePartitions(int n = 1) {
    if (n == N + 1) {
      OutputPartition();
      return;
    }
    for (int i = 0; i < N / K; ++i) {
      // Cannot place into a full bin
      if (partition_[i].size() == K) continue;
      // Cannot skip an empty bin
      if (i > 0 && partition_[i - 1].empty()) break;

      partition_[i].push_back(n);
      GeneratePartitions(n + 1);
      partition_[i].pop_back();
    }
  }

  int NumPartitionsFound() { return num_partitions_found_; }

 private:
  void OutputPartition() {
    assert(partition_.size() == N / K);
    ++num_partitions_found_;
    if (!print_) return;
    for (int i = 0; i < N / K; ++i) {
      assert(partition_[i].size() == K);
      std::cout << "{";
      for (int j = 0; j < K; ++j) {
        std::cout << partition_[i][j] << (j == K - 1 ? "}" : ", ");
      }
      if (i < N / K - 1) std::cout << ", ";
    }
    std::cout << std::endl;
  }

  std::vector<std::vector<int> > partition_;
  int N, K;
  int num_partitions_found_;
  bool print_;
};

int main() {
  int N, K;
  std::cin >> N >> K;
  PartitionGenerator g(N, K, N < 10);
  g.GeneratePartitions();
  std::cout << g.NumPartitionsFound() << " found" << std::endl;
}
