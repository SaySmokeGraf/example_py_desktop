"""Модуль с потоком расчета данных для графика."""

from threading import Thread

from PyQt5.QtWidgets import QWidget

from utils.dataflow_manager import DataFlowManager


class PlotCalcThread(Thread):
    """Поток расчета данных для графика."""

    def __init__(self, parent: QWidget, overlay: QWidget,
                 df_manager: DataFlowManager) -> None:
        """Инициализация экземпляра класса.

        :param parent: родительское окно
        :type parent: QWidget
        :param overlay: оверлей ожидания
        :type overlay: QWidget
        :param df_manager: менеджер потока данных
        :type df_manager: DataFlowManager
        """
        super().__init__(daemon=True)
        self._parent = parent
        self._overlay = overlay
        self._df_manager = df_manager

    def run(self) -> None:
        """Основное инструкции для потока."""
        self._parent.active_elems_enabled(False)
        self._df_manager.plot_method()
        self._overlay.close()
        self._parent.active_elems_enabled(True)


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
