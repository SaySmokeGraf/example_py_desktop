"""Модуль окна с заставкой."""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame

from config import PATH_IMG_SIZED
from ui.previewGUI import Ui_PreviewWindow


class PreviewWindow(QFrame):
    """Класс окна с заставкой."""

    def __init__(self) -> None:
        """Инициализация экземляра класса.

        Задает ГПИ окна и необходимые значения атрибутов.
        """
        super().__init__()
        self.ui = Ui_PreviewWindow()
        self.ui.setupUi(self)
        self.ui.lbl_image.setPixmap(QPixmap(PATH_IMG_SIZED))


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
