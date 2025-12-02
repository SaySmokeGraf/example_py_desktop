"""Модуль главного окна."""

from collections import namedtuple

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
import pyqtgraph as pgraph

from config import PATH_ICON
from ui.mainGUI import Ui_MainWindow
from utils.calc_thread import PlotCalcThread
from utils.dataflow_manager import DataFlowManager
from utils.graph_manager import GraphManager
from utils.methods import (
    calculate_method_1, calculate_method_2, calculate_method_3
)
from wins.loading_overlay import LoadingOverlay


class MainWindow(QMainWindow):
    """Класс для главного окна програмы с ГПИ и его логикой."""

    def __init__(self) -> None:
        """Инициализация экземляра класса.

        Задает ГПИ окна и необходимые значения атрибутов.
        """
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.setWindowIcon(QIcon(PATH_ICON))

        # разворачиваем графики и создаем менеджеры потоков данных
        graph_managers = self._setup_graphs()
        self._setup_dataflow_managers(graph_managers)

        # сигналы
        self._ui.btn_plot_m1.clicked.connect(lambda: self._plot_method(self._df_manager_m1))
        self._ui.btn_plot_m2.clicked.connect(lambda: self._plot_method(self._df_manager_m2))
        self._ui.btn_plot_m3.clicked.connect(lambda: self._plot_method(self._df_manager_m3))
        self._ui.check_legend_m1.stateChanged.connect(self._df_manager_m1.enable_legend)
        self._ui.check_legend_m2.stateChanged.connect(self._df_manager_m2.enable_legend)
        self._ui.check_legend_m3.stateChanged.connect(self._df_manager_m3.enable_legend)
    
    def _setup_graphs(self) -> list[GraphManager]:
        """Разворачивает все графики для методов.

        :return: список менеджеров графиков
        :rtype: list[GraphManager]
        """
        # подготавливаем именованные кортежи для замены лейблов, созданных для
        # этой цели, на графики
        MorphObject = namedtuple('MorphObject', ['frame', 'lbl', 'layout'])
        morph = (
            MorphObject(frame=self._ui.frame_graph_m1,
                        lbl=self._ui.lbl_to_morph_m1,
                        layout=self._ui.hlayout_graph_m1),
            MorphObject(frame=self._ui.frame_graph_m2,
                        lbl=self._ui.lbl_to_morph_m2,
                        layout=self._ui.hlayout_graph_m2),
            MorphObject(frame=self._ui.frame_graph_m3,
                        lbl=self._ui.lbl_to_morph_m3,
                        layout=self._ui.hlayout_graph_m3)
        )
        
        # цвета графиков
        pgraph.setConfigOption('background', 'w')
        pgraph.setConfigOption('foreground', 'k')

        # формируем список менеджеров графиков
        graph_managers = []

        # пробежка по 3 методам с заменой лейблов, созданных для этой цели, на
        # графики с дальнейшей их разверткой и менеджерами графиков
        for item in morph:
            item.layout.removeWidget(item.lbl)
            item.lbl.deleteLater()
            
            new_graph = pgraph.PlotWidget(item.frame)
            item.layout.addWidget(new_graph)
            graph_managers.append(GraphManager(new_graph))

        # возвращаем список менеджеров графиков
        return graph_managers
    
    def _setup_dataflow_managers(self,
                                 graph_managers: list[GraphManager]) -> None:
        """Создать менеджеры потоков данных.

        :param graph_managers: менеджеры графиков
        :type graph_managers: list[GraphManager]
        """
        self._df_manager_m1 = DataFlowManager(
            graph_manager=graph_managers[0],
            calc_data_sources=(self._ui.dspinbox_x1_m1,
                               self._ui.dspinbox_y1_m1,
                               self._ui.dspinbox_x2_m1,
                               self._ui.dspinbox_y2_m1,
                               self._ui.dspinbox_sigma_d_m1,
                               self._ui.dspinbox_sigma_r_m1,
                               self._ui.spinbox_p_m1,
                               self._ui.dspinbox_r_m1),
            calc_function=calculate_method_1,
            legend_checkbox=self._ui.check_legend_m1
        )

        self._df_manager_m2 = DataFlowManager(
            graph_manager=graph_managers[1],
            calc_data_sources=(self._ui.dspinbox_x1_m2,
                               self._ui.dspinbox_y1_m2,
                               self._ui.dspinbox_x2_m2,
                               self._ui.dspinbox_y2_m2,
                               self._ui.dspinbox_sigma_d_m2,
                               self._ui.dspinbox_sigma_r_m2,
                               self._ui.spinbox_p_m2,
                               self._ui.dspinbox_r_m2),
            calc_function=calculate_method_2,
            legend_checkbox=self._ui.check_legend_m2
        )

        self._df_manager_m3 = DataFlowManager(
            graph_manager=graph_managers[2],
            calc_data_sources=(self._ui.dspinbox_x1_m3,
                               self._ui.dspinbox_y1_m3,
                               self._ui.dspinbox_x2_m3,
                               self._ui.dspinbox_y2_m3,
                               self._ui.dspinbox_sigma_d_m3,
                               self._ui.dspinbox_sigma_r_m3,
                               self._ui.spinbox_p_m3,
                               self._ui.dspinbox_r_m3),
            calc_function=calculate_method_3,
            legend_checkbox=self._ui.check_legend_m3
        )
    
    def active_elems_enabled(self, enabled: bool) -> None:
        """Включение/выключение активных (интерактивных) элементов ГПИ.

        :param enabled: флаг включенности
        :type enabled: bool
        """
        self._ui.tabs_methods.setEnabled(enabled)
    
    def _plot_method(self, df_manager: DataFlowManager) -> None:
        """Построить график метода с помощью менеджера потока данных.

        Запускает оверлей ожидания и отдельный поток для расчета и сообщения
        результатов графику.

        :param df_manager: менеджер потока данных
        :type df_manager: DataFlowManager
        """
        loading_overlay = LoadingOverlay(self)
        loading_overlay.show()
        calc_thread = PlotCalcThread(self, loading_overlay, df_manager)
        calc_thread.start()


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
