#include <torch/torch.h>
#include <iostream>
#include <ATen/ops/unbind_copy.h>
#include <ATen/ops/unbind_copy_ops.h>

int main() {
  torch::Tensor tensor = torch::eye(3);
  std::cout << tensor << std::endl;

  auto t1 = torch::eye(0), t2 = torch::eye(0), t3 = torch::eye(0);

  at::TensorList out{t1, t2, t3};
  if (false) {
      at::unbind_copy_out(out, tensor);
  } else {
      at::_ops::unbind_copy_int_out::call(tensor, 0, out);
  }
}
