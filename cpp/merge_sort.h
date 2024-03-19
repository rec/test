#pragma once

#include <stdlib.h>
#include <stdio.h>

#include <limits>
#include <map>
#include <stdexcept>
#include <span>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

namespace merge_sort {

template <typename T>
void merge_sort(T& source);

namespace detail {

template <typename T>
void merge_sort(T& source, T& target, size_t begin, size_t end) {
    if (end - begin <= 0)
        return;

    auto middle = (begin + end) / 2;  // TODO: handle overflow

    merge_sort(target, source, begin, middle);
    merge_sort(target, source, middle, end);

    auto left = begin, right = middle;
    for (auto i = begin; i <= end; ++i) {
        if (left < middle && (right >= end || source[left] <= source[right])) {
            target[i] = source[left++];
        } else {
            target[i] = source[right++];
        }
    }
}

} // detail

template <typename T>
void merge_sort(T& v) {
    auto work = v;
    detail::merge_sort(work, v, 0, v.size());
}

}  // merge_sort
