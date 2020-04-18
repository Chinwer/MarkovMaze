import util
from PyQt5 import uic, QtGui, QtWidgets

from maze_view import MazeView
from decision import MarkovDecision


class MazeWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("maze_solver.ui", self)
        self.maze_view = MazeView(5, 5)
        self.vert_layout.addWidget(self.maze_view)
        self.decision = MarkovDecision(
            self.maze_view.maze_cell, 5, 5
        )

    def gen_maze(self):
        (w, h) = util.DIFFICULTY_MAP[self.b_difficulty.currentText()]
        self.maze_view.gen_maze(w, h)
        self.decision.refresh_cells(
            self.maze_view.maze_cell, w, h
        )
        self.l_iter.setText(f"N = {self.decision.iter_count}")

    def solve(self):
        # print()
        # for rows in self.maze_view.maze_cell:
        #     for r in rows:
        #         print("{:.2f}".format(r.value), end=" ")
        #     print()
        self.decision.iter()
        self.maze_view.scene.update()
        self.l_iter.setText(f"N = {self.decision.iter_count}")

    def show(self):
        pass
