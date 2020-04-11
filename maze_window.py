import util
from PyQt5 import uic, QtGui, QtWidgets
from maze_view import MazeView


class MazeWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("maze_solver.ui", self)
        self.maze_view = MazeView(5, 5)
        self.vert_layout.addWidget(self.maze_view)

    def gen_maze(self):
        (w, h) = util.DIFFICULTY_MAP[self.b_difficulty.currentText()]
        self.maze_view.gen_maze(w, h)

    def solve(self):
        pass
