"""Главная точка входа в программу.

Содержит описание окон. Задает окно, вызывает и управляет прочими
подпрограммами проекта.
"""

import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt

from config import TIME_PREVIEW
from wins.main_win import MainWindow
from wins.preview_win import PreviewWindow


def start_main_window() -> None:
    """Запускает главное окно.

    Привязывается к окончанию отсчета таймера. Помимо прочего, удаляет таймер и
    закрывает окно заставки.
    """
    global main_window, preview_window, timer

    timer.stop()
    del timer
    preview_window.close()

    main_window = MainWindow()
    main_window.setWindowFlags(QtCore.Qt.Window |
                               QtCore.Qt.CustomizeWindowHint |
                               QtCore.Qt.WindowMinimizeButtonHint |
                               QtCore.Qt.WindowMaximizeButtonHint |
                               QtCore.Qt.WindowCloseButtonHint)
    main_window.show()


# главная точка входа в программу
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_Use96Dpi)

    preview_window = PreviewWindow()
    preview_window.setWindowFlag(Qt.FramelessWindowHint)
    preview_window.show()

    timer = QTimer()
    timer.setInterval(TIME_PREVIEW * 1000)
    timer.timeout.connect(start_main_window)
    timer.start()
    
    sys.exit(app.exec())
