"""Модуль главного окна."""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox, QMainWindow
import pyqtgraph as pgraph

from config import PATH_ICON
from ui.mainGUI import Ui_MainWindow
from utils.graph_manager import GraphManager
from utils.methods import (
    calculate_method_1, calculate_method_2, calculate_method_3
)


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

        # описание создаваемых далее атрибутов класса
        self._checkboxes_leg: tuple[QCheckBox]  # чекбоксы вкл/выкл легенд
        self._graph_managers: list[GraphManager]  # менеджеры графиков

        # дополнительный ГПИ
        self._setup_additional_ui()

        # сигналы
        self._ui.btn_plot_m_1.clicked.connect(self._calculate_method_1)
        self._ui.btn_plot_m_2.clicked.connect(self._calculate_method_2)
        self._ui.btn_plot_m_3.clicked.connect(self._calculate_method_3)
        self._ui.checkBox_legend_m_1.stateChanged.connect(lambda: self._upd_legend(0))
        self._ui.checkBox_legend_m_2.stateChanged.connect(lambda: self._upd_legend(1))
        self._ui.checkBox_legend_m_3.stateChanged.connect(lambda: self._upd_legend(2))
    
    def _setup_additional_ui(self) -> None:
        """Развернуть дополнительный ГПИ."""
        # подготавливаем временные кортежи и списки для расположения графиков
        self._temp_frames_graph = (self._ui.frame_graph_m_1,
                                   self._ui.frame_graph_m_2,
                                   self._ui.frame_graph_m_3)
        self._temp_lbls_to_morph = [self._ui.lbl_to_morph_into_graph_m_1,
                                    self._ui.lbl_to_morph_into_graph_m_2,
                                    self._ui.lbl_to_morph_into_graph_m_3]
        self._temp_h_layouts = (self._ui.horizontalLayout_9,
                                self._ui.horizontalLayout_10,
                                self._ui.horizontalLayout_14)

        # подготавливаем список чекбоксов вкл/выкл легенд
        self._checkboxes_leg = (self._ui.checkBox_legend_m_1,
                                self._ui.checkBox_legend_m_2,
                                self._ui.checkBox_legend_m_3)
        
        # разворачиваем графики
        self._setup_graphs()
    
    def _setup_graphs(self) -> None:
        """Разворачивает все графики для методов."""
        # цвета графиков
        pgraph.setConfigOption('background', 'w')
        pgraph.setConfigOption('foreground', 'k')

        # формируем список менеджеров графиков
        self._graph_managers = []

        # пробежка по 3 методам с заменой лейблов, созданных для этой цели, на
        # графики с дальнейшей их разверткой и менеджерами графиков
        for i in range(3):
            self._temp_h_layouts[i].removeWidget(self._temp_lbls_to_morph[i])
            self._temp_lbls_to_morph[i].deleteLater()
            self._temp_lbls_to_morph[i] = None
            
            new_graph = pgraph.PlotWidget(self._temp_frames_graph[i])
            self._temp_h_layouts[i].addWidget(new_graph)
            self._graph_managers.append(GraphManager(new_graph))
        
        # удаляем временные списки и кортежи
        del self._temp_frames_graph
        del self._temp_h_layouts
        del self._temp_lbls_to_morph
    
    def _active_elems_enabled(self, enabled: bool) -> None:
        """Включение/выключение активных (интерактивных) элементов ГПИ.

        :param enabled: флаг включенности
        :type enabled: bool
        """
        self._ui.tabWidget.setEnabled(enabled)
    
    def _upd_legend(self, n: int) -> None:
        """Обновить состояние легенды на графике.

        :param n: номер графика от 0 до 2
        :type n: int
        """
        enabled = self._checkboxes_leg[n].isChecked()
        self._graph_managers[n].enable_legend(enabled)
    
    def _calculate_method_1(self) -> None:
        """Расчет рабочей зоны по первому методу (разностно-дальномерный).
        
        Производит расчет и выводит полученный результат на график. На время
        расчета отключает активные элементы ГПИ.
        """
        # отключение активных элементов
        self._active_elems_enabled(False)

        # параметры построения графика
        X2 = self._ui.doubleSpinBox_x1_m_1.value()
        Y2 = self._ui.doubleSpinBox_y1_m_1.value()
        X3 = self._ui.doubleSpinBox_x2_m_1.value()
        Y3 = self._ui.doubleSpinBox_y2_m_1.value()

        sigma_r_allow = self._ui.doubleSpinBox_sigma_d_m_1.value()
        sigma_t = self._ui.doubleSpinBox_sigma_r_m_1.value()

        P = self._ui.spinBox_p_m_1.value()
        r = self._ui.doubleSpinBox_r_m_1.value()

        # расчет
        graph_data = calculate_method_1(X2, Y2, X3, Y3,
                                        sigma_r_allow, sigma_t, P, r)
        
        # обновление графика и включение активных элементов
        self._graph_managers[0].update(*graph_data)
        self._active_elems_enabled(True)

    def _calculate_method_2(self) -> None:
        """Расчет рабочей зоны по второму методу (дальномерный).
        
        Производит расчет и выводит полученный результат на график. На время
        расчета отключает активные элементы ГПИ.
        """
        # отключение активных элементов
        self._active_elems_enabled(False)

        # параметры построения графика
        A1 = self._ui.doubleSpinBox_x1_m_2.value()
        A2 = self._ui.doubleSpinBox_y1_m_2.value()
        B1 = self._ui.doubleSpinBox_x2_m_2.value()
        B2 = self._ui.doubleSpinBox_y2_m_2.value()

        sigma_d = self._ui.doubleSpinBox_sigma_d_m_2.value()
        sigma_r = self._ui.doubleSpinBox_sigma_r_m_2.value()

        P = self._ui.spinBox_p_m_2.value()
        r = self._ui.doubleSpinBox_r_m_2.value()

        # расчет
        graph_data = calculate_method_2(A1, A2, B1, B2,
                                        sigma_d, sigma_r, P, r)

        # обновление графика и включение активных элементов
        self._graph_managers[1].update(*graph_data)
        self._active_elems_enabled(True)

    def _calculate_method_3(self) -> None:
        """Расчет рабочей зоны по третьему методу (угломерный).
        
        Производит расчет и выводит полученный результат на график. На время
        расчета отключает активные элементы ГПИ.
        """
        # отключение активных элементов
        self._active_elems_enabled(False)

        # параметры построения графика
        A1 = self._ui.doubleSpinBox_x1_m_3.value()
        A2 = self._ui.doubleSpinBox_y1_m_3.value()
        B1 = self._ui.doubleSpinBox_x2_m_3.value()
        B2 = self._ui.doubleSpinBox_y2_m_3.value()

        sigma_d = self._ui.doubleSpinBox_sigma_d_m_3.value()
        sigma_theta = self._ui.doubleSpinBox_sigma_r_m_3.value()

        P = self._ui.spinBox_p_m_3.value()
        r = self._ui.doubleSpinBox_r_m_3.value()

        # расчет
        graph_data = calculate_method_3(A1, A2, B1, B2,
                                        sigma_d, sigma_theta, P, r)

        # обновление графика и включение активных элементов
        self._graph_managers[2].update(*graph_data)
        self._active_elems_enabled(True)


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
