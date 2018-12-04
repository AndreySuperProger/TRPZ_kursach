from PyQt5.QtWidgets import QFrame, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QImage
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

#Направление течения в конкретной точке:
Land = -1
NoFlow = 0
North = 1
NorthernEast = 2
East = 3
SouthernEast = 4
South = 5
SouthernWest = 6
West = 7
NorthernWest = 8

#Фрагмент карты
class Area(QFrame):
	clicked = pyqtSignal()
	
	def __init__(self, waterFlow, poisoned, shipIsPresent, parentalWidget):
		super(Area, self).__init__(parentalWidget)
		self.orientation = waterFlow
		self.poisoned = poisoned
		#корабыль-чистильщик
		self.shipIsPresent = shipIsPresent
		
	def refreshColor(self):
		color = 'blue'
		if self.orientation == Land:
			color = 'green'
		elif self.poisoned:
			color = 'brown'
		super(Area, self).setStyleSheet("QWidget { background-color: %s }" %  color)
	
	def paintEvent(self, event):
		self.refreshColor()
		qp = QPainter()
		qp.begin(self)
		pen = QPen()
		pen.setWidth(5)
		qp.setPen(pen)
		
		height = self.frameRect().height()
		width = self.frameRect().width()
		
		if self.shipIsPresent:
			qp.drawImage(self.frameRect(), QImage("images/ship.png"))
		else:
			if self.orientation == NorthernWest:
				qp.drawLine(QPoint(0, 0), QPoint(width, height))
				qp.drawLine(QPoint(0, 0), QPoint(0,	height/3))
				qp.drawLine(QPoint(0, 0), QPoint(width/3, 0))
			elif self.orientation == North:
				qp.drawLine(QPoint(width/2, height), QPoint(width/2, 0))
				qp.drawLine(QPoint(width/2, 0), QPoint(width/4, height/3))
				qp.drawLine(QPoint(width/2, 0), QPoint(3*width/4, height/3))
			elif self.orientation == NorthernEast:
				qp.drawLine(QPoint(width, 0), QPoint(0, height))
				qp.drawLine(QPoint(width, 0), QPoint(width,	height/3))
				qp.drawLine(QPoint(width, 0), QPoint(2*width/3, 0))
			elif self.orientation == East:
				qp.drawLine(QPoint(0, height/2), QPoint(width, height/2))
				qp.drawLine(QPoint(width, height/2), QPoint(3*width/4, height/4))
				qp.drawLine(QPoint(width, height/2), QPoint(3*width/4, 3*height/4))
			elif self.orientation == SouthernEast:
				qp.drawLine(QPoint(0, 0), QPoint(width, height))
				qp.drawLine(QPoint(width, height), QPoint(2*width/3, height))
				qp.drawLine(QPoint(width, height), QPoint(width, 2*height/3))
			elif self.orientation == South:
				qp.drawLine(QPoint(width/2, height), QPoint(width/2, 0))
				qp.drawLine(QPoint(width/2, height), QPoint(width/4, 2*height/3))
				qp.drawLine(QPoint(width/2, height), QPoint(3*width/4, 2*height/3))
			elif self.orientation == SouthernWest:
				qp.drawLine(QPoint(width, 0), QPoint(0, height))
				qp.drawLine(QPoint(0, height), QPoint(width/3, height))
				qp.drawLine(QPoint(0, height), QPoint(0, 2*height/3))
			elif self.orientation == West:
				qp.drawLine(QPoint(0, height/2), QPoint(width, height/2))
				qp.drawLine(QPoint(0, height/2), QPoint(width/4, height/4))
				qp.drawLine(QPoint(0, height/2), QPoint(width/4, 3*height/4))
		qp.end()
		
	def mousePressEvent(self, event):
		self.clicked.emit()

