"""Модуль главного окна."""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCheckBox, QMainWindow
import pyqtgraph as pg

from config import PATH_ICON
from ui.mainGUI import Ui_MainWindow
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
        self._checkboxes_leg: list[QCheckBox]  # чекбоксы вкл/выкл легенд

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
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # формируем необходимые списки графиков и их элементов
        self._graphs = []
        self._plot_data = []
        self._plot_outline = []
        self._plot_stations = []
        self._plot_legends = []

        # пробежка по 3 методам для разворачивания для них графиков
        for i in range(3):
            self._temp_h_layouts[i].removeWidget(self._temp_lbls_to_morph[i])
            self._temp_lbls_to_morph[i].deleteLater()
            self._temp_lbls_to_morph[i] = None

            self._graphs.append(pg.PlotWidget(self._temp_frames_graph[i]))
            self._temp_h_layouts[i].addWidget(self._graphs[i])
            self._graphs[i].setLabel('left', 'Ось Y')
            self._graphs[i].setLabel('bottom', 'Ось X')
            self._graphs[i].showGrid(x=True, y=True)

            self._plot_data.append(self._graphs[i].plot([], [], pen=None, symbol='o', symbolSize=5,
                                  symbolPen='b', symbolBrush='b', name='Подходящая область'))
            self._plot_outline.append(self._graphs[i].plot([], [], pen=None, symbol='o', symbolSize=5,
                                  symbolPen='k', symbolBrush='k', name='Контур подходящей области'))
            self._plot_stations.append(self._graphs[i].plot([], [], pen=None, symbol='t1', symbolSize=20,
                                      symbolPen='r', symbolBrush='r', name='Маяки'))
            
            self._plot_legends.append(None)
            self._set_legend_on_graph(i, True)
        
        # удаляем временные списки и кортежи
        del self._temp_frames_graph
        del self._temp_h_layouts
        del self._temp_lbls_to_morph

    def _set_legend_on_graph(self, n: int, enabled: bool) -> None:
        """Установить легенду на графике.
        
        :param n: номер графика от 0 до 2
        :type n: int
        :param enabled: флаг включенности легенды
        :type enabled: bool
        """
        if enabled:
            if self._plot_legends[n] == None:
                self._plot_legends[n] = pg.LegendItem((80,60), offset=(70,20), frame=True, brush='w')
                self._plot_legends[n].setParentItem(self._graphs[n].graphicsItem())
                self._plot_legends[n].addItem(self._plot_data[n], 'Подходящая область')
                self._plot_legends[n].addItem(self._plot_outline[n], 'Контур подходящей области')
                self._plot_legends[n].addItem(self._plot_stations[n], 'Маяки')
                self._plot_legends[n].setZValue(1)
        else:
            self._graphs[n].scene().removeItem(self._plot_legends[n])
            self._plot_legends[n] = None
    
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
        self._set_legend_on_graph(n, self._checkboxes_leg[n].isChecked())
    
    def _upd_graph(self, n: int, X: list[float], Y: list[float],
                   Xout: list[float], Yout: list[float],
                   Xm: list[float], Ym: list[float]) -> None:
        """Обновляет данные на графике.

        :param n: номер графика от 0 до 2
        :type n: int
        :param X: список координат X подходящих точек
        :type X: list[float]
        :param Y: список координат Y подходящих точек
        :type Y: list[float]
        :param Xout: список координат X контура подходящих точек
        :type Xout: list[float]
        :param Yout: список координат Y контура подходящих точек
        :type Yout: list[float]
        :param Xm: список координат X маяков
        :type Xm: list[float]
        :param Ym: список координат Y маяков
        :type Ym: list[float]
        """
        self._plot_data[n].setData(X, Y)
        self._plot_outline[n].setData(Xout, Yout)
        self._plot_stations[n].setData(Xm, Ym)
    
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
        self._upd_graph(0, *graph_data)
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
        self._upd_graph(1, *graph_data)
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
        self._upd_graph(2, *graph_data)
        self._active_elems_enabled(True)


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
