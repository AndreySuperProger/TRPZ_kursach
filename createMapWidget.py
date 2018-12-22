from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QDialog
from PyQt5.QtGui import QIntValidator, QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt
from board import *

#Панель пиктограмм
class AreasPanel(QWidget):
	def __init__(self, parentWidget):
		super(AreasPanel, self).__init__(parentWidget)
		
		self.show()

#Диалог о параметрах карты
class CreateMapDialog(QDialog):
	def __init__(self, parent):
		self.parentWidget = parent
		super(CreateMapDialog, self).__init__(parent)
		self.setGeometry(0, 0, 400, 300)
		lbl1 = QLabel("Кількість рядків:", self)
		lbl1.move(20, 20)
		self.rowsEdit = self.addEdit(170, 20)
		
		lbl2 = QLabel("Кількість колонок:", self)
		lbl2.move(20, 60)
		self.colsEdit = self.addEdit(170, 60)
		
		lbl3 = QLabel("Розмір клітинок:", self)
		lbl3.move(20, 100)
		self.areaSizeEdit = self.addEdit(170, 100)
		
		'''lbl4 = QLabel("Інтервал:", self)
		lbl4.move(20, 140)
		self.intervalEdit = self.addEdit(170, 140)
		
		lbl5 = QLabel("Дистанція:", self)
		lbl5.move(20, 180)
		self.distanceEdit = self.addEdit(170, 180)'''
		
		lbl6 = QLabel("Радіус дії кораблів:", self)
		lbl6.move(20, 220)
		self.shipRadEdit = self.addEdit(170, 220)
		
		btn1 = QPushButton("ОК", self)
		btn1.move(20, 260)
		btn1.clicked.connect(self.okBtnSlot)
		
		self.show()
		
	#для создания Edit-ов
	def addEdit(self, x, y):
		editElement = QLineEdit(self)
		editElement.setValidator(QIntValidator())
		editElement.setMaxLength(2)
		editElement.setAlignment(Qt.AlignRight)
		editElement.setFont(QFont("Arial", 20))
		editElement.move(x, y)
		return editElement
		
	def okBtnSlot(self):
		self.hide()
		self.parentWidget.createMapWidget = \
			CreateMapWidget(self.parentWidget, self)
		del(self)

class CreateMapWidget(QWidget):
	def __init__(self, parentWidget, parentDialog = None):
		super(CreateMapWidget, self).__init__()
		#self.setGeometry(400, 400, 500, 600)
		self.move(300, 300)
		self.setWindowTitle('Створити карту')
		self.areaPanelActivePict = None
		self.parentWidget = parentWidget
		
		self.okBtn = QPushButton("Ok", self)
		
		self.board = Board(self, [[(0, 0)]], 20)
		if parentDialog:
			self.createNewMap(parentDialog)
		else:
			self.board.copy(parentWidget.board)
			
		boardWidth = self.board.width()
		boardHeight = self.board.height()
		
		self.okBtn.move(15 + boardWidth, 50)
		self.okBtn.clicked.connect(self.okBtnSlot)
		
		self.show()
	
	def createNewMap(self, parentDialog):
		self.board.hide()
		del(self.board)
		rows = cols = areaSize = 0
		try:
			rows = int(parentDialog.rowsEdit.text())
			print("rows = " + str(rows))
		except:
			rows = 0
		try:
			cols = int(parentDialog.colsEdit.text())
			print("cols = " + str(cols))
		except:
			cols = 0
		try:
			areaSize = int(parentDialog.areaSizeEdit.text())
			print("areaSize = " + str(areaSize))
		except:
			areaSize = 20
		'''self.flowGrid = Grid(self, [[(0, 0) for j in range(cols)] for i in range(raws)])
		self.flowGrid.show()'''
		emptyMap = [[(0, 0) for j in range(cols)] for i in range(rows)]
		self.board = Board(self, emptyMap, areaSize)
		self.okBtn.move(15 + self.board.width(), 50)
		self.hide()
		self.show()
		
	def okBtnSlot(self):
		self.hide()
		self.parentWidget.board.hide()
		self.parentWidget.board.copy(self.board)
		self.parentWidget.board.show()
		boardWidth = self.parentWidget.board.width()
		boardHeight = self.parentWidget.board.height()
		self.parentWidget.stepBtn.move(15 + boardWidth, 50)
		self.parentWidget.flowMapEditBtn.move(15 + boardWidth, 80)
		self.parentWidget.createMapBtn.move(15 + boardWidth, 110)
		self.parentWidget.show()
		del(self)
		
	#слот для обработки кликов на панели пиктограм
	def areaPanelClickedSlot(self):
		'''pictogram = self.sender()
		print("clicked on pict panel " + str(pictogram))
		self.areaPanelActivePict = pictogram'''
		
	#слот для обработки кликов на самой карте
	def flowMapClickedSlot(self):
		'''area = self.sender()
		print("clicked on flowMap " + str(area))
		if self.areaPanelActivePict == None:
			pass
		elif self.areaPanelActivePict.shipIsPresent:
			area.shipIsPresent = True
		elif self.areaPanelActivePict.poisoned:
			area.poisoned = True
		else:
			areasOrientationList = [Land, NoFlow, North, NorthernEast,
				East, SouthernEast, South, SouthernWest, West,
				NorthernWest]
			for item in areasOrientationList:
				if self.areaPanelActivePict.orientation == item:
					area.orientation = item
					if area.poisoned:
						area.poisoned = False
					area.update()'''
		
			
