from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen


class Line():
    def __init__(self, startX, startY, styleLine, label, nombreProceso = None):
        self.starPoint_x = startX
        self.starPoint_y = startY
        self.current_x = startX
        self.heightMarcs = 30
        self.separation = 30
        self.label = label
        if nombreProceso is None:
            self.nombreProceso = label
        else:
            self.nombreProceso = nombreProceso

        if styleLine == "normal":
            self.pen = QPen(Qt.black, 1, Qt.SolidLine)
        elif styleLine == "wait":
            self.pen = QPen(Qt.black, 1, Qt.DashLine)
        elif styleLine == "locked":
            self.pen = QPen(Qt.red, 1, Qt.DashLine)

        self.Marcs = []

    def addSegLineSpace(self):
        self.current_x += self.separation

    def addMarc(self):
        Marc = (self.current_x, self.starPoint_y - int(self.heightMarcs / 2), self.current_x,
                self.starPoint_y + int(self.heightMarcs / 2))
        self.Marcs.append(Marc)

    def drawLine(self, painter):
        painter.setPen(self.pen)
        painter.drawLine(self.starPoint_x, self.starPoint_y, self.current_x, self.starPoint_y)

    def paintLine(self, painter):
        painter.setPen(self.pen)
        for Marc in self.Marcs:
            painter.drawLine(Marc[0], Marc[1], Marc[2], Marc[3])
        painter.drawText(50 - 15, self.starPoint_y + 5, self.label)
        self.drawLine(painter)


class RuleLine(Line):
    def __init__(self, startX, startY, styleLine, ruleSecs):
        super().__init__(startX, startY, styleLine, "")
        self.ruleSecs = ruleSecs

    def addMarc(self):
        Marc = (self.current_x, self.starPoint_y - int(self.heightMarcs / 2), self.current_x,
                self.starPoint_y + int(self.heightMarcs / 2))
        self.Marcs.append(Marc)
        self.addSegLineSpace()

    def createMarcs(self):
        for n in range(0, self.ruleSecs):
            self.addMarc()

    def paintLine(self, painter):
        painter.setPen(self.pen)
        counter = 0
        for Marc in self.Marcs:
            painter.drawText(Marc[0] - 3, Marc[1] - 10, str(counter))
            painter.drawLine(Marc[0], Marc[1], Marc[2], Marc[3])
            counter += 1
        self.drawLine(painter)

    def getWidth(self):
        return self.Marcs[-1][0]
