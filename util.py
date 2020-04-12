import random
from cell import Cell


DIFFICULTY_MAP = {
    "Easy": (5, 5),
    "Medium": (15, 15),
    "Hard": (25, 25),
}

REWARDS_MAP = {
    Cell.PATH: -0.04,
    Cell.BLOCK: -0.75,
    Cell.TRAP: -1,
    Cell.START: -0.04,
    Cell.END: 1,
}

INIT_VAL_MAP = {
    Cell.PATH: 0,
    Cell.BLOCK: -0.75,
    Cell.TRAP: -1,
    Cell.START: 0,
    Cell.END: 1,
}


def gen_maze_reachable(w, h):

    # TODO: better random path algorithm
    def choose_random_path(w, h):
        res = {(0, 0)}
        i, j = 0, 0
        while i + 1 < w and j + 1 < h:
            if random.randint(0, 1) == 1:
                # go right
                i += 1
                res.add((i, j))
            else:
                j += 1
                res.add((i, j))

        if i + 1 < w:
            res.update([(x, j) for x in range(i + 1, w)])
        i = w - 1
        if j + 1 < h:
            res.update([(i, x) for x in range(j + 1, h)])

        return res

    path = choose_random_path(w, h)
    maze = [
        [Cell(random.randint(0, 2)) if (i, j) not in path else Cell(0) for j in range(h)]
        for i in range(w)
    ]
    maze[0][0] = Cell.START
    maze[w - 1][h - 1] = Cell.END
    return maze


if __name__ == "__main__":
    print(gen_maze_reachable(4, 5))
