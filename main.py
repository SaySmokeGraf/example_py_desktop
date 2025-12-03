"""Главная точка входа в программу.

Содержит описание окон. Задает окно, вызывает и управляет прочими
подпрограммами проекта.
"""

import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget

from config import TIME_PREVIEW
from wins.main_win import MainWindow
from wins.preview_win import PreviewWindow


def start_main_window(main_window: QWidget, preview_window: QWidget,
                      timer: QTimer) -> None:
    """Запустить главное окно.

    Привязывается к окончанию отсчета таймера. Помимо прочего, перед запуском
    главного окна удаляет таймер и после - закрывает окно заставки.

    :param main_window: главное окно 
    :type main_window: QWidget
    :param preview_window: окно заставки 
    :type preview_window: QWidget
    :param timer: таймер, к которому привязан запуск данной функции
    :type timer: QTimer
    """
    timer.stop()
    del timer
    main_window.show()
    preview_window.close()


# главная точка входа в программу
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_Use96Dpi)

    # развертка заставки и главного окна
    preview_window = PreviewWindow()
    preview_window.setWindowFlag(Qt.FramelessWindowHint)
    main_window = MainWindow()
    main_window.setWindowFlags(Qt.Window |
                               Qt.CustomizeWindowHint |
                               Qt.WindowMinimizeButtonHint |
                               Qt.WindowMaximizeButtonHint |
                               Qt.WindowCloseButtonHint)
    
    # запуск заставки
    preview_window.show()

    # таймер и подвязка его окончания к запуску главного окна
    timer = QTimer()
    timer.setInterval(TIME_PREVIEW * 1000)
    timer.timeout.connect(lambda: start_main_window(main_window,
                                                    preview_window, timer))
    timer.start()
    
    sys.exit(app.exec())
