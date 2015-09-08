from collections import defaultdict
import sys

total_calls = 0


def unpack(sudoku_str):
    return tuple(
        tuple(char if char.isdigit() else ' ' for char in line[:9])
        for line in sudoku_str.splitlines()[:9]
    )

def pack(sudoku_state):
    return '\n'.join(''.join(row) for row in sudoku_state)

def apply_choice(sudoku_state, row, col, digit):
    return tuple(
        tuple(
            digit if (r, c) == (row, col) else state_digit
            for c, state_digit in enumerate(state_row)
        )
        for r, state_row in enumerate(sudoku_state)
    )

def counts(sudoku_state):
    rows, cols, squares = {}, {}, {}

    for r, row in enumerate(sudoku_state):
        rows[r] = defaultdict(int)
        for c, digit in enumerate(row):
            if not digit.isdigit():
                digit = ' '

            square = 3 * (r // 3) + (c // 3)
            cols.setdefault(c, defaultdict(int))
            squares.setdefault(square, defaultdict(int))

            rows[r][digit] += 1
            cols[c][digit] += 1
            squares[square][digit] += 1

    return rows, cols, squares

def dependencies(rows, cols, squares):
    return dict(
        ((r, c),
         frozenset('123456789') -
         set(rows[r]) - set(cols[c]) - set(squares[3 * (r // 3) + (c // 3)]))
        for r in xrange(9) for c in xrange(9)
    )

def is_consistent(sudoku_state, choices):
    return not any(not S and not sudoku_state[r][c].isdigit()
                   for (r, c), S in choices.iteritems())

def solve(sudoku_state):
    global total_calls
    total_calls += 1

    rows, cols, squares = counts(sudoku_state)

    open_counts = dependencies(rows, cols, squares)
    if not is_consistent(sudoku_state, open_counts):
        return
    if all(not x for x in open_counts.itervalues()):
        return sudoku_state

    score, choices, (r, c) = min(
        (len(choices), choices, (r, c))
        for (r, c), choices in open_counts.iteritems()
        if choices and not sudoku_state[r][c].isdigit()
    )

    for digit in choices:
        result = solve(apply_choice(sudoku_state, r, c, digit))

        if result is not None:
            return result


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        sudoku_str = f.read()
        solution = solve(unpack(sudoku_str))
        print pack(solution)
        print
        print total_calls, 'calls'
