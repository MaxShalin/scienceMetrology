import json
import sqlite3


class SQLighter():
    def __init__(self) -> None:
        self.con = sqlite3.connect('db_measure.db')
        self.cur = self.con.cursor()

    def get_parameters(self) -> list:
        '''Получение возможных значений контролируемых параметров'''
        respone = self.cur.execute('SELECT name_parameters FROM tb_parameters').fetchall() #получение кортежа контролируемых параметров
        list_values = [x[0] for x in respone]   #преобразование кортежа контролируемых параметров в список
        
        return list_values
    
    def get_valid_name_measure_instr(self) -> list:
        '''Получение возможных значений наименования СИ'''
        respone = self.cur.execute('SELECT valid_name_measure_instr FROM tb_valid_name_measure_instr').fetchall() #получение кортежа наименований СИ
        list_values = [x[0] for x in respone]   #преобразование наименований СИ в список
        
        return list_values

    def get_type_measure_instr(self, name_measure_instr: str) -> list:
        '''Получение возможных значений типов СИ'''
        respone = self.cur.execute('SELECT type_measure_instr FROM tb_measure_instr WHERE name_measure_instr=?', (name_measure_instr,)).fetchall()
        list_values = [x[0] for x in respone]   #преобразование кортежа типов СИ в список

        return list_values

    def get_error_measure_instr(self, type_measure_instr: str) -> dict:
        '''Получение словаря с погрешностями СИ'''
        respone = self.cur.execute('SELECT error_measure FROM tb_measure_instr WHERE type_measure_instr=?', (type_measure_instr,)).fetchall()
        dict = json.loads(respone[0][0])
        
        return dict

if __name__ == '__main__':
    pass
