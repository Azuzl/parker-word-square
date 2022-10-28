# Running this script will read the words in words.txt,
# find every collection of five 5-letter words, and
# print these collections.

from collections import defaultdict

# Wrapping the solver in a function so it can be called from measure.py
def solve(wordlist_path):
    # This loads the vocabulary we're allowed to use.
    with open(r'words.txt', 'r') as f:
        words = f.read().split()

    # We're only allowed to use each letter once, so all our
    # words can only use each letter once. The words must also
    # be exactly 5 letters long.
    def can_be_used(word):
        return len(word) == len(set(word)) == 5

    words = list(filter(can_be_used, words))

    # We'll be treating the words as integers, because this is
    # faster than manipulating strings or sets of characters.
    # The correspondence between words and ints is as such:
    # a -> 1, b -> 10, c -> 100, d -> 1000, etc. (in binary)
    # The int of a word is the sum of the ints of its letters:
    # decaf = d+e+c+a+f -> 1000+10000+100+1+100000 = 111101
    # Note that 'faced' has the same letters, so its int is
    # the same. This is good, because anagrams are
    # interchangeable in this problem.
    def word_to_int(word):
        return sum(1<<(ord(c)-97) for c in word) # 97 = ord('a')
    # After we're done, we'll turn the numbers back into words.
    # We can recover the letters that were in the word by
    # looking at the bits of the int. Later, using these letters,
    # we'll be able to find all anagrams of the word.
    def int_to_letters(n):
        return ''.join(chr(i+97) for i in range(26) if n>>i & 1)

    # A list of all our int-encoded words.
    ints = sorted(set(map(word_to_int, words)))

    # For each letter, find `has[letter]`, the list of words that
    # contain that letter. This way we don't have to look through
    # the entire word list just to find a word with an 'X' in it.
    has = [[n for n in ints if n>>i & 1] for i in range(26)]

    # Count how many times each letter occurs in the word list in
    # total. That way we can start with the least common letters.
    counts = list(map(len, has))

    # Using `counts` we find the list of int-encodings for every
    # letter, when those letters are sorted from rare to common.
    alphabet = sorted(range(26), key=lambda letter:counts[letter])
    # To get check that this list is correct, uncomment this:
    # print([int_to_word(1<<i) for i in alphabet])
    # It should print a list, starting with rare letters like 'q'
    # and 'j', and ending with common ones, like 'a' and 'e'.

    # This list will hold the solutions. If there are no
    # solutions, it will be empty. The format of the solutions
    # is a bit weird, and I'm not sure "solution" is the best
    # word for it. An example solution is 12345678, meaning
    # "There's a collection of 5 words whose int-encodings
    #  add up to 12345678."
    solutions = []
    # That's not enough information to recover the actual
    # list of 5 words, though, so I keep track of the way
    # we build the int in the `deconstructions` dict.
    # If, for example deconstructions[12345678] contains
    # the pair (12110400, 235278), that means there's a
    # collection of (in this case four) words who ints
    # add up to 12110400, and another word whose int is
    # 235278. Applying this data recursively, we'll be able
    # to find all ways of construct all ways of building
    # the int 12345678 out of int-encodings of our words.
    deconstructions = defaultdict(list)

    # The main loop.
    # The basic idea is to start by trying to include the
    # least common letters in the solution. This keeps
    # early branching to a minimum.
    # We start with a single candidate (partial solution)
    # which we represent as (0, 0).
    # The first zero is the int-encoding of the empty string
    # and the second zero is the number of letters we've
    # skipped. This means:
    #  - Our search space is all strings that contain
    #    the empty string (i.e. all of them for now).
    #  - In this search space, we skip at least 0 of
    #    the letters in our alphabet.
    # Of course, we cannot skip more than 1 letter, because
    # our solution will be 25 letter, and there are only 26
    # letters in the alphabet. So if the `skipped` number
    # ever exceeds 1, we can stop exploring that candidate.
    # During each iteration, we refine our search space
    # by splitting it off into different possibilities--
    # new, more specific candidates--by adding words to the
    # candidates, or skipping letters.
    # You may think of "candidate" and "part of the search space"
    # interchangeably.
    # If we find a solution, we add it to the solutions list
    # and stop exploring that candidate, because there are
    # no solutions that are strict supersets of other solutions.
    candidates = [(0, 0)]
    for i in alphabet: # i is the int-encoding of a letter
        # The next, more refined part the search space
        new_candidates = []
        for cand, skipped in candidates:
            # Check if a solution has been found
            if cand.bit_count() == 25:
                solutions.append(cand)
                # Continue = stop searching in this candidate
                continue
            # Check if we've skipped too many letters
            if skipped > 26 - 25:
                continue
            # Sometimes, the letter is already in our candidate.
            # If so, just carry it over to the next search space.
            if cand>>i & 1:
                new_candidates.append((cand, skipped))
                continue
            # If the letter is not in the candidate, one option
            # is to just skip it.
            new_candidates.append((cand, skipped+1))
            # But we can also find a word that has the letter in it,
            # and add that word to the candidate.
            for other in has[i]:
                # Such a word must not share letters with our candidate
                if (cand & other):
                    continue
                new_cand = cand | other
                # Here were using `deconstructions` to simultaneously
                # keep track of whether we've seen this candidate already
                # (if so, we don't want to search it again), and to keep
                # track of the different ways we've built the candidate.
                if new_cand not in deconstructions:
                    new_candidates.append((new_cand, skipped))
                # Reminder: the point of `deconstructions` is so we know
                # how to build our solution when we've found it.
                deconstructions[new_cand].append((cand, other))
        candidates = new_candidates
        # To diagnose which loops take the longest:
        # print(len(candidates), set(bin(cand).count('1') for cand, _ in candidates))

    # Find `sources[n]`, the list of words in our word list
    # which have n as their int-encoding.
    sources = defaultdict(list)
    for word in words:
        if len(word) == len(set(word)) == 5:
            sources[word_to_int(word)].append(word)

    # We can now find every way to deconstruct a solution
    # or candidate into words. We use `deconstructions`
    # to find every possible way to deconstruct into ints,
    # and then `sources` to find every possible way to get
    # those ints from words.
    def deconstruct(s):
        if s.bit_count() == 5:
            for src in sources[s]:
                yield [src]
            return
        for left, right in deconstructions[s]:
            for left_d in deconstruct(left):
                for right_d in deconstruct(right):
                    yield left_d + right_d

    # Return all the ways to build of all the solutions
    solutions = [
        ' '.join(dec)
        for a in solutions
        for dec in deconstruct(a)
    ]
    solutions.sort()
    return solutions

if __name__ == '__main__':
    solutions = solve('words.txt')
    for sol in solutions:
        print(sol)
