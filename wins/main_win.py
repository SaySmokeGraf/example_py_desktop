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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(PATH_ICON))

        # описание создаваемых далее атрибутов класса
        self._checkboxes_leg: tuple[QCheckBox]  # чекбоксы вкл/выкл легенд
        self._graph_managers: list[GraphManager]  # менеджеры графиков

        # дополнительный ГПИ
        self._setup_additional_ui()

        # сигналы
        self.ui.btn_plot_m_1.clicked.connect(self._calculate_method_1)
        self.ui.btn_plot_m_2.clicked.connect(self._calculate_method_2)
        self.ui.btn_plot_m_3.clicked.connect(self._calculate_method_3)
        self.ui.checkBox_legend_m_1.stateChanged.connect(lambda: self._upd_legend(0))
        self.ui.checkBox_legend_m_2.stateChanged.connect(lambda: self._upd_legend(1))
        self.ui.checkBox_legend_m_3.stateChanged.connect(lambda: self._upd_legend(2))
    
    def _setup_additional_ui(self) -> None:
        """Развернуть дополнительный ГПИ."""
        # подготавливаем временные кортежи и списки для расположения графиков
        self._temp_frames_graph = (self.ui.frame_graph_m_1,
                                   self.ui.frame_graph_m_2,
                                   self.ui.frame_graph_m_3)
        self._temp_lbls_to_morph = [self.ui.lbl_to_morph_into_graph_m_1,
                                    self.ui.lbl_to_morph_into_graph_m_2,
                                    self.ui.lbl_to_morph_into_graph_m_3]
        self._temp_h_layouts = (self.ui.horizontalLayout_9,
                                self.ui.horizontalLayout_10,
                                self.ui.horizontalLayout_14)

        # подготавливаем список чекбоксов вкл/выкл легенд
        self._checkboxes_leg = (self.ui.checkBox_legend_m_1,
                                self.ui.checkBox_legend_m_2,
                                self.ui.checkBox_legend_m_3)
        
        # разворачиваем графики
        self._setup_graphs()
    
    def _setup_graphs(self) -> None:
        """Разворачивает все графики для методов."""
        # цвета графиков
        pgraph.setConfigOption('background', 'w')
        pgraph.setConfigOption('foreground', 'k')

        # формируем список менеджеров графиков
        self._graph_managers = []

        # пробежка по 3 методам для разворачивания для них графиков
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
        self.ui.tabWidget.setEnabled(enabled)
    
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

        # координаты
        X2, Y2 = self.ui.doubleSpinBox_x1_m_1.value(), self.ui.doubleSpinBox_y1_m_1.value()
        X3, Y3 = self.ui.doubleSpinBox_x2_m_1.value(), self.ui.doubleSpinBox_y2_m_1.value()

        # параметры погрешностей
        sigma_r_allow = self.ui.doubleSpinBox_sigma_d_m_1.value()
        sigma_t = self.ui.doubleSpinBox_sigma_r_m_1.value()

        # параметры разбиения 
        P = self.ui.spinBox_p_m_1.value()
        r = self.ui.doubleSpinBox_r_m_1.value()

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

        # координаты
        A1, A2 = self.ui.doubleSpinBox_x1_m_2.value(), self.ui.doubleSpinBox_y1_m_2.value()
        B1, B2 = self.ui.doubleSpinBox_x2_m_2.value(), self.ui.doubleSpinBox_y2_m_2.value()

        # параметры погрешностей
        sigma_d = self.ui.doubleSpinBox_sigma_d_m_2.value()
        sigma_r = self.ui.doubleSpinBox_sigma_r_m_2.value()

        # параметры разбиения 
        P = self.ui.spinBox_p_m_2.value()
        r = self.ui.doubleSpinBox_r_m_2.value()

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

        # координаты
        A1, A2 = self.ui.doubleSpinBox_x1_m_3.value(), self.ui.doubleSpinBox_y1_m_3.value()
        B1, B2 = self.ui.doubleSpinBox_x2_m_3.value(), self.ui.doubleSpinBox_y2_m_3.value()

        # параметры погрешностей
        sigma_d = self.ui.doubleSpinBox_sigma_d_m_3.value()
        sigma_theta = self.ui.doubleSpinBox_sigma_r_m_3.value()

        # параметры разбиения 
        P = self.ui.spinBox_p_m_3.value()
        r = self.ui.doubleSpinBox_r_m_3.value()

        # расчет
        graph_data = calculate_method_3(A1, A2, B1, B2,
                                        sigma_d, sigma_theta, P, r)

        # обновление графика и включение активных элементов
        self._graph_managers[2].update(*graph_data)
        self._active_elems_enabled(True)


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
