from PyQt5 import QtCore, QtWidgets, QtSql
import sys

def addRecord():
    stm.insertRow(stm.rowCount())
   
def delRecord():
    stm.removeRow(tv.currentIndex().row())
    stm.select()

def UpdTbl():
    stm.select()



app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("QSqlTableModel")
# Устанавливаем соединение с базой данных
con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
con.setDatabaseName('db_measure.db')
con.open()
# Создаем модель
stm = QtSql.QSqlTableModel(parent=window)
stm.setTable('tb_measure_instr')
stm.select()
# Задаем заголовки для столбцов модели
stm.setHeaderData(0, QtCore.Qt.Horizontal, 'Наименование \nизмеряемого \nприбора')
stm.setHeaderData(1, QtCore.Qt.Horizontal, 'тип \nизмерямого \nприбора(инструмента)')
stm.setHeaderData(2, QtCore.Qt.Horizontal, 'ошибка \nизмерения')
# Задаем для таблицы только что созданную модель
vbox = QtWidgets.QVBoxLayout()
tv = QtWidgets.QTableView()
tv.setModel(stm)
tv.setColumnWidth(0, 300)
tv.setColumnWidth(1, 300)
tv.setColumnWidth(2, 300)
vbox.addWidget(tv)

btnAdd = QtWidgets.QPushButton("&Добавить запись")
btnAdd.clicked.connect(addRecord)
vbox.addWidget(btnAdd)

stm.select()
    

btnDel = QtWidgets.QPushButton("&Удалить запись")
btnDel.clicked.connect(delRecord)
vbox.addWidget(btnDel)

btnUpd = QtWidgets.QPushButton("&Обновить таблицу")
btnUpd.clicked.connect(UpdTbl)
vbox.addWidget(btnUpd)


window.setLayout(vbox)
window.resize(900, 800)
window.show()
sys.exit(app.exec_())