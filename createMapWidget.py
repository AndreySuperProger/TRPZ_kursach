from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QDialog
from PyQt5.QtGui import QIntValidator, QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt
from flowMap import *

#Панель пиктограмм
class AreasPanel(QWidget):
	def __init__(self, parentWidget):
		super(AreasPanel, self).__init__(parentWidget)
		#self.move(500, 500)
		self.setGeometry(20, 190, 130, 360)
		
		landPict = Area(Land, False, False, self)
		landPict.setGeometry(0, 0, 50, 50)
		landPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		noFlowPict = Area(NoFlow, False, False, self)
		noFlowPict.setGeometry(0, 60, 50, 50)
		noFlowPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		northPict = Area(North, False, False, self)
		northPict.setGeometry(0, 120, 50, 50)
		northPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		northernEastPict = Area(NorthernEast, False, False, self)
		northernEastPict.setGeometry(0, 180, 50, 50)
		northernEastPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		eastPict = Area(East, False, False, self)
		eastPict.setGeometry(0, 240, 50, 50)
		eastPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		southernEastPict = Area(SouthernEast, False, False, self)
		southernEastPict.setGeometry(60, 0, 50, 50)
		southernEastPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		southPict = Area(South, False, False, self)
		southPict.setGeometry(60, 60, 50, 50)
		southPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		southernWestPict = Area(SouthernWest, False, False, self)
		southernWestPict.setGeometry(60, 120, 50, 50)
		southernWestPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		westPict = Area(West, False, False, self)
		westPict.setGeometry(60, 180, 50, 50)
		westPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		northernWestPict = Area(NorthernWest, False, False, self)
		northernWestPict.setGeometry(60, 240, 50, 50)
		northernWestPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		poisonPict = Area(NoFlow, True, False, self)
		poisonPict.setGeometry(0, 300, 50, 50)
		poisonPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
		poisonPict = Area(NoFlow, False, True, self)
		poisonPict.setGeometry(60, 300, 50, 50)
		poisonPict.clicked.connect(parentWidget.areaPanelClickedSlot)
		
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
		
		lbl4 = QLabel("Інтервал:", self)
		lbl4.move(20, 140)
		self.intervalEdit = self.addEdit(170, 140)
		
		lbl5 = QLabel("Дистанція:", self)
		lbl5.move(20, 180)
		self.distanceEdit = self.addEdit(170, 180)
		
		lbl6 = QLabel("Радіус дії кораблів:", self)
		lbl6.move(20, 220)
		self.shipRadEdit = self.addEdit(170, 220)
		
		btn1 = QPushButton("ОК", self)
		btn1.move(20, 260)
		btn1.clicked.connect(self.parentWidget.createMapDialogOkBtnClickedSlot)
		
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

#TODO: Реализовать возможность рисования не отпуская ЛКМ
class CreateMapWidget(QWidget):
	def __init__(self, parentWidget, parentDialog = None):
		super(CreateMapWidget, self).__init__()
		#self.setGeometry(400, 400, 500, 600)
		self.setWindowTitle('Створити карту')
		self.areaPanelActivePict = None
		self.parentWidget = parentWidget
		
		okBtn = QPushButton("Ok", self)
		okBtn.move(150, 150)
		okBtn.clicked.connect(parentWidget.creatorWidgetOkBtnSlot)
		
		areasPanel = AreasPanel(self)
		
		self.flowMap = FlowMap((400, 20), (0, 0), [],
			[], [], self, 0, 0, 0)
		if parentDialog:
			self.createNewMap(parentDialog)
		else:
			self.flowMap.copy(parentWidget.mainFlowMap)
		self.flowMap.bindClickedSignal(self)
		self.show()
	
	#TODO:оставить часть прошлой карты
	def createNewMap(self, parentDialog):
		self.flowMap.hide()
		del(self.flowMap)
		rows = cols = distance = interval = areaSize = 0
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
			interval = int(parentDialog.intervalEdit.text())
			print("interval = " + str(interval))
		except:
			interval = 0
		try:
			distance = int(parentDialog.distanceEdit.text())
			print("distance = " + str(distance))
		except:
			distance = 0
		try:
			areaSize = int(parentDialog.areaSizeEdit.text())
			print("areaSize = " + str(areaSize))
		except:
			areaSize = 50
		self.flowMap = FlowMap((400, 20), (rows, cols),
			[[0 for j in range(cols)] for i in range(rows)],
			[[0 for j in range(cols)] for i in range(rows)],
			[[0 for j in range(cols)] for i in range(rows)],
			self, distance, interval, areaSize)
		self.flowMap.show()
		self.hide()
		self.show()
		
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
					area.update()
		
			
