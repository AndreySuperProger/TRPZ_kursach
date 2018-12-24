import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator, QPainter, QPen, QImage, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint, QRect
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon
import random
import time
import math

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
	
def checkIfPointInsidePolygon(point, array):
	shPoint = ShapelyPoint(point.x(), point.y())
	polygon = ShapelyPolygon([(arrPoint.x(), arrPoint.y()) for arrPoint in array])
	return polygon.contains(shPoint)


class Board(QWidget):
	def __init__(self, parent, flowMap, areaSize):
		super(Board, self).__init__(parent)
		rows = len(flowMap)
		cols = len(flowMap[0])
		
		self.setGeometry(300, 10, cols*areaSize, rows*areaSize)
		
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)
		
		self.grid = Grid(self, flowMap, areaSize)
		
		self.particles = []
		
		self.ships = []
		
		self.lands = []
		
		self.clicked = False
		self.mouse_x1 = 0
		self.mouse_y1 = 0
		self.editFlowPermited = False
		
		self.polygonVertices = []
		self.polygonLines = []
		self.drawPoisonedAreaPermited = False
		
		self.addShipPermited = False
		self.addLandPermited = False
		
		self.show()
		
	def copy(self, boardToCopy):
		self.grid.copy(boardToCopy.grid)
		for particle in self.particles:
			particle.hide()
			del(particle)
		for particleToCopy in boardToCopy.particles:
			self.particles.append(Particle(self, particleToCopy.x,
				particleToCopy.y, particleToCopy.rad))
		for shipToCopy in boardToCopy.ships:
			x = shipToCopy.x
			y = shipToCopy.y
			rad = shipToCopy.cleanRadius
			vel = shipToCopy.velocity
			self.ships.append(Ship(self, x, y, rad, vel))
		for landToCopy in boardToCopy.lands:
			vertices = landToCopy.vertices
			self.lands.append(Land(self, vertices))
		rows = self.grid.rows
		cols = self.grid.cols
		areaSize = self.grid.areaSize
		self.setGeometry(300, 10, cols*areaSize, rows*areaSize)
		
	def stepBtnSlot(self):
		#движение частиц
		for particle in self.particles:
			x = particle.x
			y = particle.y
			i = int(y/self.grid.areaSize)
			j = int(x/self.grid.areaSize)
			#Рассчет поправок:
			k = particle.rad
			dx = dy = 0
			try:
				dx = self.grid.cellMrx[i][j].vector.x()/k
				dy = self.grid.cellMrx[i][j].vector.y()/k
			except:
				pass
			#TODO: учесть соседние вектора(может быть)
			particle.move(x - particle.rad + dx, y - particle.rad + dy)
			particle.x += dx
			particle.y += dy
			#Поподание частиц на землю:
			#TODO: посчитать к-ство
			point = QPoint(particle.x, particle.y)
			for land in self.lands:
				if checkIfPointInsidePolygon(point, land.vertices):
					particle.hide()
					self.particles.remove(particle)
			
		#движение кораблей и очищение воды
		for ship in self.ships:
			if self.particles:
				particleToFollow = min([particle for particle in self.particles],
					key = lambda item:(ship.x - item.x)**2 + (ship.y - item.y)**2)
				dx = particleToFollow.x - ship.x
				dy = particleToFollow.y - ship.y
				l = (dx**2 + dy**2)**0.5
				dx *= ship.velocity/l
				dy *= ship.velocity/l
				#Проверить не упрется ли корабль в землю
				for land in self.lands:
					if checkIfPointInsidePolygon(
						QPoint(ship.x + dx, ship.y + dy), land.vertices):
						dx = dy = 0
				ship.move(ship.x + dx - 20, ship.y + dy - 20)
				ship.x += dx
				ship.y += dy
				
			for i in range(len(self.particles) - 1, -1, -1):
				x1 = ship.x
				y1 = ship.y
				x2 = self.particles[i].x
				y2 = self.particles[i].y
				if ((x2 - x1)**2 + (y2 - y1)**2)**0.5 <= ship.cleanRadius:
					self.particles[i].hide()
					del(self.particles[i])
					
	def step100BtnSlot(self):
		for i in range(100):
			time.sleep(.04)
			self.stepBtnSlot()
			self.repaint()
		
	def mousePressEvent(self, QMouseEvent):
		if self.editFlowPermited:
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
				vector = 0
				try:
					vector = ((x2 - x1)/length*force, (y2 - y1)/length*force)
				except:
					pass
				areaSize = self.grid.areaSize
				
				#TODO: исправить этот дерьмокод
				#Ниже от y1
				for k in range(width):
					point = [x1, y1+k*areaSize/eps0]
					if (x2 > x1 and y2 > y1):
						while point[0] <= x2 and point[1] <= y2:
							try:
								i = int(point[1]/self.grid.areaSize)
								j = int(point[0]/self.grid.areaSize)
								cell = self.grid.cellMrx[i][j]
								cell.vector = QPoint(vector[0], vector[1])
								self.grid.flowMap[i][j] = (vector[0], vector[1])
								cell.update()
								point[0] += vector[0]*areaSize/eps
								point[1] += vector[1]*areaSize/eps
							except:
								pass
					elif (x2 <= x1 and y2 > y1):
						while point[0] >= x2 and point[1] <= y2:
							try:
								i = int(point[1]/self.grid.areaSize)
								j = int(point[0]/self.grid.areaSize)
								cell = self.grid.cellMrx[i][j]
								cell.vector = QPoint(vector[0], vector[1])
								self.grid.flowMap[i][j] = (vector[0], vector[1])
								cell.update()
								point[0] += vector[0]*areaSize/eps
								point[1] += vector[1]*areaSize/eps
							except:
								pass
					elif (x2 > x1 and y2 <= y1):
						while point[0] <= x2 and point[1] >= y2:
							try:
								i = int(point[1]/self.grid.areaSize)
								j = int(point[0]/self.grid.areaSize)
								cell = self.grid.cellMrx[i][j]
								cell.vector = QPoint(vector[0], vector[1])
								self.grid.flowMap[i][j] = (vector[0], vector[1])
								cell.update()
								point[0] += vector[0]*areaSize/eps
								point[1] += vector[1]*areaSize/eps
							except:
								pass
					elif (x2 <= x1 and y2 <= y1):
						while point[0] >= x2 and point[1] >= y2:
							try:
								i = int(point[1]/self.grid.areaSize)
								j = int(point[0]/self.grid.areaSize)
								cell = self.grid.cellMrx[i][j]
								cell.vector = QPoint(vector[0], vector[1])
								self.grid.flowMap[i][j] = (vector[0], vector[1])
								cell.update()
								point[0] += vector[0]*areaSize/eps
								point[1] += vector[1]*areaSize/eps
							except:
								pass
				#Выше от y1
				for k in range(width):
					point = [x1, y1-k*areaSize/eps0]
					if (x2 > x1 and y2 > y1):
						while point[0] <= x2 and point[1] <= y2:
							try:
								i = int(point[1]/self.grid.areaSize)
								j = int(point[0]/self.grid.areaSize)
								cell = self.grid.cellMrx[i][j]
								cell.vector = QPoint(vector[0], vector[1])
								self.grid.flowMap[i][j] = (vector[0], vector[1])
								cell.update()
								point[0] += vector[0]*areaSize/eps
								point[1] += vector[1]*areaSize/eps
							except:
								pass
					elif (x2 <= x1 and y2 > y1):
						while point[0] >= x2 and point[1] <= y2:
							try:
								i = int(point[1]/self.grid.areaSize)
								j = int(point[0]/self.grid.areaSize)
								cell = self.grid.cellMrx[i][j]
								cell.vector = QPoint(vector[0], vector[1])
								self.grid.flowMap[i][j] = (vector[0], vector[1])
								cell.update()
								point[0] += vector[0]*areaSize/eps
								point[1] += vector[1]*areaSize/eps
							except:
								pass
					elif (x2 > x1 and y2 <= y1):
						while point[0] <= x2 and point[1] >= y2:
							try:
								i = int(point[1]/self.grid.areaSize)
								j = int(point[0]/self.grid.areaSize)
								cell = self.grid.cellMrx[i][j]
								cell.vector = QPoint(vector[0], vector[1])
								self.grid.flowMap[i][j] = (vector[0], vector[1])
								cell.update()
								point[0] += vector[0]*areaSize/eps
								point[1] += vector[1]*areaSize/eps
							except:
								pass
					elif (x2 <= x1 and y2 <= y1):
						while point[0] >= x2 and point[1] >= y2:
							try:
								i = int(point[1]/self.grid.areaSize)
								j = int(point[0]/self.grid.areaSize)
								cell = self.grid.cellMrx[i][j]
								cell.vector = QPoint(vector[0], vector[1])
								self.grid.flowMap[i][j] = (vector[0], vector[1])
								cell.update()
								point[0] += vector[0]*areaSize/eps
								point[1] += vector[1]*areaSize/eps
							except:
								pass
				self.clicked = False
			else:
				self.mouse_x1 = QMouseEvent.x()
				self.mouse_y1 = QMouseEvent.y()
				self.clicked = True
				
		elif self.drawPoisonedAreaPermited:
			self.polygonVertices.append(QMouseEvent.pos())
			if (len(self.polygonVertices) > 1):
				p0 = self.polygonVertices[0]
				p1 = self.polygonVertices[-2]
				p2 = self.polygonVertices[-1]
				polygonLocked = abs(p0.x() - p2.x()) <= 5 and abs(p0.y() - p2.y()) <= 5
				if polygonLocked:
					p2 = p0
					#здесь заполнить рандомными точками:
					amount = 50
					maxSize = 10
					try:
						self.generateRandomParticles(amount, maxSize)
					except:
						pass
				x0 = findMinX([p1, p2])
				y0 = findMinY([p1, p2])
				x1 = findMaxX([p1, p2])
				y1 = findMaxY([p1, p2])
				line = Line(self, QRect(QPoint(x0, y0), QPoint(x1, y1)),
					p1, p2)
				self.polygonLines.append(line)
				if polygonLocked:
					self.removeLines()
				
		elif self.addShipPermited:
			x = QMouseEvent.x()
			y = QMouseEvent.y()
			velocity = 10
			rad = 20
			self.ships.append(Ship(self, x, y, rad, velocity))
		
		elif self.addLandPermited:
			self.polygonVertices.append(QMouseEvent.pos())
			if (len(self.polygonVertices) > 1):
				p0 = self.polygonVertices[0]
				p1 = self.polygonVertices[-2]
				p2 = self.polygonVertices[-1]
				polygonLocked = abs(p0.x() - p2.x()) <= 5 and abs(p0.y() - p2.y()) <= 5
				if polygonLocked:
					p2 = p0
					try:
						self.lands.append(Land(self, self.polygonVertices))
					except:
						pass
				x0 = findMinX([p1, p2])
				y0 = findMinY([p1, p2])
				x1 = findMaxX([p1, p2])
				y1 = findMaxY([p1, p2])
				line = Line(self, QRect(QPoint(x0, y0), QPoint(x1, y1)),
					p1, p2)
				self.polygonLines.append(line)
				if polygonLocked:
					self.removeLines()
		
	def generateRandomParticles(self, amount, maxSize):
		x0 = findMinX(self.polygonVertices)
		y0 = findMinY(self.polygonVertices)
		x1 = findMaxX(self.polygonVertices)
		y1 = findMaxY(self.polygonVertices)
		rect = QRect(QPoint(x0, y0), QPoint(x1, y1))
		while amount > 0:
			size = random.randrange(1, maxSize)
			x = random.randrange(rect.topLeft().x(), rect.bottomRight().x())
			y = random.randrange(rect.topLeft().y(), rect.bottomRight().y())
			if checkIfPointInsidePolygon(QPoint(x, y), self.polygonVertices) \
				and size <= maxSize:
				self.particles.append(Particle(self, x, y, size))
				amount -= 1
		
	def removeLines(self):
		for i in range(len(self.polygonLines) - 1, -1, -1):
			self.polygonLines[i].hide()
			del(self.polygonLines[i])
		self.polygonVertices.clear()
		
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
		self.setGeometry(0, 0, cols*areaSize, rows*areaSize)
				
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
		self.setGeometry(j*areaSize, i*areaSize, areaSize, areaSize)
		self.areaSize = areaSize
		self.vector = vector
		#self.arrow = Arrow(self, 10, areaSize)
		self.show()
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(1)
		qp.setPen(pen)
		qp.setBrush(Qt.red)
		
		l = self.areaSize/2
		qp.drawEllipse(QPoint(l, l), 1, 1)
		x = self.vector.x()
		y = self.vector.y()
		vectorLength = (x**2 + y**2)**0.5
		if vectorLength != 0:
			qp.drawEllipse(QPoint(l, l), 1, 1)
			qp.translate(QPoint(l, l))
			if y > 0:
				qp.rotate(-math.atan(x/y)/math.pi * 180)
			elif y < 0:
				qp.rotate(180 - math.atan(x/y)/math.pi * 180)
			elif y == 0:
				if x > 0:
					qp.rotate(-90)
				else:
					qp.rotate(90)
			qp.drawLine(QPoint(0, 0), QPoint(0, vectorLength))
			qp.drawLine(QPoint(0, vectorLength), QPoint(-3, vectorLength -3))
			qp.drawLine(QPoint(0, vectorLength), QPoint(3, vectorLength -3))
		
