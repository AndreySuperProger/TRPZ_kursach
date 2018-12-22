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
		
		self.board = Board(self, testMap1, 20)
		boardWidth = self.board.width()
		boardHeight = self.board.height()
		
		self.stepBtn = QPushButton("Крок", self)
		self.stepBtn.move(15 + boardWidth, 50)
		self.stepBtn.clicked.connect(self.board.stepBtnSlot)
		
		self.flowMapEditBtn = QPushButton("Редагувати карту", self)
		self.flowMapEditBtn.move(15 + boardWidth, 80)
		self.flowMapEditBtn.clicked.connect(self.flowMapEditBtnSlot)
		
		self.createMapBtn = QPushButton("Створити нову карту", self)
		self.createMapBtn.move(15 + boardWidth, 110)
		self.createMapBtn.clicked.connect(self.createMapBtnSlot)
		
		self.show()
		
	def flowMapEditBtnSlot(self):
		self.createMapWidget = CreateMapWidget(self)
		self.hide()
		print(self.board.grid.flowMap)
		
	def createMapBtnSlot(self):
		self.createMapDialog = CreateMapDialog(self)
		self.hide()
			

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	mainWindow = MainWindow()
	
	mainWindow.show()
	sys.exit(app.exec_())
