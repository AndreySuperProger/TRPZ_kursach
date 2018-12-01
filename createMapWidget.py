from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator, QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt
from flowMap import *

class AreasPanel(QWidget):
	def __init__(self, parentWidget):
		super(AreasPanel, self).__init__(parentWidget)
		self.move(500, 500)
		self.setGeometry(20, 150, 130, 360)
		
		landPict = Area(Land, False, self)
		landPict.setGeometry(0, 0, 50, 50)
		landPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		noFlowPict = Area(NoFlow, False, self)
		noFlowPict.setGeometry(0, 60, 50, 50)
		noFlowPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		northPict = Area(North, False, self)
		northPict.setGeometry(0, 120, 50, 50)
		northPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		northernEastPict = Area(NorthernEast, False, self)
		northernEastPict.setGeometry(0, 180, 50, 50)
		northernEastPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		eastPict = Area(East, False, self)
		eastPict.setGeometry(0, 240, 50, 50)
		eastPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		southernEastPict = Area(SouthernEast, False, self)
		southernEastPict.setGeometry(60, 0, 50, 50)
		southernEastPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		southPict = Area(South, False, self)
		southPict.setGeometry(60, 60, 50, 50)
		southPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		southernWestPict = Area(SouthernWest, False, self)
		southernWestPict.setGeometry(60, 120, 50, 50)
		southernWestPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		westPict = Area(West, False, self)
		westPict.setGeometry(60, 180, 50, 50)
		westPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		northernWestPict = Area(NorthernWest, False, self)
		northernWestPict.setGeometry(60, 240, 50, 50)
		northernWestPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		poisonPict = Area(NoFlow, True, self)
		poisonPict.setGeometry(0, 300, 50, 50)
		poisonPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		self.show()
	
class CreateMapWidget(QWidget):
	def __init__(self, parentWidget):
		super(CreateMapWidget, self).__init__()
		#self.setGeometry(400, 400, 500, 600)
		self.setWindowTitle('Створити карту')
		self.areaPanelActivePict = None
		self.parentWidget = parentWidget
		
		lbl1 = QLabel("Довжина:", self)
		lbl1.move(20, 20)
		lbl2 = QLabel("Ширина:", self)
		lbl2.move(20, 60)
		
		rowsEdit = QLineEdit(self)
		rowsEdit.setValidator(QIntValidator())
		rowsEdit.setMaxLength(2)
		rowsEdit.setAlignment(Qt.AlignRight)
		rowsEdit.setFont(QFont("Arial",20))
		rowsEdit.move(120, 20)
		self.rowsEdit = rowsEdit
		
		colsEdit = QLineEdit(self)
		colsEdit.setValidator(QIntValidator())
		colsEdit.setMaxLength(2)
		colsEdit.setAlignment(Qt.AlignRight)
		colsEdit.setFont(QFont("Arial", 20))
		colsEdit.move(120, 60)
		self.colsEdit = colsEdit
		
		refreshMapBtn = QPushButton("Оновити карту", self)
		refreshMapBtn.move(20, 110)
		refreshMapBtn.clicked.connect(self.refreshMapSlot)
		
		okBtn = QPushButton("Ok", self)
		okBtn.move(150, 110)
		okBtn.clicked.connect(parentWidget.creatorWidgetOkBtnSlot)
		
		areasPanel = AreasPanel(self)
		
		self.flowMap = FlowMap((400, 20), (0, 0), [],
			[], self, 0, 0, 0)
		self.flowMap.copy(parentWidget.mainFlowMap)
		self.flowMap.bindClickedSignal(self)
		
		self.show()
	
	#TODO:оставить часть прошлой карты	
	def refreshMapSlot(self):
		self.flowMap.hide()
		del(self.flowMap)
		rows = cols = 0
		try:
			rows = int(self.rowsEdit.text())
			cols = int(self.colsEdit.text())
		except:
			rows = cols = 0
		self.flowMap = FlowMap((400, 20), (rows, cols),
			[[0 for j in range(cols)] for i in range(rows)],
			[[0 for j in range(cols)] for i in range(rows)], self, 10, 10, 50)
		self.flowMap.show()
		self.flowMap.bindClickedSignal(self)
		self.update()
		
	#слот для обработки кликов на панели пиктограм
	def areaPanelClickedSlot(self):
		pictogram = self.sender()
		print("clicked on pict panel " + str(pictogram))
		self.areaPanelActivePict = pictogram
		
	#слот для обработки кликов на самой карте
	def flowMapClickedSlot(self):
		area = self.sender()
		print("clicked on flowMap " + str(area))
		if self.areaPanelActivePict == None:
			pass
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
					area.update()
		
			
