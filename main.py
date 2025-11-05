"""
Главная программа проекта.
Задает окно, вызывает и управляет прочими подпрограммами проекта.

Классы:
    MainWindow

Функции:
    start_main_window() -> None
"""
import sys, os.path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from PIL import Image

from config import *
from modules.GUI_logic import Ui_Main_Upgraded
from modules.GUI_preview import Ui_PreviewWin


class PreviewWindow(QtWidgets.QFrame):
    """
    Класс окна заставки.

    Атрибуты:
    ---------
    None

    Методы:
    -------
    None
    """
    def __init__(self):
        """
        Инициализация экземляра класса.
        Задает ГПИ окна и необходимые значения атрибутов.

        Параметры:
        ----------
        None
        """
        super().__init__()
        self.ui = Ui_PreviewWin()
        self.ui.setupUi(self)

        # создание картинки с измененным под ГПИ размером по необходимости
        if os.path.exists(path_img_new):
            self.ui.lbl_image.setPixmap(QPixmap(path_img_new))
        else:
            image = Image.open(path_img)
            resized_image = image.resize(IMG_SIZES)
            resized_image.save(path_img_new)
            self.ui.lbl_image.setPixmap(QPixmap(path_img_new))

class MainWindow(QtWidgets.QMainWindow):
    """
    Класс для главного окна програмы с ГПИ и его логикой.

    Атрибуты:
    ---------
    None

    Методы:
    -------
    None
    """

    def __init__(self):
        """
        Инициализация экземляра класса.
        Задает ГПИ окна и необходимые значения атрибутов.

        Параметры:
        ----------
        None
        """
        super().__init__()
        self.ui = Ui_Main_Upgraded()
        self.ui.setupUi(self)


def start_main_window():
    """
    Запускает главное окно. Привязывается к окончанию отсчета таймера.
    Помимо прочего, удаляет таймер и закрывает окно заставки.

    Параметры:
    ----------
    window : PyQt5.QtWidgets.QMainWindow
        (global) Главное окно программы.
    timer : PyQt5.QtCore.QTimer
        (global) Таймер, к которому подвязан вызов данной функции.
    prewin : PyQt5.QtWidgets.QFrame
        (global) Окно заставки.
    
    Возвращаемое значение:
    ----------------------
    None
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
