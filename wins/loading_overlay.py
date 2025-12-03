"""Модуль с оверлеем ожидания."""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QWidget

from config import PATH_IMG_LOADING
from ui.loadingGUI import Ui_LoadingOverlay


class LoadingOverlay(QFrame):
    """Класс оверлея ожидания."""

    def __init__(self, parent: QWidget) -> None:
        """Инициализация экземпляра класса.

        :param parent: родительское окно
        :type parent: QWidget
        """
        super().__init__(parent)

        self._ui = Ui_LoadingOverlay()
        self._ui.setupUi(self)
        self._ui.lbl_image.setPixmap(QPixmap(PATH_IMG_LOADING))
        self.setWindowFlags(Qt.WindowStaysOnTopHint |
                            Qt.FramelessWindowHint)
        
        self._place_on_parent(parent)
    
    def _place_on_parent(self, parent: QWidget) -> None:
        """Расположение оверлея ожидания на родителе.

        Располагает оверлей посередине родительского окна.

        :param parent: родительское окно
        :type parent: QWidget
        """
        height = self.geometry().height()
        width = self.geometry().width()
        parent_height = parent.geometry().height()
        parent_width = parent.geometry().width()
        x, y = (parent_width - width) // 2, (parent_height - height) // 2
        self.setGeometry(x, y, width, height)


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
