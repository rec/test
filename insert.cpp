    using IntVec = std::vector<int>;
    using IntSet = std::unsorted_map<int>;

    IntVec deduped(const IntVec& src) {
        IntVec result;
        IntSet seen;

        for (auto i : src) {
            auto it = seen.find(i);
            if (it == seen.end()) {
                result.push_back(i);
                seen.insert(it, i);
            }
        }
    }
