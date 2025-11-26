"""Модуль главного окна."""

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from config import PATH_ICON
from ui.mainlogicGUI import Ui_Main_Upgraded


class MainWindow(QtWidgets.QMainWindow):
    """Класс для главного окна програмы с ГПИ и его логикой."""

    def __init__(self) -> None:
        """Инициализация экземляра класса.

        Задает ГПИ окна и необходимые значения атрибутов.
        """
        super().__init__()
        self.ui = Ui_Main_Upgraded()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(PATH_ICON))


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
