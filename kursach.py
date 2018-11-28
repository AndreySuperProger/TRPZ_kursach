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
	
class CreateMapWidget(QWidget):
	flowMap = None
	rowsEdit = None
	colsEdit = None
	def __init__(self):
		super(CreateMapWidget, self).__init__()
		self.setGeometry(400, 400, 500, 600)
		self.setWindowTitle('Створити карту')
		
		lbl1 = QLabel("Довжина:", self)
		lbl1.move(20, 20)
		lbl2 = QLabel("Ширина:", self)
		lbl2.move(20, 60)
		
		rowsEdit = QLineEdit(self)
		rowsEdit.setValidator(QIntValidator())
		rowsEdit.setMaxLength(2)
		rowsEdit.setAlignment(Qt.AlignRight)
		rowsEdit.setFont(QFont("Arial",20))
		rowsEdit.move(120, 20)
		self.rowsEdit = rowsEdit
		
		colsEdit = QLineEdit(self)
		colsEdit.setValidator(QIntValidator())
		colsEdit.setMaxLength(2)
		colsEdit.setAlignment(Qt.AlignRight)
		colsEdit.setFont(QFont("Arial", 20))
		colsEdit.move(120, 60)
		self.colsEdit = colsEdit
		
		createMapBtn = QPushButton("Створити карту", self)
		createMapBtn.move(20, 100)
		createMapBtn.clicked.connect(lambda:self.createMap())
		
		self.flowMap = FlowMap((400, 20), (2, 2), [[0, 0], [0, 0]],
			[[0, 0], [0, 0]], self, 10, 10, 50)
		
		self.show()
		
	def createMap(self):
		self.flowMap.hide()
		del(self.flowMap)
		rows = int(self.rowsEdit.text())
		cols = int(self.colsEdit.text())
		self.flowMap = FlowMap((400, 20), (rows, cols),
			[[0 for j in range(cols)] for i in range(rows)],
			[[0 for j in range(cols)] for i in range(rows)], self, 10, 10, 50)
		self.flowMap.show()
		
def createMapWidgetSlot():
	global creatorWidget
	creatorWidget = CreateMapWidget()
	

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
	createMapBtn.clicked.connect(createMapWidgetSlot)
	
    #Карта:
	fm = FlowMap((150, 20), (len(Map), len(Map[0])), Map, PoisonMap, w, 10, 10, 50)
	stepBtn.clicked.connect(fm.step)
	
	w.show()
	sys.exit(app.exec_())
