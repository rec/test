#include <torch/torch.h>
#include <iostream>
#include <ATen/ops/unbind_copy.h>

int main() {
  torch::Tensor tensor = torch::eye(3);
  std::cout << tensor << std::endl;
}
