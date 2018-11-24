from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QPoint

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
	orientation = 0
	poisoned = False
	
	def __init__(self, waterFlow, poisoned, parentalWidget):
		super(Area, self).__init__(parentalWidget)
		self.orientation = waterFlow
		self.poisoned = poisoned
		
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

class FlowMap:
	rows = None
	cols = None
	Map = []
	def __init__(self, size, initial_flowMap, initial_poisonMap,
		parentalWidget, distance, interval, area_size):
		self.size = size
		topLeft = (150, 20)
		self.rows = size[0]
		self.cols = size[1]
		for i in range(self.rows):
			self.Map.append([])
			for j in range(self.cols):
				poison = False
				if initial_poisonMap[i][j] == 1:
					poison = True
				frame = Area(initial_flowMap[i][j], poison, parentalWidget)
				self.Map[i].append(frame)
				frame.setGeometry(topLeft[0] + j*(area_size + distance),
					topLeft[1] + i*(area_size + interval), area_size, area_size)
	
	def step(self):
		if self.rows > 1:	#TODO: определить ситуации, когда rows == 1 или cols == 1
			for i in range(1, self.rows - 1):
				if self.cols > 1:
					for j in range(1, self.cols - 1):
						if self.Map[i][j].poisoned:
							areaToPoison = None
							if self.Map[i][j].orientation == NoFlow or \
								self.Map[i][j].orientation == Land:
								continue
							elif self.Map[i][j].orientation == North:
								areaToPoison = self.Map[i - 1][j]
							elif self.Map[i][j].orientation == NorthernEast:
								areaToPoison = self.Map[i - 1][j + 1]
							elif self.Map[i][j].orientation == East:
								areaToPoison = self.Map[i][j + 1]
							elif self.Map[i][j].orientation == SouthernEast:
								areaToPoison = self.Map[i + 1][j + 1]
							elif self.Map[i][j].orientation == South:
								areaToPoison = self.Map[i + 1][j]
							elif self.Map[i][j].orientation == SouthernWest:
								areaToPoison = self.Map[i + 1][j - 1]
							elif self.Map[i][j].orientation == West:
								areaToPoison = self.Map[i][j - 1]
							elif self.Map[i][j].orientation == NorthernWest:
								areaToPoison = self.Map[i - 1][j - 1]
							areaToPoison.poisoned = True
							areaToPoison.repaint()
