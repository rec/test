#include <torch/torch.h>
#include <iostream>
#include <ATen/ops/unbind_copy.h>
#include <ATen/ops/unbind_copy_ops.h>

const auto size = 2;

int main() {
  torch::Tensor tensor = torch::ones(3);
  std::cout << "tensor" << tensor << std::endl;

  auto t1 = torch::zeros(size), t2 = torch::zeros(size), t3 = torch::zeros(size);

  at::TensorList out{t1, t2, t3};
  if (false) {
      at::unbind_copy_out(out, tensor);
  } else {
      at::_ops::unbind_copy_int_out::call(tensor, 0, out);
  }
  std::cout << "ts " << t1 << t2 << t3 << std::endl;
  std::cout << "size " << t1.sizes() << std::endl;
}
