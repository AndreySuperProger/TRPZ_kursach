import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

class Board(QWidget):
	def __init__(self, parent, flowMap, areaSize):
		super(Board, self).__init__(parent)
		rows = len(flowMap)
		cols = len(flowMap[0])
		
		self.setGeometry(10, 10, cols*areaSize, rows*areaSize)
		
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)
		
		self.grid = Grid(self, flowMap, areaSize)
		
		self.particle = Particle(self, 10, 10, 4)
		
		self.show()
		
	def copy(self, boardToCopy):
		self.grid.copy(boardToCopy.grid)
		rows = self.grid.rows
		cols = self.grid.cols
		areaSize = self.grid.areaSize
		self.setGeometry(10, 10, cols*areaSize, rows*areaSize)
		
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
	def __init__(self, parent, flowMap, areaSize):
		super(Grid, self).__init__(parent)
		self.flowMap = flowMap
		self.areaSize = areaSize
		rows = len(flowMap)
		cols = len(flowMap[0])
		self.rows = rows
		self.cols = cols
		self.cellMrx = [[None for j in range(cols)] for i in range(rows)]
		for i in range(rows):
			for j in range(cols):
				x = flowMap[i][j][0]
				y = flowMap[i][j][1]
				self.cellMrx[i][j] = GridCell(self, j, i, areaSize, QPoint(x, y))
				
	def copy(self, gridToCopy):
		del(self.flowMap)
		for i in range(self.rows):
			for j in range(self.cols - 1, -1, -1):
				self.cellMrx[i][j].hide()
				del(self.cellMrx[i][j])
		del(self.cellMrx)
				
		self.flowMap = gridToCopy.flowMap
		self.areaSize = gridToCopy.areaSize
		areaSize = self.areaSize
		rows = len(self.flowMap)
		cols = len(self.flowMap[0])
		self.rows = rows
		self.cols = cols
		
		self.cellMrx = [[None for j in range(cols)] for i in range(rows)]
		for i in range(rows):
			for j in range(cols):
				x = self.flowMap[i][j][0]
				y = self.flowMap[i][j][1]
				self.cellMrx[i][j] = GridCell(self, j, i, self.areaSize, QPoint(x, y))
		self.setGeometry(0, 0, cols*areaSize, rows*areaSize)
		
		
class GridCell(QFrame):
	def __init__(self, parent, j, i, areaSize, vector):
		super(GridCell, self).__init__(parent)
		self.setGeometry(j*areaSize - 10, i*areaSize - 10, areaSize, areaSize)
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
