import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from createMapWidget import *
from maps import *
from board import *

class MainWindow(QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.move(300, 300)
		self.setWindowTitle("Прогнозування розповсюдження полютантів")
		
		self.board = Board(self, testMap1, testMap2, 20)
		self.board.move(280, 10)
		
		self.stepBtn = QPushButton("Крок", self)
		self.stepBtn.move(15, 20)
		self.stepBtn.clicked.connect(self.board.stepBtnSlot)
		
		self.step100Btn = QPushButton("100 кроків", self)
		self.step100Btn.move(15, 50)
		self.step100Btn.clicked.connect(self.board.step100BtnSlot)
		
		self.flowMapEditBtn = QPushButton("Редагувати карту", self)
		self.flowMapEditBtn.move(15, 80)
		self.flowMapEditBtn.clicked.connect(self.flowMapEditBtnSlot)
		
		self.createMapBtn = QPushButton("Створити нову карту", self)
		self.createMapBtn.move(15, 110)
		self.createMapBtn.clicked.connect(self.createMapBtnSlot)
		
		lbl1 = QLabel("Частинок потрапило на узбережжя:", self)
		lbl1.move(15, 240)
		
		self.landParticlesCountLabel = QLabel("   0", self)
		self.landParticlesCountLabel.move(15, 270)
		
		lbl1 = QLabel("Частинок вийшло за межі карти:", self)
		lbl1.move(15, 300)
		
		self.outMapParticlesCountLabel = QLabel("   0", self)
		self.outMapParticlesCountLabel.move(15, 330)
		
		self.show()
		
	def flowMapEditBtnSlot(self):
		self.createMapWidget = CreateMapWidget(self)
		self.hide()
		
	def createMapBtnSlot(self):
		self.createMapDialog = CreateMapDialog(self)
		self.hide()
			

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	mainWindow = MainWindow()
	
	mainWindow.show()
	sys.exit(app.exec_())
