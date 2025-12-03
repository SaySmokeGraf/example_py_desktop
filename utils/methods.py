"""Модуль с методами расчета рабочих зон."""

import math

from utils.graph_manager import GraphDataFrame


def vector_magnitude(v: list[float, float]) -> float:
    """Расчет модуля двумерного вектора

    :param v: двумерный вектор
    :type v: list[float, float]

    :return: модуль вектора
    :rtype: float
    """
    return math.sqrt(v[0]**2 + v[1]**2)

def dot_product(v1: list[float, float], v2: list[float, float]) -> float:
    """Расчет произведения двумерных векторов.

    :param v1: первый двумерный вектор
    :type v1: list[float, float]
    :param v2: второй двумерный вектор
    :type v2: list[float, float]

    :return: результат произведения векторов
    :rtype: float
    """
    return v1[0] * v2[0] + v1[1] * v2[1]

def dot_to_mag_prod(v1: list[float, float], v2: list[float, float]) -> float:
    """Расчет отношения произведения векторов к произведению их модулей.

    :param v1: первый двумерный вектор
    :type v1: list[float, float]
    :param v2: второй двумерный вектор
    :type v2: list[float, float]

    :return: отношение произведения векторов к произведению их модулей
    :rtype: float
    """
    dot_prod = dot_product(v1, v2)
    mag_prod = vector_magnitude(v1) * vector_magnitude(v2)
    return dot_prod / mag_prod if mag_prod else 0

def calculate_method_1(X1: float, Y1: float, X2: float, Y2: float,
                       sigma_d: float, sigma_r: float,
                       P: int, r: float) -> GraphDataFrame:
    """Расчет рабочей зоны по первому методу (разностно-дальномерный).
    
    Для обозначения отдельных величин используется математические обозначения в
    соответствии с методом расчета рабочих зон.

    В данном методе используется 3 маяка, один из которых считается
    расположенным в начале координат. Таковой обозначим индексом 0 (X0, Y0 и
    т.д.) для сохранения единости обозначений.

    :param X1: координата X первого маяка
    :type X1: float
    :param Y1: координата Y первого маяка
    :type Y1: float
    :param X2: координата X второго маяка
    :type X2: float
    :param Y2: координата Y второго маяка
    :type Y2: float
    :param sigma_d: допустимая радиальная ошибка
    :type sigma_d: float
    :param sigma_r: значение радиальной ошибки
    :type sigma_r: float
    :param P: число отсчетов
    :type P: int
    :param r: величина шага
    :type r: float

    :return: кадр данных для графика
    :rtype: GraphDataFrame
    """
    # вспомогательные данные
    sigma_ratio = sigma_d / sigma_r if sigma_r else float('inf')

    # рассчитываемые данные
    coord_x = []
    coord_y = []
    coord_outline_x = []
    coord_outline_y = []

    # пробежка по углам с шагом 0.1 градуса
    for j in range(1, 3601):
        flag_not_first_iter = False
        flag_in_good_area = False
        angle = j * 0.1 * math.pi / 180

        # пробежка в конкретном углу от начала координат
        for i in range(1, int(P) + 1):
            Xm, Ym = math.sin(angle) * (i * r), math.cos(angle) * (i * r)
            
            v0 = [0 - Xm, 0 - Ym]
            v1 = [X1 - Xm, Y1 - Ym]
            v2 = [X2 - Xm, Y2 - Ym]
            
            # расчет коэффициента
            dot_v0_v1 = dot_to_mag_prod(v0, v1)
            dot_v0_v2 = dot_to_mag_prod(v0, v2)
            
            psi1 = math.acos(max(-1, min(1, dot_v0_v1)))
            psi2 = math.acos(max(-1, min(1, dot_v0_v2)))
            
            u_coef = math.sqrt(math.sin(psi1 / 2)**2 + math.sin(psi2 / 2)**2)
            d_coef = 2 * math.sin((psi1 + psi2) / 2) * math.sin(psi1 / 2) * math.sin(psi2 / 2)
            if d_coef:
                Kr = u_coef / d_coef
            else:
                Kr = float('inf')
            
            # условие "подходящести" точки, проверка на краевые точки и
            # добавление таковой в соответствующий список
            if Kr < sigma_ratio:
                if flag_not_first_iter and not flag_in_good_area:
                    coord_outline_x.append(Xm)
                    coord_outline_y.append(Ym)
                else:
                    coord_x.append(Xm)
                    coord_y.append(Ym)
                flag_in_good_area = True

            else:
                if flag_not_first_iter and flag_in_good_area and coord_x:
                    coord_outline_x.append(coord_x[-1])
                    coord_outline_y.append(coord_y[-1])
                    coord_x.pop()
                    coord_y.pop()
                flag_in_good_area = False

            flag_not_first_iter = True
    
    # сборка и возврат данных
    return_data = GraphDataFrame(
        coord_x, coord_y,
        coord_outline_x, coord_outline_y,
        [0, X1, X2], [0, Y1, Y2]
    )
    return return_data

