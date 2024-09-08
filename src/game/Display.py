from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PySide6.QtGui import QColor

from src.game.Constants import Constants


class Chessboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        self.setLayout(grid_layout)

        white = QColor('white')
        black = QColor('black')

        for row in range(Constants.BOARD_SIZE):
            for col in range(Constants.BOARD_SIZE):
                label = QLabel()
                if (row + col) % 2 == 0:
                    label.setStyleSheet(f"background-color: {white.name()};")
                else:
                    label.setStyleSheet(f"background-color: {black.name()};")
                grid_layout.addWidget(label, row, col)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chessboard')
        self.setGeometry(100, 100, 800, 800)
        self.setCentralWidget(Chessboard())

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.resize(size, size)
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
