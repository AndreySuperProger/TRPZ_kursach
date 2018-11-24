from flowMap import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator

'''
Map = [[NoFlow, NoFlow, NoFlow, Land, Land],
	[NoFlow, West, West, NorthernWest, Land],
	[NoFlow, West, West, NorthernWest, Land],
	[NoFlow, West, West, NorthernWest, Land],
	[NoFlow, West, West, NorthernWest, Land]]'''
	
Map = [
	[NoFlow, NoFlow, NoFlow],
	[NoFlow, NorthernWest, NoFlow],
	[NoFlow, NoFlow, NoFlow]]
	
PoisonMap = [
	[0, 0, 0],
	[0, 1, 0],
	[0, 0, 0]]
	
creatorWidget = None
	
def createMap():
	global creatorWidget
	print('invoking createMap()...')
	creatorWidget = QWidget()
	creatorWidget.setGeometry(400, 400, 500, 600)
	creatorWidget.setWindowTitle('Створити карту')
	
	lbl1 = QLabel("Довжина:", creatorWidget)
	lbl1.move(20, 20)
	lbl2 = QLabel("Ширина:", creatorWidget)
	lbl2.move(20, 60)
	
	rowsEdit = QLineEdit(creatorWidget)
	rowsEdit.setValidator(QIntValidator())
	rowsEdit.setMaxLength(2)
	rowsEdit.setAlignment(Qt.AlignRight)
	rowsEdit.setFont(QFont("Arial",20))
	rowsEdit.move(120, 20)
	
	colsEdit = QLineEdit(creatorWidget)
	colsEdit.setValidator(QIntValidator())
	colsEdit.setMaxLength(2)
	colsEdit.setAlignment(Qt.AlignRight)
	colsEdit.setFont(QFont("Arial",20))
	colsEdit.move(120, 60)
	
	creatorWidget.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	#GUI:
	w = QWidget()
	w.move(300, 300)
	w.setWindowTitle('Прогнозування розповсюдження полютантів')
	
	stepBtn = QPushButton("Крок", w)
	stepBtn.move(20, 20)
	
	createMapBtn = QPushButton("Створити карту", w)
	createMapBtn.move(20, 50)
	createMapBtn.clicked.connect(createMap)
	
    #Карта:
	fm = FlowMap((len(Map), len(Map[0])), Map, PoisonMap, w, 10, 10, 50)
	stepBtn.clicked.connect(fm.step)
	
	w.show()
	sys.exit(app.exec_())
