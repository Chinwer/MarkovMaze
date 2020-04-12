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

    gamma = 0.95

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
        for i in range(self.rows):
            for j in range(self.cols):
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
                res += prob * (-0.8 + self.gamma * cell.value)
                continue

            dest_cell = self.cells[new_row][new_col]
            # When moving towards obstacle,
            # the agent moves back to where it was before
            if dest_cell.cell == Cell.BLOCK:
                dest_cell = cell
            # When moving towards trap cell,
            # the agent moves back to the start cell
            elif dest_cell.cell == Cell.TRAP:
                dest_cell = self.cells[0][0]
            res += prob * (
                util.REWARDS_MAP[dest_cell.cell] + self.gamma * dest_cell.value
            )

        return res
