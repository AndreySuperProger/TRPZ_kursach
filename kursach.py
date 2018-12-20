from flowMap import *
from createMapWidget import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator


'''Map = [[NoFlow, NoFlow, NoFlow, Land, Land],
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
	
ShipsPositionMap = [
	[1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0]]'''
	
'''Map = [
	[NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow]]
	
PoisonMap = [
	[1, 1, 1],
	[1, 1, 1],
	[1, 1, 1]]
	
ShipsPositionMap = [
	[0, 0, 0],
	[0, 1, 0],
	[0, 0, 0]]'''
	
Map = [
	[NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow],
	[NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow, NoFlow]]
	
PoisonMap = [
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 1, 1, 1, 1]]
	
ShipsPositionMap = [
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0]]

class MainWindow(QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.move(300, 300)
		self.setWindowTitle("Прогнозування розповсюдження полютантів")
		
		self.creatorWidget = None
		self.createMapDialog = None
		
		stepBtn = QPushButton("Крок", self)
		stepBtn.move(20, 20)
		
		createMapBtn = QPushButton("Створити нову карту", self)
		createMapBtn.move(20, 50)
		createMapBtn.clicked.connect(self.createMapWidgetSlot)
		
		editMapBtn = QPushButton("Редагувати карту", self)
		editMapBtn.move(20, 80)
		editMapBtn.clicked.connect(self.editMapWidgetSlot)
		
		#Карта:
		self.mainFlowMap = FlowMap((180, 20), (len(Map), len(Map[0])),
			Map, PoisonMap, ShipsPositionMap, self, 10, 10, 50)
		stepBtn.clicked.connect(self.mainFlowMap.step)
		
	#слот для кнопки "Створити карту"
	def createMapWidgetSlot(self):
		self.createMapDialog = CreateMapDialog(self)
		self.hide()
		
	#слот для кнопки "Редагувати карту"
	def editMapWidgetSlot(self):
		self.creatorWidget = CreateMapWidget(self)
		self.hide()
		
	#Слот для кнопки "Ок" в creatorWidget
	def creatorWidgetOkBtnSlot(self):
		self.mainFlowMap.copy(self.creatorWidget.flowMap)
		self.creatorWidget.close()
		del(self.creatorWidget)
		self.show()
		
	#Слот для кнопки "Ок" в createMapDialog
	def createMapDialogOkBtnClickedSlot(self):
		self.creatorWidget = CreateMapWidget(self, self.createMapDialog)
		self.createMapDialog.close()
		del(self.createMapDialog)
	

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	mainWindow = MainWindow()
	
	mainWindow.show()
	sys.exit(app.exec_())
