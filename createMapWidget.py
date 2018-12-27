from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QDialog, QSlider
from PyQt5.QtGui import QIntValidator, QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt
from board import *
from maps import *

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
		
		lbl6 = QLabel("Радіус дії кораблів:", self)
		lbl6.move(20, 220)
		self.shipRadEdit = self.addEdit(170, 220)
		
		okBtn = QPushButton("ОК", self)
		okBtn.move(20, 260)
		okBtn.clicked.connect(self.okBtnSlot)
		
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
		self.setWindowTitle('Створити карту')
		self.parentWidget = parentWidget
		
		self.board = Board(self, [[(0, 0)]], [[(0, 0)]], 20)
		
		firstBtnPos = QPoint(15, 0)
		
		createFlowBtn = QPushButton("Задати напрям течії", self)
		createFlowBtn.move(firstBtnPos + QPoint(0, 30))
		createFlowBtn.clicked.connect(self.createFlowBtnSlot)
		
		createWindBtn = QPushButton("Задати напрям вітру", self)
		createWindBtn.move(firstBtnPos + QPoint(150, 30))
		createWindBtn.clicked.connect(self.createWindBtnSlot)
		
		lbl1 = QLabel("Сила вітру/течії:", self)
		lbl1.move(firstBtnPos + QPoint(0, 70))
		self.forceEdit = self.addEdit(firstBtnPos + QPoint(135, 70))
		
		lbl1 = QLabel("Ширина області:", self)
		lbl1.move(firstBtnPos + QPoint(0, 110))
		self.widthEdit = self.addEdit(firstBtnPos + QPoint(135, 110))
		
		addParticlesBtn = QPushButton("Задати область забруднення", self)
		addParticlesBtn.move(firstBtnPos + QPoint(0, 200))
		addParticlesBtn.clicked.connect(self.addParticlesBtnSlot)
		
		lbl1 = QLabel("Кількість частинок:", self)
		lbl1.move(firstBtnPos + QPoint(0, 240))
		self.amountEdit = self.addEdit(firstBtnPos + QPoint(135, 240))
		
		lbl1 = QLabel("Максимальний\nрозмір частинок:", self)
		lbl1.move(firstBtnPos + QPoint(0, 280))
		self.sizeEdit = self.addEdit(firstBtnPos + QPoint(135, 280))
		
		addShipBtn = QPushButton("Додати корабель", self)
		addShipBtn.move(firstBtnPos + QPoint(0, 400))
		addShipBtn.clicked.connect(self.addShipBtnSlot)
		
		lbl1 = QLabel("Радіус дії корабля:", self)
		lbl1.move(firstBtnPos + QPoint(0, 440))
		self.radiusEdit = self.addEdit(firstBtnPos + QPoint(135, 440))
		
		lbl1 = QLabel("Швидкість корабля:", self)
		lbl1.move(firstBtnPos + QPoint(0, 490))
		self.velocityEdit = self.addEdit(firstBtnPos + QPoint(135, 490))
		
		addLandBtn = QPushButton("Додати землю", self)
		addLandBtn.move(firstBtnPos + QPoint(0, 560))
		addLandBtn.clicked.connect(self.addLandBtnSlot)
		
		self.okBtn = QPushButton("Ok", self)
		self.okBtn.move(firstBtnPos + QPoint(135, 560))
		self.okBtn.clicked.connect(self.okBtnSlot)
		
		if parentDialog:
			self.createNewMap(parentDialog)
		else:
			self.board.copy(parentWidget.board)
		self.board.move(400, 10)
		
		self.show()
		
	'''def addEdit(self, x, y):
		editElement = QLineEdit(self)
		editElement.setValidator(QIntValidator())
		editElement.setMaxLength(2)
		editElement.setAlignment(Qt.AlignRight)
		editElement.setFont(QFont("Arial", 20))
		editElement.move(x, y)
		return editElement'''
		
	def addEdit(self, p):
		editElement = QLineEdit(self)
		editElement.setValidator(QIntValidator())
		editElement.setMaxLength(2)
		editElement.setAlignment(Qt.AlignRight)
		editElement.setFont(QFont("Arial", 20))
		editElement.move(p)
		return editElement
	
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
		self.board = Board(self, emptyMap, emptyMap, areaSize)
		self.hide()
		self.show()
		
	def okBtnSlot(self):
		self.hide()
		self.parentWidget.board.hide()
		self.parentWidget.board.copy(self.board)
		self.parentWidget.board.show()
		self.parentWidget.show()
		del(self)
		
	def createFlowBtnSlot(self):
		self.board.editFlowPermited = True
		self.board.editWindPermited = False
		self.board.drawPoisonedAreaPermited = False
		self.board.addShipPermited = False
		self.board.addLandPermited = False
		
	def createWindBtnSlot(self):
		self.board.editFlowPermited = False
		self.board.editWindPermited = True
		self.board.drawPoisonedAreaPermited = False
		self.board.addShipPermited = False
		self.board.addLandPermited = False
		
	def addParticlesBtnSlot(self):
		self.board.drawPoisonedAreaPermited = True
		self.board.editFlowPermited = False
		self.board.editWindPermited = False
		self.board.addShipPermited = False
		self.board.addLandPermited = False
		
	def addShipBtnSlot(self):
		self.board.drawPoisonedAreaPermited = False
		self.board.editFlowPermited = False
		self.board.editWindPermited = False
		self.board.addShipPermited = True
		self.board.addLandPermited = False
		
	def addLandBtnSlot(self):
		self.board.drawPoisonedAreaPermited = False
		self.board.editFlowPermited = False
		self.board.editWindPermited = False
		self.board.addShipPermited = False
		self.board.addLandPermited = True
		
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
		
			
