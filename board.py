import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, QRect

def findMinX(array):
		x = 1000
		for item in array:
			if (item.x() < x):
				x = item.x()
		return x
		
def findMaxX(array):
	x = 0
	for item in array:
		if (item.x() > x):
			x = item.x()
	return x
	
def findMinY(array):
	y = 1000
	for item in array:
		if (item.y() < y):
			y = item.y()
	return y
	
def findMaxY(array):
	y = 0
	for item in array:
		if (item.y() > y):
			y = item.y()
	return y


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
		
		self.clicked = False
		self.mouse_x1 = 0
		self.mouse_y1 = 0
		self.editFlowPermited = False
		
		self.polygonVertices = []
		self.polygonLines = []
		self.drawPoisonedAreaPermitted = False
		
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
		
	def mousePressEvent(self, QMouseEvent):
		if (self.editFlowPermited):
			force = 10
			width = 5
			eps0 = 2
			eps = 16
			if self.clicked:
				x1 = self.mouse_x1
				y1 = self.mouse_y1
				x2 = QMouseEvent.x()
				y2 = QMouseEvent.y()
				
				length = ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)
				vector = ((x2 - x1)/length*force, (y2 - y1)/length*force)
				areaSize = self.grid.areaSize
				
				#TODO: исправить этот дерьмокод
				#TODO: добавить try блоки
				#Ниже от y1
				for k in range(width):
					point = [x1, y1+k*areaSize/eps0]
					if (x2 > x1 and y2 > y1):
						while point[0] <= x2 and point[1] <= y2:
							i = int(point[1]/self.grid.areaSize)
							j = int(point[0]/self.grid.areaSize)
							cell = self.grid.cellMrx[i][j]
							cell.vector = QPoint(vector[0], vector[1])
							self.grid.flowMap[i][j] = (vector[0], vector[1])
							cell.update()
							point[0] += vector[0]*areaSize/eps
							point[1] += vector[1]*areaSize/eps
					elif (x2 <= x1 and y2 > y1):
						while point[0] >= x2 and point[1] <= y2:
							i = int(point[1]/self.grid.areaSize)
							j = int(point[0]/self.grid.areaSize)
							cell = self.grid.cellMrx[i][j]
							cell.vector = QPoint(vector[0], vector[1])
							self.grid.flowMap[i][j] = (vector[0], vector[1])
							cell.update()
							point[0] += vector[0]*areaSize/eps
							point[1] += vector[1]*areaSize/eps
					elif (x2 > x1 and y2 <= y1):
						while point[0] <= x2 and point[1] >= y2:
							i = int(point[1]/self.grid.areaSize)
							j = int(point[0]/self.grid.areaSize)
							cell = self.grid.cellMrx[i][j]
							cell.vector = QPoint(vector[0], vector[1])
							self.grid.flowMap[i][j] = (vector[0], vector[1])
							cell.update()
							point[0] += vector[0]*areaSize/eps
							point[1] += vector[1]*areaSize/eps
					elif (x2 <= x1 and y2 <= y1):
						while point[0] >= x2 and point[1] >= y2:
							i = int(point[1]/self.grid.areaSize)
							j = int(point[0]/self.grid.areaSize)
							cell = self.grid.cellMrx[i][j]
							cell.vector = QPoint(vector[0], vector[1])
							self.grid.flowMap[i][j] = (vector[0], vector[1])
							cell.update()
							point[0] += vector[0]*areaSize/eps
							point[1] += vector[1]*areaSize/eps
				#Выше от y1
				for k in range(width):
					point = [x1, y1-k*areaSize/eps0]
					if (x2 > x1 and y2 > y1):
						while point[0] <= x2 and point[1] <= y2:
							i = int(point[1]/self.grid.areaSize)
							j = int(point[0]/self.grid.areaSize)
							cell = self.grid.cellMrx[i][j]
							cell.vector = QPoint(vector[0], vector[1])
							self.grid.flowMap[i][j] = (vector[0], vector[1])
							cell.update()
							point[0] += vector[0]*areaSize/eps
							point[1] += vector[1]*areaSize/eps
					elif (x2 <= x1 and y2 > y1):
						while point[0] >= x2 and point[1] <= y2:
							i = int(point[1]/self.grid.areaSize)
							j = int(point[0]/self.grid.areaSize)
							cell = self.grid.cellMrx[i][j]
							cell.vector = QPoint(vector[0], vector[1])
							self.grid.flowMap[i][j] = (vector[0], vector[1])
							cell.update()
							point[0] += vector[0]*areaSize/eps
							point[1] += vector[1]*areaSize/eps
					elif (x2 > x1 and y2 <= y1):
						while point[0] <= x2 and point[1] >= y2:
							i = int(point[1]/self.grid.areaSize)
							j = int(point[0]/self.grid.areaSize)
							cell = self.grid.cellMrx[i][j]
							cell.vector = QPoint(vector[0], vector[1])
							self.grid.flowMap[i][j] = (vector[0], vector[1])
							cell.update()
							point[0] += vector[0]*areaSize/eps
							point[1] += vector[1]*areaSize/eps
					elif (x2 <= x1 and y2 <= y1):
						while point[0] >= x2 and point[1] >= y2:
							i = int(point[1]/self.grid.areaSize)
							j = int(point[0]/self.grid.areaSize)
							cell = self.grid.cellMrx[i][j]
							cell.vector = QPoint(vector[0], vector[1])
							self.grid.flowMap[i][j] = (vector[0], vector[1])
							cell.update()
							point[0] += vector[0]*areaSize/eps
							point[1] += vector[1]*areaSize/eps	
				self.clicked = False
			else:
				self.mouse_x1 = QMouseEvent.x()
				self.mouse_y1 = QMouseEvent.y()
				self.clicked = True
				
		elif(self.drawPoisonedAreaPermitted):
			if (len(self.polygonVertices) > 0):
				x1 = QMouseEvent.x()
				y1 = QMouseEvent.y()
				x2 = self.polygonVertices[0].x()
				y2 = self.polygonVertices[0].y()
				#если полигон нарисован:
				if (abs(x2 - x1) < 5 and abs(y2 - y1) < 5):
					x01 = findMinX([QPoint(x1, y1), QPoint(x2, y2)])
					y01 = findMinY([QPoint(x1, y1), QPoint(x2, y2)])
					x02 = findMaxX([QPoint(x1, y1), QPoint(x2, y2)])
					y02 = findMaxY([QPoint(x1, y1), QPoint(x2, y2)])
					line = Line(self, QRect(QPoint(x01, y01), QPoint(x02, y02)),
						QPoint(x1, y1), QPoint(x2, y2))
					self.polygonLines.append(line)
			self.polygonVertices.append(QMouseEvent.pos())
			if (len(self.polygonVertices) > 1):
				p0 = self.polygonVertices[-1]
				p1 = self.polygonVertices[-2]
				x0 = findMinX([p0, p1])
				y0 = findMinY([p0, p1])
				x1 = findMaxX([p0, p1])
				y1 = findMaxY([p0, p1])
				line = Line(self, QRect(QPoint(x0, y0), QPoint(x1, y1)),
					p0, p1)
				self.polygonLines.append(line)
		
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
		
class Line(QFrame):
	def __init__(self, parent, rect, p1, p2):
		super(Line, self).__init__(parent)
		self.p1 = p1 - rect.topLeft()
		self.p2 = p2 - rect.topLeft()
		self.setGeometry(rect)
		self.show()
		
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(3)
		qp.setPen(pen)
		
		qp.drawLine(self.p1, self.p2)
		
class Polygon(QFrame):
	def __init__(self, parent, rect, vertices):
		super(Polygon, self).__init__(parent)
		self.vertices = vertices
		for item in self.vertices:
			item -= rect.topLeft()
		self.setGeometry(rect)
		self.show()
		
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(1)
		qp.setPen(pen)
		
		for i in range(len(self.vertices) - 1):
			qp.drawLine(self.vertices[i], self.vertices[i + 1])
		qp.drawLine(self.vertices[-1], self.vertices[0])
