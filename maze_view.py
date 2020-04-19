import util
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
from cell import Cell


class MazeView(QtWidgets.QGraphicsView):
    WIDTH = 800
    HEIGHT = 800

    def __init__(self, w, h, parent=None):
        super().__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setFixedSize(self.WIDTH + 100, self.HEIGHT + 100)
        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)
        # self.fitInView(0, 0, self.WIDTH, self.HEIGHT, Qt.KeepAspectRatio)
        self.w = w
        self.h = h
        self.cell_size = self.WIDTH / self.w
        self.maze_cell = self.gen_cells()

    def gen_maze(self, w, h):
        self.scene.clear()
        self.w = w
        self.h = h
        self.cell_size = self.WIDTH / self.w
        self.maze_cell = self.gen_cells()

    def gen_cells(self):
        cells = util.gen_maze_reachable(self.w, self.h)
        cell_items = []
        for i in range(self.w):
            cell_items.append([])
            for j in range(self.h):
                cell = CellItem(i, j, self.cell_size, cells[i][j])
                cell_items[i].append(cell)
                self.scene.addItem(cell)

        return cell_items

    def show_path(self, path):
        for (r, c) in path:
            self.maze_cell[r][c].in_path = True
        self.scene.update()


class CellItem(QtWidgets.QGraphicsItem):
    block_color_map = {
        Cell.PATH: Qt.white,
        Cell.BLOCK: Qt.black,
        Cell.TRAP: Qt.gray,
        Cell.START: Qt.blue,
        Cell.END: Qt.red,
    }
    pen_color_map = {
        Cell.PATH: Qt.black,
        Cell.BLOCK: Qt.white,
        Cell.TRAP: Qt.white,
        Cell.START: Qt.white,
        Cell.END: Qt.white,
    }

    def __init__(self, row, col, size, cell=Cell.PATH, parent=None):
        super().__init__(parent)
        self.setPos(col * size, row * size)
        self.row = row
        self.col = col
        self.size = size
        self.cell = cell
        self.value = util.INIT_VAL_MAP[self.cell]
        self.in_path = False

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.size, self.size)

    def set_value(self, value: float):
        self.value = value

    def paint(self, painter, style_option_graphics_item, widget=None):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(self.boundingRect(), self.block_color_map[self.cell])

        # draw border
        painter.setPen(QtGui.QPen(Qt.black))
        painter.drawRect(self.boundingRect())

        if self.in_path:
            color = QtGui.QColor("#f5b971")
            painter.setPen(QtGui.QPen(color))
            painter.setBrush(QtGui.QBrush(color))
            x = self.size / 2
            y = self.size / 2
            painter.drawEllipse(QPoint(x, y), self.size / 6, self.size / 6)

        font = QtGui.QFont()
        font.setPointSize(10)
        painter.setPen(QtGui.QPen(self.pen_color_map[self.cell]))
        painter.setFont(font)
        painter.drawText(
            self.boundingRect(),
            Qt.AlignHCenter | Qt.AlignVCenter,
            "{:.2f}".format(self.value),
        )
