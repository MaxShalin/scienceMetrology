"""
Модуль с функциями для рассчета значений оценки единства измерений и достоверности контроля параметров
"""


def calculate_error_maesure(error_meassure_dict: dict, nominal_value: float) -> float or bool:
    """Данная функция производит рассчет суммарной погрешности измерений СИ
    на основе номинального значения контролируемого параметра ( nominal_value)
    и метрологических характеристик СИ (error_meassure_dict)."""
    x = nominal_value                          #создание локальной переменной "х" для реализации функции eval
    for value in error_meassure_dict:          #перебор всех диапазонов работы СИ
        if float(value) >= x:                                 #если номинальное значение входит в диапазон
            error =  eval(error_meassure_dict.get(value))      #рассчет суммарной погрешности
            return round(error, 5)
    return False   

def calculate_accuracy(tolerance: float, error_maesure:float) -> float:
    """Расчет фактического значения коэффициента точности."""
    accuracy = abs(tolerance)/abs(error_maesure)
    return round(accuracy,1)

if __name__ == '__main__':
    pass