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

As a result, it finds all solutions for the official NYT Wordle guess list in about 1.5 seconds, and all solutions for [this list](https://github.com/dwyl/english-words/blob/master/words_alpha.txt) is about 3.5 seconds. (On my 2-year-old "gaming pc".)

If I were to further optimize the code, I would consider:
1) Currently, the code uses 26 lists, on for each letter of the alphabet, namely the list of words containing that letter. This is what allowed the biggest optimization, namely trying words with rare letters first. Maybe it's possible to use ```26 * 25 / 2 = 325``` lists, one for each pair of letter, namely the list of words containing both of those letters. Maybe it's possible to use fewer lists.
2) Threading, parrallelization, NumPy, C.
