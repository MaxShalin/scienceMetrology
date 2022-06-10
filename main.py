import sys
from sql_lite import SQLighter
from PyQt5 import QtWidgets, uic
from expression import *


db = SQLighter() #подключаем базу двнных db_measure.db

class Ui_dialog(QtWidgets.QDialog):
    """Класс диалогового окна с предупреждением в случае неправильных введеных данных"""
    def __init__(self):
        super(Ui_dialog, self).__init__()
        uic.loadUi('qt_forms/dialog.ui', self)                    #загрузка файла интерфейса диалогового окна
        self.dialog_button.clicked.connect(self.close_dialog)     #нажатие кнопки 'понятно'

    def close_dialog(self) -> None:
        self.close()
        
class Ui(QtWidgets.QMainWindow):
    """Класс основного окна программы"""
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi('qt_forms/main_form.ui', self)                                           #загрузка файла интерфейса основного окна
        #установка возможных значений бокса наименования контролируемых параметров 
        self.name_parameters.addItem("")                                                    #первый параметр пустой
        self.name_parameters.addItems(db.get_parameters())                                  #следующие параметры из БД
        #установка возможныхзначений наименований СИ
        self.name_measure_instr.addItem("")                                                 #первый параметр пустой
        self.name_measure_instr.addItems(db.get_valid_name_measure_instr())                 #следующие параметры из БД
        #установка возможных значений типов СИ от выбранного наименования СИ
        self.name_measure_instr.currentIndexChanged.connect(self.change_type_measure_instr) #при изменении наименования СИ изменяются типы СИ
        self.pushButton.clicked.connect(self.recall)                                        #нажатие кнопки провести оценку
        self.show()

    def change_type_measure_instr(self) -> None:
        """Метод формирования списка типов СИ от их наименования через БД"""
        self.type_measure_instr.clear()                                                     #очистка бокса тип СИ
        select_name_measure_instr = self.name_measure_instr.currentText()                   #получение значения выбранного наименования СИ
        list_type_measure_instr = db.get_type_measure_instr(select_name_measure_instr)      #получение из БД списка всех типов относящихся к выбранному наименованию СИ
        self.type_measure_instr.addItem("")                                                 #первый параметр пустой
        self.type_measure_instr.addItems(list_type_measure_instr)                           #установка списка в бокс тип СИ
     
    def recall(self) -> None:
        """Метод рассчета суммарной погрешности измерений и точности по нажатию кнопки 'Проыести оценку'."""
        #сбор всех значений из интерфейса
        name_parameters = self.name_parameters.currentText()
        tolerance = self.tolerance.text()
        nominal_value = self.nominal_value.text()
        name_measure_instr = self.name_measure_instr.currentText()
        type_measure_instr= self.type_measure_instr.currentText()
        #проверка условий, что все поля заполнены
        if name_parameters != "" and tolerance and nominal_value and name_measure_instr != "" and type_measure_instr != "":
            try:
                tolerance = float(tolerance)                                     #преобразование значения допускаемого отклониия типа строка в тип плавующая точка 
                nominal_value = float(nominal_value)                             #тоже для номинального значения
            except:                                                              #если введены недоустимые значения отклонения и номенального значения (буквы и т.д)
                self.dialog_warning('Не корректно введены значения\n\
                                     номинального значения\n\
                                     или допускаемого отклонения')
                return

            dict_error_measure = db.get_error_measure_instr(type_measure_instr)  #описание в модуле sql-lite.py
            dict_param_error_measure = dict_error_measure.get(name_parameters)   #получение словаря (структуры) МХ СИ по контролируему параметру

            if not dict_param_error_measure:                                                       #если такого параметра нет
                self.dialog_warning(f'Выбранный тип СИ не обеспечивает {name_parameters.lower()}') #вызов диалогового окна с предупреждением 
                return

            error = calculate_error_maesure(dict_param_error_measure, nominal_value)  #описание в модуле expression.py

            if not error:                                                                          #если номинальное значение выходит за диапазон 
                self.dialog_warning(f'Номинальное значение выходит за диапазон СИ')                #вызов диалогового окна с предупреждением 
                return

            self.error_measure.setText(str(error))                                    #установка в поле 'суммарная погреность' полученного значения 
            accuracy = calculate_accuracy(tolerance, error)                           #описание в модуле expression.py
            self.accuracy.setText(str(accuracy))                                      #установка в поле 'показатель точности' полученного значения
        #если какое-то поле основного окнане заполнено 
        else:                                                                      
            self.dialog_warning('Не корректно введены данные')                        #вызов диалогового окна с предупреждением 
                    
    def dialog_warning(self, text_warning: str) -> None:
        """Метод вызова диалогового окна с предупреждением.
        
        text_warning - отображаемое сообщение"""
        dialog = Ui_dialog()
        dialog.messege.setText(text_warning)  #установка отображаемого сообщения
        dialog.exec_()                        #запуск класса

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()



