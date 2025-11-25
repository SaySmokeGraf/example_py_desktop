"""Главная точка входа в программу.

Содержит описание окон. Задает окно, вызывает и управляет прочими
подпрограммами проекта.
"""

import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap

from config import PATH_IMG_SIZED, TIME_PREVIEW
from ui.mainlogicGUI import Ui_Main_Upgraded
from ui.previewGUI import Ui_PreviewWin


class PreviewWindow(QtWidgets.QFrame):
    """Класс окна заставки."""

    def __init__(self) -> None:
        """Инициализация экземляра класса.

        Задает ГПИ окна и необходимые значения атрибутов.
        """
        super().__init__()
        self.ui = Ui_PreviewWin()
        self.ui.setupUi(self)
        self.ui.lbl_image.setPixmap(QPixmap(PATH_IMG_SIZED))


class MainWindow(QtWidgets.QMainWindow):
    """Класс для главного окна програмы с ГПИ и его логикой."""

    def __init__(self) -> None:
        """Инициализация экземляра класса.

        Задает ГПИ окна и необходимые значения атрибутов.
        """
        super().__init__()
        self.ui = Ui_Main_Upgraded()
        self.ui.setupUi(self)


def start_main_window() -> None:
    """Запускает главное окно.

    Привязывается к окончанию отсчета таймера. Помимо прочего, удаляет таймер и
    закрывает окно заставки.
    """
    global window, timer, prewin

    timer.stop()
    del timer
    prewin.close()

    window = MainWindow()
    window.setWindowFlags(QtCore.Qt.Window |
                        QtCore.Qt.CustomizeWindowHint |
                        QtCore.Qt.WindowMinimizeButtonHint |
                        QtCore.Qt.WindowMaximizeButtonHint |
                        QtCore.Qt.WindowCloseButtonHint)
    window.show()


# главная точка входа в программу
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_Use96Dpi)

    prewin = PreviewWindow()
    prewin.setWindowFlag(Qt.FramelessWindowHint)
    prewin.show()

    timer = QTimer()
    timer.setInterval(TIME_PREVIEW*1000)
    timer.timeout.connect(start_main_window)
    timer.start()
    
    sys.exit(app.exec())
