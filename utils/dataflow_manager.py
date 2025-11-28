"""Модуль с менеджером потока данных."""

from typing import Callable, Iterable

from PyQt5.QtWidgets import QCheckBox, QDoubleSpinBox, QSpinBox

from utils.graph_manager import GraphManager


class DataFlowManager:
    """Класс менеджера потока данных.
    
    Предназначен для направления потока данных от источников (элементов ГПИ для
    ввода данных) до графика напрямую (например, вкл/выкл легенду) или через
    промежуточный подсчет (расчет методов). По сути говоря - проводник между
    вводными и выводящими элементами ГПИ; или некая сущность, ставящая их в
    соответствие между собой.
    """
    
    def __init__(self, graph_manager: GraphManager,
                 calc_data_sources: tuple[QDoubleSpinBox | QSpinBox],
                 calc_function: Callable, legend_checkbox: QCheckBox) -> None:
        """Инициализация экземпляра класса.

        :param graph_manager: менеджер графика
        :type graph_manager: GraphManager
        :param calc_data_sources: список источников данных из ГПИ для расчета
        по методу
        :type calc_data_sources: tuple[QDoubleSpinBox | QSpinBox]
        :param calc_function: функция метода расчета рабочей зоны
        :type calc_function: Callable
        :param legend_checkbox: виджет чекбокса наличия легенды
        :type legend_checkbox: QCheckBox
        """
        self._graph_manager = graph_manager
        self._calc_data_sources = calc_data_sources
        self._calc_function = calc_function
        self._legend_checkbox = legend_checkbox
    
    def _calculate(self, data: Iterable[float | int]) -> list[list[float]]:
        """Рассчитать данные для графика по методу.

        :param data: данные для подсчета
        :type data: Iterable[float | int]

        :return: рассчитанные данные
        :rtype: list[list[float]]
        """
        return self._calc_function(*data)
    
    def _get_data(self) -> Iterable[float | int]:
        """Получить данные из источников.

        :return: данные из ГПИ источников
        :rtype: Iterable[float | int]
        """
        return [item.value() for item in self._calc_data_sources]
    
    def plot_method(self) -> None:
        """Построить график по методу."""
        graph_data = self._calculate(self._get_data())
        self._graph_manager.update(*graph_data)
    
    def enable_legend(self) -> None:
        """Включить/выключить легенду."""
        enabled = self._legend_checkbox.isChecked()
        self._graph_manager.enable_legend(enabled)


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
