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

def calculate_method_1(X2: float, Y2: float, X3: float, Y3: float,
                       sigma_r_allow: float, sigma_t: float, P: int,
                       r: float) -> GraphDataFrame:
    """Расчет рабочей зоны по первому методу (разностно-дальномерный).
    
    Для обозначения отдельных величин используется математические обозначения в
    соответствии с методом расчета рабочих зон.

    В данном методе используется 3 маяка, первый из которых считается
    расположенным в начале координат.

    :param X2: координата X второго маяка
    :type X2: float
    :param Y2: координата Y второго маяка
    :type Y2: float
    :param X3: координата X третьего маяка
    :type X3: float
    :param Y3: координата Y третьего маяка
    :type Y3: float
    :param sigma_r_allow: допустимая радиальная ошибка
    :type sigma_r_allow: float
    :param sigma_t: значение радиальной ошибки
    :type sigma_t: float
    :param P: число отсчетов
    :type P: int
    :param r: величина шага
    :type r: float

    :return: кадр данных для графика
    :rtype: GraphDataFrame
    """
    # вспомогательные данные
    sigma_ratio = sigma_r_allow / sigma_t if sigma_t else float('inf')

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
            mx = math.sin(angle) * (i * r)
            my = math.cos(angle) * (i * r)
            
            # получение векторов
            m0 = [0 - mx, 0 - my]
            v1 = [X2 - mx, Y2 - my]
            v2 = [X3 - mx, Y3 - my]
            
            # расчет коэффициента
            dot_m0_v1 = dot_to_mag_prod(m0, v1)
            dot_m0_v2 = dot_to_mag_prod(m0, v2)
            
            psi1 = math.acos(max(-1, min(1, dot_m0_v1)))
            psi2 = math.acos(max(-1, min(1, dot_m0_v2)))
            
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
                    coord_outline_x.append(mx)
                    coord_outline_y.append(my)
                else:
                    coord_x.append(mx)
                    coord_y.append(my)
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
        [0, X2, X3], [0, Y2, Y3]
    )
    return return_data

def calculate_method_2(A1: float, A2: float, B1: float, B2: float,
                       sigma_d: float, sigma_r: float, P: int,
                       r: float) -> GraphDataFrame:
    """Расчет рабочей зоны по второму методу (дальномерный).

    Для обозначения отдельных величин используется математические обозначения в
    соответствии с методом расчета рабочих зон.

    :param A1: координата X первого маяка
    :type A1: float
    :param A2: координата Y первого маяка
    :type A2: float
    :param B1: координата X второго маяка
    :type B1: float
    :param B2: координата Y второго маяка
    :type B2: float
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
    A = [A1, A2]
    B = [B1, B2]
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
            M = [math.cos(angle) * (i * r), math.sin(angle) * (i * r)]

            # векторы
            MB = [B[0] - M[0], B[1] - M[1]]
            MA = [A[0] - M[0], A[1] - M[1]]
            
            # расчет косинуса и синуса
            COS_alpha = dot_to_mag_prod(MA, MB)
            if COS_alpha > 1:
                COS_alpha = 1
            elif COS_alpha < -1:
                COS_alpha = -1
            SIN_alpha = math.sqrt(1 - COS_alpha**2)

            # условие "подходящести" точки, проверка на краевые точки и
            # добавление таковой в соответствующий список
            if SIN_alpha >= sina:
                if flag_not_first_iter and not flag_in_good_area:
                    coord_outline_x.append(M[0])
                    coord_outline_y.append(M[1])
                else:
                    coord_x.append(M[0])
                    coord_y.append(M[1])
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
        [A1, B1], [A2, B2]
    )
    return return_data

def calculate_method_3(A1: float, A2: float, B1: float, B2: float,
                       sigma_d: float, sigma_theta: float, P: int,
                       r: float) -> GraphDataFrame:
    """Расчет рабочей зоны по третьему методу (угломерный).

    Для обозначения отдельных величин используется математические обозначения в
    соответствии с методом расчета рабочих зон.

    :param A1: координата X первого маяка
    :type A1: float
    :param A2: координата Y первого маяка
    :type A2: float
    :param B1: координата X второго маяка
    :type B1: float
    :param B2: координата Y второго маяка
    :type B2: float
    :param sigma_d: допустимая угловая ошибка
    :type sigma_d: float
    :param sigma_theta: значение угловой ошибки
    :type sigma_theta: float
    :param P: число отсчетов
    :type P: int
    :param r: величина шага
    :type r: float

    :return: кадр данных для графика
    :rtype: GraphDataFrame
    """
    # вспомогательные данные
    A = [A1, A2]
    B = [B1, B2]

    d_AB = math.sqrt((A1 - B1)**2 + (A2 - B2)**2)  # расстояние между A и B
    if not d_AB:
        return_data = GraphDataFrame(
            [], [], [], [],
            [A1, B1], [A2, B2]
        )
        return return_data

    sigma_ratio = sigma_d / (d_AB * sigma_theta) if sigma_theta else float('inf')

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
            M = [math.cos(angle) * (i * r), math.sin(angle) * (i * r)]

            # векторы
            MB = [B[0] - M[0], B[1] - M[1]]
            MA = [A[0] - M[0], A[1] - M[1]]
            
            # расчет косинуса и синуса
            COS_alpha = dot_to_mag_prod(MA, MB)
            if COS_alpha > 1:
                COS_alpha = 1
            elif COS_alpha < -1:
                COS_alpha = -1
            SIN_alpha = math.sqrt(1 - COS_alpha**2)
            
            if SIN_alpha:
                rA = vector_magnitude(MA)
                rB = vector_magnitude(MB)
                Kr = 0.017 / SIN_alpha * math.sqrt((rA / d_AB)**2 + (rB / d_AB)**2)

                # условие "подходящести" точки, проверка на краевые точки и
                # добавление таковой в соответствующий список
                if Kr <= sigma_ratio:
                    if flag_not_first_iter and not flag_in_good_area:
                        coord_outline_x.append(M[0])
                        coord_outline_y.append(M[1])
                    else:
                        coord_x.append(M[0])
                        coord_y.append(M[1])
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
        [A1, B1], [A2, B2]
    )
    return return_data

if __name__ == "__main__":
    print(__doc__)
    input('Введите Enter, чтобы выйти.')
