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

The script needs a file called `words.txt` to get its words from. I don't know what license if any applies to the official NYT Wordle guess list, so I have not included it in this GNU GPLv3 project. It is however available [here](https://github.com/tabatkins/wordle-list).
