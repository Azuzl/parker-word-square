# parker-word-square

This Python script lets you create squares like this one:
```
WAQFS
JUMPY
VOZHD
BLING
TRECK
```
This square is special because:
1) Each of the 5 rows of the square is a 5-letter word.
2) The words have no letters in common with each other. i.e. they use 25 unique letters.
3) Each word is a valid [Wordle](https://www.nytimes.com/games/wordle/index.html) guess.

Given a list of words, such as the one in (3), this script produces sets of five 5-letter words satisfying properties (1) and (2).

I got this idea from [this video](https://youtu.be/_-AfhLQfb6w) by Matt Parker, who in turn got it from a listener of his podcast.

## Where's the word list?

The script needs a file called `words.txt` to get its words from. I don't know what license if any applies to the official NYT Wordle guess list, so I have not included it in this GNU GPLv3 project. You can download it here [here](https://github.com/tabatkins/wordle-list), and manually put it in the same folder as `solve.py`.

## Performance

This script uses some optimizations to get good performance despite it being Python. This includes:
1) Discarding words that cannot occur in any solution, e.g. because they have repeat letters or are the wrong length.
2) Avoiding repeated work by merging branches of the search tree when they have the same leaf.
3) When refining the search tree, prioritizing words with uncommon letters, so early branching is reduced.
4) Representing words (or more precisely, equivalence classes of words under the anagram relation) as integers, each bit representing a letter from the alphabet.

As a result, it finds all solutions for the official NYT Wordle guess list in about 1.5 seconds, and all solutions for [this list](https://github.com/dwyl/english-words/blob/master/words_alpha.txt) in about 3.5 seconds. (On my 2-year-old "gaming pc".)

If I were to further optimize the code, I would consider:
1) Use a completely different technique. The way we're representing words as integers / bits makes both [linear programming](https://en.wikipedia.org/wiki/Linear_programming) and [SAT solvers](https://en.wikipedia.org/wiki/SAT_solver) seem natural approaches.
2) Currently, the code uses 26 lists, on for each letter of the alphabet, namely the list of words containing that letter. This is what allowed the biggest optimization, namely trying words with rare letters first. Maybe it's possible to use ```26 * 25 / 2 = 325``` lists, one for each pair of letter, namely the list of words containing both of those letters. How would you use this information?
3) Threading, parrallelization, NumPy, C.

## Computational complexity

In order to talk about the computational complexity of this algorithm, as well as other algorithms solving the same problem, let's introduce some names:
- Let $n$ be the number of words in the `words.txt`.
- Let $w$ be the length we want the words to be. Let's assume every word in `words.txt` is already $w$ letters long.
- Let $h$ be the number of words we want each solution to be. (In `solve.py` I assume that $w = h = 5$ because we wanted a 5 by 5 square, but in general we may want any rectangular shape.)
- Let $s$ be the size of the alphabet.
- Let $t = t(n, w, h, s)$ be the worst-case time it takes some particular algorithm to solve the problem given the values of $n, w, h$ and $s$. 
- Let's assume we only need our algorithm to print out 1 valid word rectangle (of width $w$ and height $h$) if one exists.

Note that the length of the input is asymptotically equal to $nw\log_2s$, and the length of the output is asymptotically equal to $wh\log_2s$, so a simple lower bound for the complexity of the problem is $$t = \Omega((n+h)w\log_2s),$$ or if $w, h$ and $s$ are constant (e.g. $w=h=5$ and $s=26$), the lower bound is just $$t = \Omega(n).$$

Perhaps surprisingly, assuming $w, h$ and $s$ are constant, even brute force algorithms may have complexity $\Omega(n)$, meeting the lower bound. This is because there's only $s^w$ possible different words, which would also be constant. So if you first filter out duplicates, which you can do in $\Omega(n)$ time, the size of the problem becomes bounded by a constant, and can be solved in constant time by e.g. a giant lookup table.

However, in practice, brute force algorithms have performance that looks like $t \sim n^h$, at least for relatively small values of $n$. This is because such algorithms consider every way to pick $h$ words from a list of $n$ different words, e.g. using $h$ nested loops of length $n$. My algorithm ends up working quite similarly to brute-force algorithms in this sense. For example, if $w = h = 5$ but $s=24,$ and every letter in the alphabet was about equally common, then my algorithm would check a large chunk of those $n^k$ combinations, but never find a solution (because there is none). However, it still performs faster in practice, because it branches on words containing uncommon letters first, of which there are much fewer than $n$.
