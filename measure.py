import solve
import timeit

def measure_duration(solver, wordlist_path, number=None):
    return timeit.timeit(lambda: solver(wordlist_path), number=number)

if __name__ == '__main__':
    for run in range(3):
        duration = measure_duration(solve.solve, 'words.txt', 3)
        print(duration)
