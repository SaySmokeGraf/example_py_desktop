"""Модуль с ГПИ для проекта.

Дорабатывает автоматически созданный ГПИ (Qt Designer + pyuic5) и задает логику
отработки элементов.
"""

import math

from PyQt5.QtWidgets import QMainWindow
import pyqtgraph as pg

from ui.mainGUI import Ui_MainWindow


class Ui_Main_Upgraded(Ui_MainWindow):
    """Класс ГПИ и логики отработки элементов ГПИ проекта.

    Родительский класс содержит автоматически созданный с помощью Qt Designer и
    pyuic5 ГПИ.
    """

    def setupUi(self, main_window_instance: QMainWindow) -> None:
        """Установка элементов и их параметров на ГПИ.

        :param main_window_instance: инстанция главного окна
        :type main_window_instance: QMainWindow
        """
        super().setupUi(main_window_instance)
        self.btn_plot_m_1.clicked.connect(self._calculate_method_1)
        self.btn_plot_m_2.clicked.connect(self._calculate_method_2)
        self.btn_plot_m_3.clicked.connect(self._calculate_method_3)
        self.checkBox_legend_m_1.stateChanged.connect(lambda: self._upd_legend(0))
        self.checkBox_legend_m_2.stateChanged.connect(lambda: self._upd_legend(1))
        self.checkBox_legend_m_3.stateChanged.connect(lambda: self._upd_legend(2))

        # подготавливаем кортежи и списки для расположения графиков в ГПИ
        # и настройки их элементов и параметров в дальнейшем
        self.frame_graph = (self.frame_graph_m_1, self.frame_graph_m_2,
                            self.frame_graph_m_3)
        self.lbl_to_morph = [self.lbl_to_morph_into_graph_m_1, self.lbl_to_morph_into_graph_m_2,
                             self.lbl_to_morph_into_graph_m_3]
        self.h_layouts = (self.horizontalLayout_9, self.horizontalLayout_10,
                          self.horizontalLayout_14)
        self.checkboxes_leg = (self.checkBox_legend_m_1, self.checkBox_legend_m_2,
                               self.checkBox_legend_m_3)
        
        # разворачиваем графики
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.graph = []
        self.plot_data = []
        self.plot_outline = []
        self.plot_stations = []
        self.plot_legends = []
        for i in range(3):
            self.h_layouts[i].removeWidget(self.lbl_to_morph[i])
            self.lbl_to_morph[i].deleteLater()
            self.lbl_to_morph[i] = None

            self.graph.append(pg.PlotWidget(self.frame_graph[i]))
            self.h_layouts[i].addWidget(self.graph[i])
            self.graph[i].setLabel('left', 'Ось Y')
            self.graph[i].setLabel('bottom', 'Ось X')
            self.graph[i].showGrid(x=True, y=True)

            self.plot_data.append(self.graph[i].plot([], [], pen=None, symbol='o', symbolSize=5,
                                  symbolPen='b', symbolBrush='b', name='Подходящая область'))
            self.plot_outline.append(self.graph[i].plot([], [], pen=None, symbol='o', symbolSize=5,
                                  symbolPen='k', symbolBrush='k', name='Контур подходящей области'))
            self.plot_stations.append(self.graph[i].plot([], [], pen=None, symbol='t1', symbolSize=20,
                                      symbolPen='r', symbolBrush='r', name='Маяки'))
            
            self.plot_legends.append(None)
            self._set_legend_on_graph(i, True)
            
    
    def _active_elems_enabled(self, enabled: bool) -> None:
        """Включение/выключение активных (интерактивных) элементов ГПИ.

        :param enabled: флаг включенности
        :type enabled: bool
        """
        self.tabWidget.setEnabled(enabled)
    
    def _set_legend_on_graph(self, n: int, enabled: bool) -> None:
        """Установить легенду на графике.
        
        :param n: номер графика от 0 до 2
        :type n: int
        :param enabled: флаг включенности легенды
        :type enabled: bool
        """
        if enabled:
            if self.plot_legends[n] == None:
                self.plot_legends[n] = pg.LegendItem((80,60), offset=(70,20), frame=True, brush='w')
                self.plot_legends[n].setParentItem(self.graph[n].graphicsItem())
                self.plot_legends[n].addItem(self.plot_data[n], 'Подходящая область')
                self.plot_legends[n].addItem(self.plot_outline[n], 'Контур подходящей области')
                self.plot_legends[n].addItem(self.plot_stations[n], 'Маяки')
                self.plot_legends[n].setZValue(1)
        else:
            self.graph[n].scene().removeItem(self.plot_legends[n])
            self.plot_legends[n] = None

    def _upd_legend(self, n: int) -> None:
        """Обновить состояние легенды на графике.

        :param n: номер графика от 0 до 2
        :type n: int
        """
        self._set_legend_on_graph(n, self.checkboxes_leg[n].isChecked())

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
        self.plot_data[n].setData(X, Y)
        self.plot_outline[n].setData(Xout, Yout)
        self.plot_stations[n].setData(Xm, Ym)
    
    def _calc_vector_magnitude(self, v: list[float, float]) -> float:
        """Расчет модуля двумерного вектора

        :param v: двумерный вектор
        :type v: list[float, float]

        :return: модуль вектора
        :rtype: float
        """
        return math.sqrt(v[0]**2 + v[1]**2)
    
    def _calc_dot_product(self, v1: list[float, float],
                          v2: list[float, float]) -> float:
        """Расчет произведения двумерных векторов.

        :param v1: первый двумерный вектор
        :type v1: list[float, float]
        :param v2: второй двумерный вектор
        :type v2: list[float, float]

        :return: результат произведения векторов
        :rtype: float
        """
        return v1[0] * v2[0] + v1[1] * v2[1]
    
    def _calculate_method_1(self) -> None:
        """Расчет рабочей зоны по первому методу (разностно-дальномерный).
        
        Производит расчет и выводит полученный результат на график. На время
        расчета отключает активные элементы ГПИ.
        """
        # отключение активных элементов
        self._active_elems_enabled(False)

        # координаты
        X1, Y1 = self.doubleSpinBox_x1_m_1.value(), self.doubleSpinBox_y1_m_1.value()
        X2, Y2 = self.doubleSpinBox_x2_m_1.value(), self.doubleSpinBox_y2_m_1.value()
        # параметры погрешностей
        sigma_r_allow = self.doubleSpinBox_sigma_d_m_1.value()
        sigma_t = self.doubleSpinBox_sigma_r_m_1.value()
        # параметры разбиения 
        P = self.spinBox_p_m_1.value()
        r = self.doubleSpinBox_r_m_1.value()

        # сам расчет
        coord_x = []
        coord_y = []
        coord_outline_x = []
        coord_outline_y = []

        for j in range(1, 3601):
            flag_not_first_iter = False
            flag_in_good_area = False
            angle = j * 0.1 * math.pi / 180
            for i in range(1, int(P) + 1):
                mx = math.sin(angle) * (i * r)
                my = math.cos(angle) * (i * r)
                
                # получение векторов
                m0 = [0 - mx, 0 - my]
                v1 = [X1 - mx, Y1 - my]
                v2 = [X2 - mx, Y2 - my]
                
                dot_m0_v1 = self._calc_dot_product(m0, v1) / (self._calc_vector_magnitude(m0) * self._calc_vector_magnitude(v1))
                dot_m0_v2 = self._calc_dot_product(m0, v2) / (self._calc_vector_magnitude(m0) * self._calc_vector_magnitude(v2))
                
                psi1 = math.acos(max(-1, min(1, dot_m0_v1)))
                psi2 = math.acos(max(-1, min(1, dot_m0_v2)))
                
                try:
                    Kr = math.sqrt(math.sin(psi1 / 2)**2 + math.sin(psi2 / 2)**2) / (2 * math.sin((psi1 + psi2) / 2) * math.sin(psi1/2) * math.sin(psi2/2))
                except ZeroDivisionError:
                    Kr = sigma_r_allow / sigma_t + 1
                
                # условие "подходящести" точки и проверка на краевые точки
                if Kr < sigma_r_allow / sigma_t:
                    if flag_not_first_iter and not flag_in_good_area:
                        coord_outline_x.append(mx)
                        coord_outline_y.append(my)
                    else:
                        coord_x.append(mx)
                        coord_y.append(my)
                    flag_in_good_area = True

                else:
                    if flag_not_first_iter and flag_in_good_area:
                        coord_outline_x.append(coord_x[-1])
                        coord_outline_y.append(coord_y[-1])
                        coord_x.pop(-1)
                        coord_y.pop(-1)
                    flag_in_good_area = False

                flag_not_first_iter = True
        
        # обновление графика и включение активных элементов
        self._upd_graph(0, 
                        coord_x, coord_y,
                        coord_outline_x, coord_outline_y,
                        [0, X1, X2], [0, Y1, Y2])
        self._active_elems_enabled(True)

    def _calculate_method_2(self) -> None:
        """Расчет рабочей зоны по второму методу (дальномерный).
        
        Производит расчет и выводит полученный результат на график. На время
        расчета отключает активные элементы ГПИ.
        """
        # отключение активных элементов
        self._active_elems_enabled(False)

        # координаты
        A1, A2 = self.doubleSpinBox_x1_m_2.value(), self.doubleSpinBox_y1_m_2.value()
        B1, B2 = self.doubleSpinBox_x2_m_2.value(), self.doubleSpinBox_y2_m_2.value()
        A = [A1, A2]
        B = [B1, B2]
        # параметры погрешностей
        sigma_d = self.doubleSpinBox_sigma_d_m_2.value()
        sigma_r = self.doubleSpinBox_sigma_r_m_2.value()
        # параметры разбиения 
        P = self.spinBox_p_m_2.value()
        r = self.doubleSpinBox_r_m_2.value()

        sina = math.sqrt(2) * sigma_r/sigma_d       # sin(alpha) = 2^1/2 * sigma/sigma

        # сам расчет
        coord_x = []
        coord_y = []
        coord_outline_x = []
        coord_outline_y = []

        for j in range(1, 3601):
            flag_not_first_iter = False
            flag_in_good_area = False
            angle = j * 0.1 * math.pi / 180             # alpha = j * 0.1 pi/180
            for i in range(1, int(P) + 1):
                M = [math.cos(angle) * (i * r), math.sin(angle) * (i * r)]
                MB = [B[0] - M[0], B[1] - M[1]]
                MA = [A[0] - M[0], A[1] - M[1]]
                
                COS_alpha = self._calc_dot_product(MA, MB) / (self._calc_vector_magnitude(MA) * self._calc_vector_magnitude(MB))
                SIN_alpha = math.sqrt(1 - COS_alpha**2)

                # условие "подходящести" точки и проверка на краевые точки
                if SIN_alpha >= sina:
                    if flag_not_first_iter and not flag_in_good_area:
                        coord_outline_x.append(M[0])
                        coord_outline_y.append(M[1])
                    else:
                        coord_x.append(M[0])
                        coord_y.append(M[1])
                    flag_in_good_area = True

                else:
                    if flag_not_first_iter and flag_in_good_area:
                        coord_outline_x.append(coord_x[-1])
                        coord_outline_y.append(coord_y[-1])
                        coord_x.pop(-1)
                        coord_y.pop(-1)
                    flag_in_good_area = False

                flag_not_first_iter = True

        # обновление графика и включение активных элементов
        self._upd_graph(1,
                        coord_x, coord_y,
                        coord_outline_x, coord_outline_y,
                        [A1, B1], [A2, B2])
        self._active_elems_enabled(True)

    def _calculate_method_3(self) -> None:
        """Расчет рабочей зоны по третьему методу (угломерный).
        
        Производит расчет и выводит полученный результат на график. На время
        расчета отключает активные элементы ГПИ.
        """
        # отключение активных элементов
        self._active_elems_enabled(False)

        # координаты
        A1, A2 = self.doubleSpinBox_x1_m_3.value(), self.doubleSpinBox_y1_m_3.value()
        B1, B2 = self.doubleSpinBox_x2_m_3.value(), self.doubleSpinBox_y2_m_3.value()
        A = [A1, A2]
        B = [B1, B2]
        # параметры погрешностей
        sigma_d = self.doubleSpinBox_sigma_d_m_3.value()
        sigma_theta = self.doubleSpinBox_sigma_r_m_3.value()
        # параметры разбиения 
        P = self.spinBox_p_m_3.value()
        r = self.doubleSpinBox_r_m_3.value()

        d_AB = math.sqrt((A1-B1)**2 + (A2-B2)**2) # расстояние между A и B

        # сам расчет
        coord_x = []
        coord_y = []
        coord_outline_x = []
        coord_outline_y = []

        for j in range(1, 3601):
            flag_not_first_iter = False
            flag_in_good_area = False
            angle = j * 0.1 * math.pi / 180             # alpha = j * 0.1 pi/180
            for i in range(1, int(P) + 1):
                M = [math.cos(angle) * (i * r), math.sin(angle) * (i * r)]
                MB = [B[0] - M[0], B[1] - M[1]]
                MA = [A[0] - M[0], A[1] - M[1]]
                
                COS_alpha = self._calc_dot_product(MA, MB) / (self._calc_vector_magnitude(MA) * self._calc_vector_magnitude(MB))
                SIN_alpha = math.sqrt(1 - COS_alpha**2)
                
                if SIN_alpha != 0:
                    rA = self._calc_vector_magnitude(MA)
                    rB = self._calc_vector_magnitude(MB)
                    Kr = 0.017/SIN_alpha * math.sqrt((rA/d_AB)**2 + (rB/d_AB)**2)

                    # условие "подходящести" точки и проверка на краевые точки
                    if Kr <= sigma_d/(d_AB*sigma_theta):
                        if flag_not_first_iter and not flag_in_good_area:
                            coord_outline_x.append(M[0])
                            coord_outline_y.append(M[1])
                        else:
                            coord_x.append(M[0])
                            coord_y.append(M[1])
                        flag_in_good_area = True

                    else:
                        try:
                            if flag_not_first_iter and flag_in_good_area:
                                coord_outline_x.append(coord_x[-1])
                                coord_outline_y.append(coord_y[-1])
                                coord_x.pop(-1)
                                coord_y.pop(-1)
                        except IndexError:
                            pass
                        flag_in_good_area = False

                    flag_not_first_iter = True

        # обновление графика и включение активных элементов
        self._upd_graph(2,
                        coord_x, coord_y,
                        coord_outline_x, coord_outline_y,
                        [A1, B1], [A2, B2])
        self._active_elems_enabled(True)


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
