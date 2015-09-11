from collections import defaultdict
import sys

total_calls = 0


def unpack(sudoku_str):
    return tuple(
        (r, c, 3 * (r // 3) + (c // 3), char)
        for r, line in enumerate(sudoku_str.splitlines()[:9])
        for c, char in enumerate(line[:9])
        if char.isdigit()
    )

def pack(sudoku_state):
    state = {
        (r, c): digit
        for r, c, square, digit in sudoku_state
    }

    return '\n'.join(
        ''.join(state.get((r, c), ' ') for c in xrange(9))
        for r in xrange(9)
    )

def counts(sudoku_state):
    rows, cols, squares = {}, {}, {}

    for r, c, square, digit in sudoku_state:
        rows.setdefault(r, defaultdict(int))
        cols.setdefault(c, defaultdict(int))
        squares.setdefault(square, defaultdict(int))

        rows[r][digit] += 1
        cols[c][digit] += 1
        squares[square][digit] += 1

    return rows, cols, squares

def dependencies(sudoku_state, rows, cols, squares):
    deps = {
        (r, c): (frozenset('123456789')
                 - set(rows.get(r, ()))
                 - set(cols.get(c, ()))
                 - set(squares.get(3 * (r // 3) + (c // 3), ())))
        for r in xrange(9) for c in xrange(9)
    }

    for r, c, square, digit in sudoku_state:
        del deps[(r, c)]

    return deps

def is_consistent(sudoku_state, choices):
    return all(S for (r, c), S in choices.iteritems())

def solve(sudoku_state):
    global total_calls
    total_calls += 1

    rows, cols, squares = counts(sudoku_state)

    open_counts = dependencies(sudoku_state, rows, cols, squares)
    if not is_consistent(sudoku_state, open_counts):
        return
    if not open_counts:
        return sudoku_state

    score, choices, (r, c) = min(
        (len(choices), choices, (r, c))
        for (r, c), choices in open_counts.iteritems()
    )

    for digit in choices:
        result = solve(sudoku_state + ((r, c, 3 * (r // 3) + (c // 3), digit),))

        if result is not None:
            return result


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        sudoku_str = f.read()
        solution = solve(unpack(sudoku_str))
        print pack(solution)
        print
        print total_calls, 'calls'
