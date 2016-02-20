import sys

total_calls = 0


class HeaderRoot(object):
    __slots__ = ('left', 'right', 'count')

    def __init__(self):
        self.left = self
        self.right = self

        self.count = 0

    def __iter__(self):
        node = self.right
        while node != self:
            yield node
            node = node.right


class Header(object):
    __slots__ = ('left', 'right', 'up', 'down', 'header', 'count')

    def __init__(self, header):
        self.left = self
        self.right = self
        self.up = self
        self.down = self

        self.header = header
        self.count = 0

    def __iter__(self):
        node = self.down
        while node != self:
            yield node
            node = node.down

    def cover(self):
        self.right.left, self.left.right = self.left, self.right
        for node in self:
            for cons in node:
                cons.up.down, cons.down.up = cons.down, cons.up
                cons.column.count -= 1

    def uncover(self):
        for node in reversed(list(self)):
            for cons in reversed(list(node)):
                cons.column.count += 1
                cons.down.up, cons.up.down = cons, cons
        self.right.left, self.left.right = self, self


class Constraint(object):
    __slots__ = ('left', 'right', 'up', 'down', 'column')

    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self

        self.column = None

    def __iter__(self):
        node = self.right
        while node != self:
            yield node
            node = node.right


def unpack(sudoku_str):
    root = HeaderRoot()
    solution = []
    solved_constraints = set()

    for r, line in enumerate(sudoku_str.splitlines()[:9]):
        for c, char in enumerate(line[:9]):
            box = 3 * (r // 3) + (c // 3)

            if char.isdigit():
                value = int(char)
                solution.append((r, c, value))
                solved_constraints |= {
                    ('square', r, c), ('row', value, r),
                    ('column', value, c), ('box', value, box)
                }

    for r in xrange(9):
        for c in xrange(9):
            box = 3 * (r // 3) + (c // 3)

            for value in xrange(1, 10):
                constraints = {
                    ('square', r, c), ('row', value, r),
                    ('column', value, c), ('box', value, box)
                }

                if any(cons in solved_constraints for cons in constraints):
                    continue

                columns = [node for node in root if node.header in constraints]
                constraints -= {node.header for node in columns}
                for header in constraints:
                    column = Header(header)
                    column.left, column.right = root.left, root
                    root.left.right, root.left = column, column
                    root.count += 1
                    columns.append(column)

                for column in columns:
                    cons = Constraint()
                    cons.column = column
                    cons.up, cons.down = column.up, column
                    column.up.down, column.up = cons, cons
                    column.count += 1

                    first = columns[0].up
                    cons.left, cons.right = first.left, first
                    first.left.right, first.left = cons, cons

    return root, solution


def pack(state):
    state = {(r, c): value for r, c, value in state}

    return '\n'.join(
        ''.join(str(state.get((r, c), ' ')) for c in xrange(9))
        for r in xrange(9)
    )


def solve(root, solution):
    global total_calls
    total_calls += 1

    if root.right == root:
        return solution

    count, column = min((c.count, c) for c in root)
    column.cover()

    for node in column:
        for cons in node:
            if cons.column.header[0] != 'square':
                value = cons.column.header[1]
            if cons.column.header[0] == 'square':
                r, c = cons.column.header[1:]
            if cons.column.header[0] == 'row':
                r = cons.column.header[2]
            if cons.column.header[0] == 'column':
                c = cons.column.header[2]

            cons.column.cover()
        solution.append((r, c, value))

        result = solve(root, solution)
        if result is not None:
            return solution

        for cons in reversed(list(node)):
            cons.column.uncover()

    column.uncover()


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        sudoku_str = f.read()
        solution = solve(*unpack(sudoku_str))
        print pack(solution)
        print
        print total_calls, 'calls'
