#!/usr/bin/env python3
from enum import Enum

import util
from cell import Cell

# Moving direction


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class MarkovDecision:
    # Probability of moving in all directions
    probability_map = [
        [0.2, 0.6, 0.2],  # left-up, up, right-up
        [0.2, 0.6, 0.2],  # left-down, down, right-down
        [0.2, 0.6, 0.2],  # left-up, left, left-down
        [0.2, 0.6, 0.2],  # right-up, right, right-down
    ]
    # Position change of moving
    pos_delta_map = [
        [(-1, -1), (-1, 0), (-1, 1)],  # left-up, up, right-up
        [(1, -1), (1, 0), (1, 1)],  # left-down, down, right-down
        [(-1, -1), (0, -1), (1, -1)],  # left-up, left, left-down
        [(-1, 1), (0, 1), (1, 1)],  # right-up, right, right-down
    ]

    gamma = 0.8

    def __init__(self, cells, rows, cols):
        self.cells = cells
        self.rows = rows
        self.cols = cols
        self.iter_count = 1

    def refresh_cells(self, cells, rows, cols):
        self.cells = cells
        self.rows = rows
        self.cols = cols
        self.iter_count = 1

    def iter(self):
        for i in range(self.rows - 1, -1, -1):
            for j in range(self.cols - 1, -1, -1):
                cur_cell = self.cells[i][j]
                if (
                    cur_cell.cell == Cell.TRAP
                    or cur_cell.cell == Cell.END
                    or cur_cell.cell == Cell.BLOCK
                ):
                    continue
                new_val = float("-inf")
                for drct in Direction:
                    res = self.move(cur_cell, drct)
                    new_val = max(new_val, res)
                cur_cell.set_value(new_val)
        self.iter_count += 1

    def move(self, cell, drct: Direction):
        res = 0
        idx = drct.value

        for i, prob in enumerate(self.probability_map[idx]):
            pos_delta = self.pos_delta_map[idx][i]
            new_row = cell.row + pos_delta[0]
            new_col = cell.col + pos_delta[1]

            # Move out of boundary
            if (
                new_row < 0
                or new_row >= self.rows
                or new_col < 0
                or new_col >= self.cols
            ):
                res += prob * (-0.5 + self.gamma * cell.value)
                continue

            dest_cell = self.cells[new_row][new_col]
            value = dest_cell.value
            if dest_cell.cell == Cell.BLOCK:
                value = cell.value
            elif dest_cell.cell == Cell.TRAP:
                value = self.cells[0][0].value
            elif dest_cell.cell == Cell.END:
                value = 0

            res += prob * \
                (util.REWARDS_MAP[dest_cell.cell] + self.gamma * value)

        return res

    # Find a path from the starting cell to the ending cell
    def walk(self):
        res = [(0, 0)]
        arrived = False
        cur_pos = (0, 0)
        while not arrived:
            cur_pos = self.next_step(cur_pos)
            if cur_pos == (self.rows - 1, self.cols - 1):
                # destination arrived
                arrived = True
            if cur_pos in res or cur_pos == (-1, -1):
                # The agent has stepped back to previously arrived cell
                # A valid path can't be found according to the current iteration result
                return []
            res.append(cur_pos)
        return res

    def is_out_of_bound(self, row, col):
        return (row < 0 or col < 0
                or row >= self.rows or col >= self.cols)

    def next_step(self, cur_pos):
        res = (-1, -1)
        max_val = -9999
        for i in range(-1, 2):
            for j in range(-1, 2):
                row = cur_pos[0] + i
                col = cur_pos[1] + j
                if self.is_out_of_bound(row, col):
                    continue
                cell = self.cells[row][col]
                if cell.cell == Cell.BLOCK or cell.cell == Cell.TRAP:
                    continue
                if cell.value > max_val:
                    max_val = cell.value
                    res = (row, col)
        return res
