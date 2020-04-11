#!/usr/bin/env python

import sys
from PyQt5.Qt import QApplication
from maze_window import MazeWindow


def main():
    app = QApplication(sys.argv)
    window = MazeWindow()
    window.show()
    sys.exit(app.exec())


main()