def calculate_method_2(X1: float, Y1: float, X2: float, Y2: float,
                       sigma_d: float, sigma_r: float,
                       P: int, r: float) -> GraphDataFrame:
    """Расчет рабочей зоны по второму методу (дальномерный).

    Для обозначения отдельных величин используется математические обозначения в
    соответствии с методом расчета рабочих зон.

    :param X1: координата X первого маяка
    :type X1: float
    :param Y1: координата Y первого маяка
    :type Y1: float
    :param X2: координата X второго маяка
    :type X2: float
    :param Y2: координата Y второго маяка
    :type Y2: float
    :param sigma_d: допустимая радиальная ошибка
    :type sigma_d: float
    :param sigma_r: значение радиальной ошибки
    :type sigma_r: float
    :param P: число отсчетов
    :type P: int
    :param r: величина шага
    :type r: float

    :return: кадр данных для графика
    :rtype: GraphDataFrame
    """
    # вспомогательные данные
    sina = math.sqrt(2) * sigma_r / sigma_d if sigma_d else float('inf')

    # рассчитываемые данные
    coord_x = []
    coord_y = []
    coord_outline_x = []
    coord_outline_y = []

    # пробежка по углам с шагом 0.1 градуса
    for j in range(1, 3601):
        flag_not_first_iter = False
        flag_in_good_area = False
        angle = j * 0.1 * math.pi / 180

        # пробежка в конкретном углу от начала координат
        for i in range(1, int(P) + 1):
            Xm, Ym = math.cos(angle) * (i * r), math.sin(angle) * (i * r)

            v1 = [X1 - Xm, Y1 - Ym]
            v2 = [X2 - Xm, Y2 - Ym]
            
            # расчет косинуса и синуса
            COS_alpha = dot_to_mag_prod(v1, v2)
            if COS_alpha > 1:
                COS_alpha = 1
            elif COS_alpha < -1:
                COS_alpha = -1
            SIN_alpha = math.sqrt(1 - COS_alpha**2)

            # условие "подходящести" точки, проверка на краевые точки и
            # добавление таковой в соответствующий список
            if SIN_alpha >= sina:
                if flag_not_first_iter and not flag_in_good_area:
                    coord_outline_x.append(Xm)
                    coord_outline_y.append(Ym)
                else:
                    coord_x.append(Xm)
                    coord_y.append(Ym)
                flag_in_good_area = True

            else:
                if flag_not_first_iter and flag_in_good_area and coord_x:
                    coord_outline_x.append(coord_x[-1])
                    coord_outline_y.append(coord_y[-1])
                    coord_x.pop()
                    coord_y.pop()
                flag_in_good_area = False

            flag_not_first_iter = True
    
    # сборка и возврат данных
    return_data = GraphDataFrame(
        coord_x, coord_y,
        coord_outline_x, coord_outline_y,
        [X1, X2], [Y1, Y2]
    )
    return return_data

def calculate_method_3(X1: float, Y1: float, X2: float, Y2: float,
                       sigma_d: float, sigma_r: float,
                       P: int, r: float) -> GraphDataFrame:
    """Расчет рабочей зоны по третьему методу (угломерный).

    Для обозначения отдельных величин используется математические обозначения в
    соответствии с методом расчета рабочих зон.

    :param X1: координата X первого маяка
    :type X1: float
    :param Y1: координата Y первого маяка
    :type Y1: float
    :param X2: координата X второго маяка
    :type X2: float
    :param Y2: координата Y второго маяка
    :type Y2: float
    :param sigma_d: допустимая угловая ошибка
    :type sigma_d: float
    :param sigma_r: значение угловой ошибки
    :type sigma_r: float
    :param P: число отсчетов
    :type P: int
    :param r: величина шага
    :type r: float

    :return: кадр данных для графика
    :rtype: GraphDataFrame
    """
    # вспомогательные данные
    d_AB = math.sqrt((X1 - X2)**2 + (Y1 - Y2)**2)  # расстояние между маяками
    if not d_AB:
        return_data = GraphDataFrame(
            [], [], [], [],
            [X1, X2], [Y1, Y2]
        )
        return return_data

    sigma_ratio = sigma_d / (d_AB * sigma_r) if sigma_r else float('inf')

    # рассчитываемые данные
    coord_x = []
    coord_y = []
    coord_outline_x = []
    coord_outline_y = []

    # пробежка по углам с шагом 0.1 градуса
    for j in range(1, 3601):
        flag_not_first_iter = False
        flag_in_good_area = False
        angle = j * 0.1 * math.pi / 180

        # пробежка в конкретном углу от начала координат
        for i in range(1, int(P) + 1):
            Xm, Ym = math.cos(angle) * (i * r), math.sin(angle) * (i * r)

            v1 = [X1 - Xm, Y1 - Ym]
            v2 = [X2 - Xm, Y2 - Ym]
            
            # расчет косинуса и синуса
            COS_alpha = dot_to_mag_prod(v1, v2)
            if COS_alpha > 1:
                COS_alpha = 1
            elif COS_alpha < -1:
                COS_alpha = -1
            SIN_alpha = math.sqrt(1 - COS_alpha**2)
            
            if SIN_alpha:
                r1 = vector_magnitude(v1)
                r2 = vector_magnitude(v2)
                Kr = 0.017 / SIN_alpha * math.sqrt((r1 / d_AB)**2 + (r2 / d_AB)**2)

                # условие "подходящести" точки, проверка на краевые точки и
                # добавление таковой в соответствующий список
                if Kr <= sigma_ratio:
                    if flag_not_first_iter and not flag_in_good_area:
                        coord_outline_x.append(Xm)
                        coord_outline_y.append(Ym)
                    else:
                        coord_x.append(Xm)
                        coord_y.append(Ym)
                    flag_in_good_area = True

                else:
                    if flag_not_first_iter and flag_in_good_area and coord_x:
                        coord_outline_x.append(coord_x[-1])
                        coord_outline_y.append(coord_y[-1])
                        coord_x.pop()
                        coord_y.pop()
                    flag_in_good_area = False

                flag_not_first_iter = True
    
    # сборка и возврат данных
    return_data = GraphDataFrame(
        coord_x, coord_y,
        coord_outline_x, coord_outline_y,
        [X1, X2], [Y1, Y2]
    )
    return return_data


if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
