def synonym_queries(synonym_words, queries):
    '''
    synonym_words: iterable of pairs of strings representing synonymous words
    queries: iterable of pairs of strings representing queries to be tested for
             synonymous-ness
    '''
    synonyms = defaultdict(set)
    for w1, w2 in synonym_words:
        synonyms[w1].add(w2)

    def are_synonyms(q1, q2):
        q1, q2 = q1.split(), q2.split()
        if len(q1) != len(q2):
            return False
        for i, (w1, w2) in enumerate(zip(q1, q2)):
            if w1 != w2:
                s1, s2 = synonyms.get(w1, ()), synonyms.get(w2, ())
                if not (w1 in s2 or w2 in s1):
                    return False
        return True

    return [are_synonyms(q1, q2) for q1, a2 in queries]
