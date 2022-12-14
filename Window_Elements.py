from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QVBoxLayout, QTableWidget, QGroupBox, QAbstractItemView, \
    QGridLayout

from Line import RuleLine


class AreaContainer(QWidget):
    def __init__(self):
        super().__init__()

        # Layout del container
        self.Layout = QGridLayout(self)
        self.Layout.setContentsMargins(25, 25, 25, 25)


class GantContainer(QWidget):
    def __init__(self, rulerLine):
        super().__init__()
        # Varriables de control
        self.lineSeparation = 50
        self.y_availableSpace = 150
        self.counter = -1
        self.waitLines = []
        self.executeLines = []
        self.finishedLines = []
        self.lockedLines = []
        self.updatePermission = False
        self.current_y = 100
        #Layout del contenedor
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, self.current_y, 1130, self.lineSeparation)
        self.rulerLine = rulerLine

    def addHorizontalSpace(self, rulerLine):
        self.horizontalLayout.setContentsMargins(self.horizontalLayout.contentsMargins().left(),
                                                    self.horizontalLayout.contentsMargins().top(),
                                                    self.horizontalLayout.contentsMargins().right() + 30,
                                                    self.horizontalLayout.contentsMargins().bottom())
        rulerLine.addMarc()

    def addVerticalSpace(self):
        self.current_y += self.lineSeparation
        self.horizontalLayout.setContentsMargins(self.horizontalLayout.contentsMargins().left(),
                                                    self.current_y,
                                                    self.horizontalLayout.contentsMargins().right(),
                                                    self.horizontalLayout.contentsMargins().bottom())

    def simulateSegProgression(self):
        for line in self.waitLines:
            line.addSegLineSpace()
        for line in self.executeLines:
            line.addSegLineSpace()        
        for line in self.lockedLines:
            line.addSegLineSpace()

        # Pura simulacion porque en realidad se dependeria de las lineas en ejecucion y con una logica diferente
        if len(self.executeLines) and self.executeLines[0].current_x >= self.rulerLine.getWidth():
            self.horizontalLayout.setContentsMargins(self.horizontalLayout.contentsMargins().left(),
                                                     self.horizontalLayout.contentsMargins().top(),
                                                     self.horizontalLayout.contentsMargins().right() + 30,
                                                     self.lineSeparation)
            self.rulerLine.addMarc()
        elif len(self.waitLines) and self.waitLines[0].current_x >= self.rulerLine.getWidth():
            self.horizontalLayout.setContentsMargins(self.horizontalLayout.contentsMargins().left(),
                                                     self.horizontalLayout.contentsMargins().top(),
                                                     self.horizontalLayout.contentsMargins().right() + 30,
                                                     self.lineSeparation)
            self.rulerLine.addMarc()
        elif len(self.lockedLines) and self.lockedLines[0].current_x >= self.rulerLine.getWidth():
            self.horizontalLayout.setContentsMargins(self.horizontalLayout.contentsMargins().left(),
                                                     self.horizontalLayout.contentsMargins().top(),
                                                     self.horizontalLayout.contentsMargins().right() + 30,
                                                     self.lineSeparation)
            self.rulerLine.addMarc()

    def paintElements(self, painter):
        for line in self.waitLines:
            line.paintLine(painter)
        for line in self.executeLines:
            line.paintLine(painter)
        for line in self.finishedLines:
            line.paintLine(painter)
        for line in self.lockedLines:
            line.paintLine(painter)

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.updatePermission:
            pass
        
        # Siempre se pinta la regla de los segundos
        self.rulerLine.paintLine(painter=painter)
        self.paintElements(painter=painter)


class QueueTable(QTableWidget):
    def __init__(self, width, height):
        super().__init__()
        self.setFixedSize(width, height)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setDragDropOverwriteMode(False)
        self.setColumnCount(3)
        for i in range(0, 3):
            self.setColumnWidth(i, 60)
        self.setRowCount(0)

        headers = ("Proceso", "T. Llegada", "Rafaga")
        self.setHorizontalHeaderLabels(headers)




