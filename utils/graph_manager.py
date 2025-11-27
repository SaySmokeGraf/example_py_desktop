"""Модуль с менеджером графика."""

import pyqtgraph as pgraph


class GraphManager:
    """Класс менеджера графика."""

    def __init__(self, plot_widget: pgraph.PlotWidget) -> None:
        """Инициализация экземпляра класса.

        Принимает виджет графика, затем настраивает и подготавливает его.

        :param plot_widget: виджет графика
        :type plot_widget: PlotWidget
        """
        self._graph = plot_widget
        self._setup()
    
    def _setup(self) -> None:
        """Настройка графика и подготовка вспомогательных атрибутов."""
        # настройка виджета
        self._graph.setLabel('left', 'Ось Y')
        self._graph.setLabel('bottom', 'Ось X')
        self._graph.showGrid(x=True, y=True)

        # наборы данных на графике
        self._plot_data = self._graph.plot([], [], pen=None,
                    symbol='o', symbolSize=5, symbolPen='b', symbolBrush='b',
                    name='Подходящая область')
        self._plot_outline = self._graph.plot([], [], pen=None,
                    symbol='o', symbolSize=5, symbolPen='k', symbolBrush='k',
                    name='Контур подходящей области')
        self._plot_stations = self._graph.plot([], [], pen=None,
                    symbol='t1', symbolSize=20, symbolPen='r', symbolBrush='r',
                    name='Маяки')
        
        # настройка легенды
        self._graph_legend = None
        self.enable_legend()

    def update(self, X: list[float], Y: list[float],
                     Xout: list[float], Yout: list[float],
                     Xm: list[float], Ym: list[float]) -> None:
        """Обновляет данные на графике.

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
        self._plot_data.setData(X, Y)
        self._plot_outline.setData(Xout, Yout)
        self._plot_stations.setData(Xm, Ym)

    def enable_legend(self, enabled: bool = True) -> None:
        """Включить/выключить легенду на графике.

        :param enabled: флаг включенности легенды, по умолчанию: True
        :type enabled: bool
        """
        if enabled:
            if self._graph_legend is None:
                self._graph_legend = pgraph.LegendItem((80, 60),
                                    offset=(70, 20), frame=True, brush='w')
                self._graph_legend.setParentItem(self._graph.graphicsItem())
                self._graph_legend.addItem(self._plot_data,
                                           'Подходящая область')
                self._graph_legend.addItem(self._plot_outline,
                                           'Контур подходящей области')
                self._graph_legend.addItem(self._plot_stations,
                                           'Маяки')
                self._graph_legend.setZValue(1)
        else:
            if self._graph_legend is not None:
                self._graph.scene().removeItem(self._graph_legend)
                self._graph_legend = None

    @property
    def graph(self) -> pgraph.PlotWidget:
        """Виджет графика.

        :return: виджет графика
        :rtype: PlotWidget
        """
        return self._graph


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
