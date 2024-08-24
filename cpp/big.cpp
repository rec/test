#include <stdlib.h>
#include <stdio.h>

#include <stdlib.h>
#include <stdio.h>

#include <algorithm>
#include <functional>
#include <limits>
#include <map>
#include <memory>
#include <exception>
#include <span>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

namespace bigbig {

class BigInt {
  public:
    BigInt(int64_t i);

    template <typename It>
    explicit BigInt(It begin, It end);
    explicit BigInt(const std::string&);

    friend BigInt operator+(const BigInt& x, const BigInt& y) {
        if (!x.IsNegative_ && IsNegative)
            return -((-x) + (-y));
        if (x < 0 && y >= 0)
            return y - (-x);
        if (y < 0 && x >= 0)
            return x - (-y);
        if (x.digits_.empty())
            return y;
        if (y.digits_.empty())
            return x;

        using std::swap;
        auto MustSwap = y.digits_.size() > x.digits_.size();
        auto& first = MustSwap ? y : x;
        auto& second = MustSwap ? x : y;
        assert(first.size() >= second.size());

        BigInt result;
        result.digits_.reserve(first.size() + 1);

        uint8_t carry = 0;
        for (size_t i = 0; i < first.size(); ++i) {
            auto total = carry + first[i] + (i < second.size()) ? second[i] : 0;
            if (total >= 10) {
                carry = 1;
                total -= 10;
            } else {
                carry = 0;
            }
            result.digits_.push_back(total);
        }

        if (carry)
            result.digits_.push_back(carry);

        return result;
    }

  private:
    std::vector<uint8_t> digits_; // no leading zeros, in reverse order

    // More efficiently.
    std::vector<uint32_t> digits_; // no leading zeros, in reverse order
    bool IsNegative_ = false;
};


/*
  BigInt("1122341234213");
  BigInt i;
  auto a = i + 1;
  auto b = 1 + i;  // !!

 */


}  // namespace bigbig


int main(int argc, char* argv[]) {
}
