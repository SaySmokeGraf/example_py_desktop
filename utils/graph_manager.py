"""Модуль с менеджером графика."""

from dataclasses import dataclass

import pyqtgraph as pgraph


@dataclass(eq=False)
class GraphDataFrame:
    """Класс кадра данных на графике.
    
    :param X: список координат X подходящих точек
    :type X: list[float]
    :param Y: список координат Y подходящих точек
    :type Y: list[float]
    :param Xout: список координат X контура подходящих точек
    :type Xout: list[float]
    :param Yout: список координат Y контура подходящих точек
    :type Yout: list[float]
    :param Xst: список координат X маяков
    :type Xst: list[float]
    :param Yst: список координат Y маяков
    :type Yst: list[float] 
    """
    X: list[float]
    Y: list[float]
    Xout: list[float]
    Yout: list[float]
    Xst: list[float]
    Yst: list[float]


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

    def update(self, dataframe: GraphDataFrame) -> None:
        """Обновляет данные на графике.

        :param dataframe: кадр данных для графика
        :type dataframe: GraphDataFrame
        """
        self._plot_data.setData(dataframe.X, dataframe.Y)
        self._plot_outline.setData(dataframe.Xout, dataframe.Yout)
        self._plot_stations.setData(dataframe.Xst, dataframe.Yst)

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


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