class FlowMap(QWidget):
	def __init__(self, topLeft, size, initial_flowMap, initial_poisonMap,
		initial_shipsPositionMap, parentWidget, distance, interval, area_size):
		super(FlowMap, self).__init__(parentWidget)
		height = (size[0] + 1)*(area_size + distance)
		width = (size[1] + 1)*(area_size + interval)
		self.setGeometry(topLeft[0], topLeft[1], width, height)
		self.rows = size[0]
		self.cols = size[1]
		self.Map = []
		self.parentWidget = parentWidget
		self.distance = distance
		self.interval = interval
		self.area_size = area_size
		for i in range(self.rows):
			self.Map.append([])
			for j in range(self.cols):
				poison = False
				if initial_poisonMap[i][j] == 1:
					poison = True
				ship = False
				if initial_shipsPositionMap[i][j] == 1:
					ship = True
				frame = Area(initial_flowMap[i][j], poison, ship, self)
				self.Map[i].append(frame)
				frame.setGeometry(j*(area_size + distance),
					i*(area_size + interval), area_size, area_size)
				frame.show()
				
	def copy(self, itemToCopy):
		for i in range(self.rows - 1, -1, -1):
			for j in range(self.cols - 1, -1, -1):
				self.Map[i][j].hide()
				del(self.Map[i][j])
			del(self.Map[i])
			
		self.rows = itemToCopy.rows
		self.cols = itemToCopy.cols
		
		self.parentWidget = itemToCopy.parentWidget
		self.distance = itemToCopy.distance
		self.interval = itemToCopy.interval
		self.area_size = itemToCopy.area_size
		
		height = (self.rows + 1)*(self.area_size + self.distance)
		width = (self.cols + 1)*(self.area_size + self.interval)
		self.resize(width, height)
		
		for i in range(self.rows):
			self.Map.append([])
			for j in range(self.cols):
				frameToCopy = itemToCopy.Map[i][j]
				frame = Area(frameToCopy.orientation, frameToCopy.poisoned,
					frameToCopy.shipIsPresent, self)
				self.Map[i].append(frame)
				frame.setGeometry(j*(self.area_size + self.distance),
					i*(self.area_size + self.interval), self.area_size, self.area_size)
				frame.show()
		self.parentWidget.update()
		
	#для createMapWidget
	def bindClickedSignal(self, parentWidget):
		for row in self.Map:
			for frame in row:
				frame.clicked.connect(parentWidget.flowMapClickedSlot)
	
	def step(self):
		poisonedAreas = [(self.Map[i][j], i, j) for i in range(self.rows)
			for j in range(self.cols) if self.Map[i][j].poisoned]
		#рассчитать загрязненные територии на этом шаге
		for areaTuple in poisonedAreas:
			area = areaTuple[0]
			i = areaTuple[1]
			j = areaTuple[2]
			
			areaToPoison = None
			if self.Map[i][j].orientation == North:
				if i > 0:
					areaToPoison = self.Map[i - 1][j]
			elif self.Map[i][j].orientation == NorthernEast:
				if i > 0 and j < self.cols - 1:
					areaToPoison = self.Map[i - 1][j + 1]
			elif self.Map[i][j].orientation == East:
				if j < self.cols - 1:
					areaToPoison = self.Map[i][j + 1]
			elif self.Map[i][j].orientation == SouthernEast:
				if i < self.rows - 1 and j < self.cols - 1:
					areaToPoison = self.Map[i + 1][j + 1]
			elif self.Map[i][j].orientation == South:
				if i < self.rows - 1:
					areaToPoison = self.Map[i + 1][j]
			elif self.Map[i][j].orientation == SouthernWest:
				if i < self.rows - 1 and j > 0:
					areaToPoison = self.Map[i + 1][j - 1]
			elif self.Map[i][j].orientation == West:
				if j > 0:
					areaToPoison = self.Map[i][j - 1]
			elif self.Map[i][j].orientation == NorthernWest:
				if i >= 0 and j > 0:
					areaToPoison = self.Map[i - 1][j - 1]
					
			if areaToPoison:
				areaToPoison.poisoned = True
				
		areasWithShips = [(self.Map[i][j], i, j) for i in range(self.rows)
			for j in range(self.cols) if self.Map[i][j].shipIsPresent]
		#рассчитать куда поплывут корабли
		#TODO: хорошо бы инкапсулировать в отдельный класс
		#TODO: обновить перед этим poisonedAreas
		#TODO: добавить переменный радиус действия кораблей
		for shipTuple in areasWithShips:
			area = shipTuple[0]
			i = shipTuple[1]
			j = shipTuple[2]
			
			if poisonedAreas:
				areaToFollow = min([areaTuple for areaTuple in poisonedAreas],
					key = lambda item: abs(item[1] - i) + abs(item[2] - j))
				areaToFollow_i = areaToFollow[1]
				areaToFollow_j = areaToFollow[2]
				areaToGo = [0, 0]
				if i < areaToFollow_i:
					areaToGo[0] = 1
				elif i > areaToFollow_i:
					areaToGo[0] = -1
				if j < areaToFollow_j:
					areaToGo[1] = 1
				elif j > areaToFollow_j:
					areaToGo[1] = -1
				#areaToGo += [i, j]
				areaToGo[0] += i
				areaToGo[1] += j
				
				area.shipIsPresent = False
				self.Map[areaToGo[0]][areaToGo[1]].shipIsPresent = True
				
				#пересчёт загрезненных областей:
				for i in range(self.rows):
					for j in range(self.cols):
						#радиус
						if (areaToGo[0] - i)**2 + (areaToGo[1] - j)**2 <= 1 \
							and self.Map[i][j].poisoned:
							self.Map[i][j].poisoned = False
