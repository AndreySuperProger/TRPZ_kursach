import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from maps import *

class MainWindow(QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.move(300, 300)
		self.setWindowTitle("Прогнозування розповсюдження полютантів")
		
		board = Board(self)
		
		stepBtn = QPushButton("Крок", self)
		stepBtn.move(520, 50)
		stepBtn.clicked.connect(board.stepBtnSlot)
		
		self.show()
		
class Board(QWidget):
	def __init__(self, parent):
		super(Board, self).__init__(parent)
		self.setGeometry(10, 10, 500, 500)
		
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)
		
		self.grid = Grid(self, testMap1)
		
		self.particle = Particle(self, 10, 10, 4)
		
		self.show()
		
	#TODO: для каждой частицы
	def stepBtnSlot(self):
		x = self.particle.x()
		y = self.particle.y()
		i = int(x/20)
		j = int(y/20)
		dx = self.grid.cellMrx[i][j].vector.x()
		dy = self.grid.cellMrx[i][j].vector.y()
		#TODO: учесть соседние вектора
		self.particle.move(x + dx, y + dy)
		
class Grid(QWidget):
	def __init__(self, parent, flowMap):
		super(Grid, self).__init__(parent)
		rows = len(flowMap)
		cols = len(flowMap[0])
		self.cellMrx = [[None for j in range(cols)] for i in range(rows)]
		for i in range(rows):
			for j in range(cols):
				x = flowMap[i][j][0]
				y = flowMap[i][j][1]
				self.cellMrx[i][j] = GridCell(self, j*20, i*20, QPoint(x, y))
		
class GridCell(QFrame):
	def __init__(self, parent, x, y, vector):
		super(GridCell, self).__init__(parent)
		self.setGeometry(x - 10, y - 10, 20, 20)
		self.vector = vector
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(1)
		qp.setPen(pen)
		qp.setBrush(Qt.red)
		
		qp.drawEllipse(QPoint(10, 10), 1, 1)
		
		qp.drawLine(QPoint(10, 10), QPoint(10 + self.vector.x(), 10 + self.vector.y()))
		
		
#частица пятна
class Particle(QFrame):
	def __init__(self, parent, x, y, rad):
		super(Particle, self).__init__(parent)
		self.rad = rad
		self.setGeometry(x, y, 2*rad, 2*rad)
		self.show()
		
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(1)
		qp.setPen(pen)
		qp.setBrush(Qt.black)
		
		qp.drawEllipse(QPoint(self.rad, self.rad), self.rad - 1, self.rad - 1)
			

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	mainWindow = MainWindow()
	
	mainWindow.show()
	sys.exit(app.exec_())
