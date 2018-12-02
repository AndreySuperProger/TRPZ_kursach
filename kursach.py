from flowMap import *
from createMapWidget import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator


Map = [[NoFlow, NoFlow, NoFlow, Land, Land],
	[NoFlow, West, West, NorthernWest, Land],
	[NoFlow, West, West, NorthernWest, Land],
	[NoFlow, West, West, NorthernWest, Land],
	[NoFlow, West, West, NorthernWest, Land]]
	
PoisonMap = [
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0]]
	
'''Map = [
	[NoFlow, NoFlow, NoFlow],
	[NoFlow, NorthernWest, NoFlow],
	[NoFlow, NoFlow, NoFlow]]
	
PoisonMap = [
	[0, 0, 0],
	[0, 1, 0],
	[0, 0, 0]]'''

class MainWindow(QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.move(300, 300)
		self.setWindowTitle('Прогнозування розповсюдження полютантів')
		
		self.creatorWidget = None
		
		stepBtn = QPushButton("Крок", self)
		stepBtn.move(20, 20)
		
		createMapBtn = QPushButton("Створити карту", self)
		createMapBtn.move(20, 50)
		createMapBtn.clicked.connect(self.createMapWidgetSlot)
		
		#Карта:
		self.mainFlowMap = FlowMap((150, 20), (len(Map), len(Map[0])),
			Map, PoisonMap, self, 10, 10, 50)
		stepBtn.clicked.connect(self.mainFlowMap.step)
		
	def createMapWidgetSlot(self):
		self.creatorWidget = CreateMapWidget(self)
		self.hide()
		
	def creatorWidgetOkBtnSlot(self):
		self.mainFlowMap.copy(self.creatorWidget.flowMap)
		self.creatorWidget.close()
		self.show()
	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	mainWindow = MainWindow()
	
	mainWindow.show()
	sys.exit(app.exec_())