class Arrow(QFrame):
	def __init__(self, parent, length, areaSize):
		super(Arrow, self).__init__(parent)
		self.setGeometry(0, 0, length, areaSize)
		self.length = length
		self.areaSize = areaSize
		self.show()
	
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(1)
		qp.setPen(pen)
		
		qp.drawLine(QPoint(self.areaSize/2, self.areaSize/2), QPoint(0, self.length))
		
		
#частица пятна
class Particle(QFrame):
	def __init__(self, parent, x, y, rad):
		super(Particle, self).__init__(parent)
		self.x = x
		self.y = y
		self.rad = rad
		self.setGeometry(x - rad, y - rad, 2*rad, 2*rad)
		self.show()
		
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(1)
		qp.setPen(pen)
		qp.setBrush(Qt.black)
		
		qp.drawEllipse(QPoint(self.rad, self.rad), self.rad - 1, self.rad - 1)
		
class Ship(QFrame):
	def __init__(self, parent, x, y, rad, vel):
		super(Ship, self).__init__(parent)
		self.setGeometry(x - 20, y - 20, 40, 40)
		self.x = x
		self.y = y
		self.cleanRadius = rad
		self.velocity = vel
		self.show()
		
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(1)
		qp.setPen(pen)
		qp.drawImage(self.frameRect(), QImage("images/ship.png"))
		
	#TODO: реализовать удаление из карты
	def mousePressEvent(self, QMouseEvent):
		#self.hide()
		#del(self)
		pass
		
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
		
class Land(QFrame):
	def __init__(self, parent, vertices):
		super(Land, self).__init__(parent)
		self.vertices = []
		for item in vertices:
			self.vertices.append(QPoint(item))
		x0 = findMinX(vertices)
		y0 = findMinY(vertices)
		x1 = findMaxX(vertices)
		y1 = findMaxY(vertices)
		self.rect = QRect(QPoint(x0, y0), QPoint(x1, y1))
		'''for item in self.vertices:
			item -= rect.topLeft()'''
		self.setGeometry(self.rect)
		self.show()
		
	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(0)
		qp.setBrush(QColor(Qt.green))
		qp.setPen(pen)
		
		verticesToDraw = [item - self.rect.topLeft() for item in self.vertices]
		polygon = QPolygon(verticesToDraw)
		qp.drawPolygon(polygon)
