import util
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from maze_view import MazeView
from decision import MarkovDecision


class MazeWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("maze_solver.ui", self)
        self.maze_view = MazeView(4, 4)
        self.vert_layout.addWidget(self.maze_view)
        self.decision = MarkovDecision(self.maze_view.maze_cell, 4, 4)

    def gen_maze(self):
        (w, h) = util.DIFFICULTY_MAP[self.b_difficulty.currentText()]
        self.maze_view.gen_maze(w, h)
        self.decision.refresh_cells(self.maze_view.maze_cell, w, h)
        self.l_iter.setText(f"N = {self.decision.iter_count}")

    def solve(self):
        self.decision.iter()
        self.maze_view.scene.update()
        self.l_iter.setText(f"N = {self.decision.iter_count}")

    def information(self, title, msg):
        QMessageBox.information(self, title, msg, QMessageBox.Ok)

    def walk(self):
        path = self.decision.walk()
        if len(path) == 0:
            self.information("Information", "Cannot find a valid path!")
        else:
            self.maze_view.show_path(path)
