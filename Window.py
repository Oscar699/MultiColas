from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QVBoxLayout, QTableWidget, QGroupBox, QAbstractItemView, \
    QLabel, QDesktopWidget, QTableWidgetItem

from Line import RuleLine, Line
from Window_Elements import GantContainer, AreaContainer, QueueTable

class Window(QWidget):
    def __init__(self, ColaProcesos):
        super().__init__()
        
        self.ColaProcesos = ColaProcesos
        self.rulerLine = RuleLine(startX=50, startY=50, styleLine="normal", ruleSecs=36)
        self.rulerLine.createMarcs()

        # Layout de la ventana
        self.layout = QVBoxLayout(self)

        # Contenedor para el scroll
        self.tablesContainer = AreaContainer()
        self.gantContainer = GantContainer(self.rulerLine)

        # Area de scroll
        self.TableScroll = QScrollArea()
        self.GantScroll = QScrollArea()
        self.TableScroll.setWidget(self.tablesContainer)
        self.GantScroll.setWidget(self.gantContainer)
        self.TableScroll.setWidgetResizable(True)
        self.GantScroll.setWidgetResizable(True)
        self.layout.addWidget(self.TableScroll)
        self.layout.addWidget(self.GantScroll)

        # Titulo de las tablas
        self.tablesContainer.Layout.addWidget(QLabel("Tabla Procesos"), 0, 0, Qt.AlignCenter)
        self.tablesContainer.Layout.addWidget(QLabel("Cola RR"), 0, 1, Qt.AlignCenter)
        self.tablesContainer.Layout.addWidget(QLabel("Cola SJF"), 0, 2, Qt.AlignCenter)
        self.tablesContainer.Layout.addWidget(QLabel("Cola FCFS"), 0, 3, Qt.AlignCenter)

        # Tabla de procesos
        self.ProcessTable = QTableWidget()
        self.ProcessTable.setFixedSize(580, 290)
        self.ProcessTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ProcessTable.setDragDropOverwriteMode(False)
        self.ProcessTable.setColumnCount(8)
        for i in range(0, 8):
            self.ProcessTable.setColumnWidth(i, 65)
        self.ProcessTable.setColumnWidth(7, 80)
        self.ProcessTable.setRowCount(0)
        headers = ("Proceso", "T. Llegada", "Rafaga", "T. Comienzo", "T. Final", "T. Retorno", "T. Espera", "Semaforo")
        self.ProcessTable.setHorizontalHeaderLabels(headers)
        self.tablesContainer.Layout.addWidget(self.ProcessTable, 1, 0)

        # Tablas para colas
        self.rr_Table = QueueTable(200, 290)
        self.tablesContainer.Layout.addWidget(self.rr_Table, 1, 1)
        self.sjf_Table = QueueTable(200, 290)
        self.tablesContainer.Layout.addWidget(self.sjf_Table, 1, 2)
        self.fcfs_Table = QueueTable(200, 290)
        self.tablesContainer.Layout.addWidget(self.fcfs_Table, 1, 3)


        # Propiedades de la ventana
        self.setGeometry(0, 0, 1280, 800)
        self.setWindowTitle('Proyecto Final SO')
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.show()

        self.actualizarColas()        # Se sincroniza informacion inicial de las colas

        # Se dibujan los procesos
        listosRR = self.ColaProcesos.rr.colaListo.colaComoLista()
        listosSJF = self.ColaProcesos.sjf.colaListo.colaComoLista()
        listosFCFS = self.ColaProcesos.fcfs.colaListo.colaComoLista()
        for proceso in listosRR:
            proceso.agregarLineaEspera = False
            proceso.estaPintado = True
            waitLine = Line(startX=50, startY=self.gantContainer.current_y, styleLine="wait", label=proceso.nombre)
            waitLine.addMarc()
            self.gantContainer.waitLines.append(waitLine)
            self.gantContainer.addVerticalSpace()

        for proceso in listosSJF:
            proceso.agregarLineaEspera = False
            proceso.estaPintado = True
            waitLine = Line(startX=50, startY=self.gantContainer.current_y, styleLine="wait", label=proceso.nombre)
            waitLine.addMarc()
            self.gantContainer.waitLines.append(waitLine)
            self.gantContainer.addVerticalSpace()
        
        for proceso in listosFCFS:
            proceso.agregarLineaEspera = False
            proceso.estaPintado = True
            waitLine = Line(startX=50, startY=self.gantContainer.current_y, styleLine="wait", label=proceso.nombre)
            waitLine.addMarc()
            self.gantContainer.waitLines.append(waitLine)
            self.gantContainer.addVerticalSpace()
        
    def addItemTable(self, data):
        data = self.replaceNoneContent(data)
        fila = self.ProcessTable.rowCount()
        self.ProcessTable.insertRow(fila)
        for column in range(8):
            tableItem = QTableWidgetItem(str(data[column]))
            self.ProcessTable.setItem(fila, column, tableItem)

    def changeRowTable(self, rowNumber, newData):
        newData = self.replaceNoneContent(newData)
        for column in range(8):
            tableItem = QTableWidgetItem(newData[column])
            self.ProcessTable.setItem(rowNumber, column, tableItem)

    def replaceNoneContent(self, data):
        for i in range(7):
            var = data[i]
            if var is not None:
                data[i] = str(var)
            else:
                data[i] = "-"
        return data

    # Funcion que sincroniza las tablas de las colas con la informacion en el backend de cada una de las colas
    def actualizarColas(self):
        self.rr_Table.setRowCount(0)
        self.sjf_Table.setRowCount(0)
        self.fcfs_Table.setRowCount(0)

        enEjecucionRR = self.ColaProcesos.rr.procesoEnEjecucion
        enEjecucionSJF = self.ColaProcesos.sjf.procesoEnEjecucion
        enEjecucionFCFS = self.ColaProcesos.fcfs.procesoEnEjecucion

        listosRR = self.ColaProcesos.rr.colaListo.colaComoLista()
        listosSJF = self.ColaProcesos.sjf.colaListo.colaComoLista()
        listosFCFS = self.ColaProcesos.fcfs.colaListo.colaComoLista()

        bloqueadosRR = self.ColaProcesos.rr.colaBloqueados.colaComoLista()
        bloqueadosSJF = self.ColaProcesos.sjf.colaBloqueados.colaComoLista()
        bloqueadosFCFS = self.ColaProcesos.fcfs.colaBloqueados.colaComoLista()

        listaFinalRR = []
        listaFinalSJF = []
        listaFinalFCFS = []
        if enEjecucionRR is not None:
            listaFinalRR.append([enEjecucionRR.nombre, enEjecucionRR.llegada, enEjecucionRR.rafaga])
        if enEjecucionSJF is not None:
            listaFinalSJF.append([enEjecucionSJF.nombre, enEjecucionSJF.llegada, enEjecucionSJF.rafaga])
        if enEjecucionFCFS is not None:
            listaFinalFCFS.append([enEjecucionFCFS.nombre, enEjecucionFCFS.llegada, enEjecucionFCFS.rafaga])

        for itemRR in listosRR:
            listaFinalRR.append([itemRR.nombre, itemRR.llegada, itemRR.rafaga])
        
        for itemSJF in listosSJF:
            listaFinalSJF.append([itemSJF.nombre, itemSJF.llegada, itemSJF.rafaga])
        
        for itemFCFS in listosFCFS:
            listaFinalFCFS.append([itemFCFS.nombre, itemFCFS.llegada, itemFCFS.rafaga])
        
        for itemRR in bloqueadosRR:
            listaFinalRR.append([itemRR.nombre, itemRR.llegada, itemRR.rafaga])
        
        for itemSJF in bloqueadosSJF:
            listaFinalSJF.append([itemSJF.nombre, itemSJF.llegada, itemSJF.rafaga])
        
        for itemFCFS in bloqueadosFCFS:
            listaFinalFCFS.append([itemFCFS.nombre, itemFCFS.llegada, itemFCFS.rafaga])
        
        for itemRR in listaFinalRR:
            fila = self.rr_Table.rowCount()
            self.rr_Table.insertRow(fila)
            for column in range(3):
                tableItem = QTableWidgetItem(str(itemRR[column]))
                self.rr_Table.setItem(fila, column, tableItem)

        for itemSJF in listaFinalSJF:
            fila = self.sjf_Table.rowCount()
            self.sjf_Table.insertRow(fila)
            for column in range(3):
                tableItem = QTableWidgetItem(str(itemSJF[column]))
                self.sjf_Table.setItem(fila, column, tableItem)
        
        for itemFCFS in listaFinalFCFS:
            fila = self.fcfs_Table.rowCount()
            self.fcfs_Table.insertRow(fila)
            for column in range(3):
                tableItem = QTableWidgetItem(str(itemFCFS[column]))
                self.fcfs_Table.setItem(fila, column, tableItem)

    def pintarTerminados(self):
        for proceso in self.ColaProcesos.rr.colaTerminados:
            if proceso["cambiaSemaforo"]:
                proceso["cambiaSemaforo"] = False
                data = list(proceso.values())
                rowNumber = self.ProcessTable.findItems(data[0], Qt.MatchContains)[0].row()
                self.changeRowTable(rowNumber=rowNumber, newData=data)

        for proceso in self.ColaProcesos.sjf.colaTerminados:
            if proceso["cambiaSemaforo"]:
                proceso["cambiaSemaforo"] = False
                data = list(proceso.values())
                rowNumber = self.ProcessTable.findItems(data[0], Qt.MatchContains)[0].row()
                self.changeRowTable(rowNumber=rowNumber, newData=data)
        
        for proceso in self.ColaProcesos.fcfs.colaTerminados:
            if proceso["cambiaSemaforo"]:
                proceso["cambiaSemaforo"] = False
                data = list(proceso.values())
                rowNumber = self.ProcessTable.findItems(data[0], Qt.MatchContains)[0].row()
                self.changeRowTable(rowNumber=rowNumber, newData=data)

    def tick(self):
        tick = self.ColaProcesos.tick()
        self.pintarTerminados()

        if self.ColaProcesos.procesoEnEjecucion is not None:

            proceso = self.ColaProcesos.procesoEnEjecucion.__dict__
            data = list(proceso.values())
            if not self.ColaProcesos.procesoEnEjecucion.agregadoTablaPPal:
                self.ColaProcesos.procesoEnEjecucion.agregadoTablaPPal = True
                self.addItemTable(data)


            
            
            rowNumber = self.ProcessTable.findItems(data[0], Qt.MatchContains)[0].row()
            tableItem = QTableWidgetItem(data[7])
            self.ProcessTable.setItem(rowNumber, 7, tableItem)

            banderaWait = True
            banderaExecute = True
            banderaFinished = True

            for (i, finishedLine) in enumerate(self.gantContainer.finishedLines):
                if finishedLine.nombreProceso == self.ColaProcesos.procesoEnEjecucion.nombre:
                    banderaFinished = False

            for (i, waitLine) in enumerate(self.gantContainer.waitLines):
                if waitLine.nombreProceso == self.ColaProcesos.procesoEnEjecucion.nombre :
                    banderaWait = False
                    executeLine = Line(startX=waitLine.current_x, startY=waitLine.starPoint_y, styleLine="normal", label="", nombreProceso=self.ColaProcesos.procesoEnEjecucion.nombre)
                    executeLine.addMarc()
                    self.gantContainer.executeLines.append(executeLine)
                    self.gantContainer.finishedLines.append(self.gantContainer.waitLines.pop(i))
                    

            for (i, executeLine) in enumerate(self.gantContainer.executeLines):
                if executeLine.nombreProceso != self.ColaProcesos.procesoEnEjecucion.nombre:
                    executeLine.addMarc()
                    proceso = self.buscarProceso(executeLine.nombreProceso)
                    data = list(proceso.values())
                    rowNumber = self.ProcessTable.findItems(data[0], Qt.MatchContains)[0].row()
                    self.changeRowTable(rowNumber=rowNumber, newData=data)
                    self.gantContainer.finishedLines.append(self.gantContainer.executeLines.pop(i))

            for (i, executeLine) in enumerate(self.gantContainer.executeLines):
                if executeLine.nombreProceso == self.ColaProcesos.procesoEnEjecucion.nombre:
                    banderaExecute = False

            if banderaExecute and banderaWait and banderaFinished:
                proceso = self.ColaProcesos.procesoEnEjecucion
                startX = (50+self.rulerLine.separation*(tick["tiempo"]-1))
                executeLine = Line(startX=startX, startY=self.gantContainer.current_y, styleLine="normal", label=proceso.nombre)
                executeLine.addMarc()
                data = list(proceso.__dict__.values())
                self.gantContainer.executeLines.append(executeLine)
                self.gantContainer.addVerticalSpace()
        else:
            for (i, executeLine) in enumerate(self.gantContainer.executeLines):
                executeLine.addMarc()
                proceso = self.buscarProceso(executeLine.nombreProceso)
                data = list(proceso.values())
                rowNumber = self.ProcessTable.findItems(data[0], Qt.MatchContains)[0].row()
                self.changeRowTable(rowNumber=rowNumber, newData=data)
                self.gantContainer.finishedLines.append(self.gantContainer.executeLines.pop(i))

        #MostrarLinea Bloqueados
        for proceso in self.ColaProcesos.rr.colaBloqueados.colaComoLista():
            self.pintarProcesoBloqueado(tick, proceso)

        for proceso in self.ColaProcesos.sjf.colaBloqueados.colaComoLista():
            self.pintarProcesoBloqueado(tick, proceso)

        for proceso in self.ColaProcesos.fcfs.colaBloqueados.colaComoLista():
            self.pintarProcesoBloqueado(tick, proceso)

        #Terminar Linea de bloqueados 
        for (i,lockedLine) in enumerate(self.gantContainer.lockedLines):
            banderaLock = True
            for proceso in self.ColaProcesos.rr.colaBloqueados.colaComoLista():
                if lockedLine.nombreProceso == proceso.nombre:
                    banderaLock = False
                    break
            
            for proceso in self.ColaProcesos.sjf.colaBloqueados.colaComoLista():
                if lockedLine.nombreProceso == proceso.nombre:
                    banderaLock = False
                    break

            for proceso in self.ColaProcesos.fcfs.colaBloqueados.colaComoLista():
                if lockedLine.nombreProceso == proceso.nombre:
                    banderaLock = False
                    break

            #No existe el proceso en la cola de bloqueados pero si se esta pintando
            if banderaLock:
                lockedLine.addMarc()
                self.gantContainer.finishedLines.append(self.gantContainer.lockedLines.pop(i))

        

        listosRR = self.ColaProcesos.rr.colaListo.colaComoLista()
        listosSJF = self.ColaProcesos.sjf.colaListo.colaComoLista()
        listosFCFS = self.ColaProcesos.fcfs.colaListo.colaComoLista()
        # Inicializacion de los procesos existentes en "cola de espera"
        for proceso in listosRR:
            if not proceso.estaPintado:
                proceso.estaPintado = True
                waitLine = Line(startX=(50+self.rulerLine.separation*(tick["tiempo"]-1)), startY=self.gantContainer.current_y, styleLine="wait", label=proceso.nombre)
                waitLine.addMarc()
                self.gantContainer.waitLines.append(waitLine)
                self.gantContainer.addVerticalSpace()

        for proceso in listosSJF:
            if not proceso.estaPintado:
                proceso.estaPintado = True
                waitLine = Line(startX=(50+self.rulerLine.separation*(tick["tiempo"]-1)), startY=self.gantContainer.current_y, styleLine="wait", label=proceso.nombre)
                waitLine.addMarc()
                self.gantContainer.waitLines.append(waitLine)
                self.gantContainer.addVerticalSpace()
            
        for proceso in listosFCFS:
            if not proceso.estaPintado:
                proceso.estaPintado = True
                waitLine = Line(startX=(50+self.rulerLine.separation*(tick["tiempo"]-1)), startY=self.gantContainer.current_y, styleLine="wait", label=proceso.nombre)
                waitLine.addMarc()
                self.gantContainer.waitLines.append(waitLine)
                self.gantContainer.addVerticalSpace()
                
    def pintarProcesoBloqueado(self, tick, proceso):
        banderaLock = True
        for lockedLine in self.gantContainer.lockedLines:
            if lockedLine.nombreProceso == proceso.nombre:
                banderaLock = False
                break
        if banderaLock:
            posY = 0
            for (i, finishedLine) in enumerate(self.gantContainer.finishedLines):
                if finishedLine.nombreProceso == proceso.nombre:
                    posY = finishedLine.starPoint_y

            lockedLine = Line(startX=(50+self.rulerLine.separation*(tick["tiempo"]-1)), startY=posY, styleLine="locked", label="", nombreProceso=proceso.nombre)
            self.gantContainer.lockedLines.append(lockedLine)


    def buscarProceso(self, nomProceso):
        procesoRR = self.buscarEnColaEspecifica(self.ColaProcesos.rr,nomProceso)
        procesoSJF = self.buscarEnColaEspecifica(self.ColaProcesos.sjf,nomProceso)
        procesoFCFS = self.buscarEnColaEspecifica(self.ColaProcesos.fcfs,nomProceso)
        if procesoRR is not None:
            return procesoRR
        
        if procesoSJF is not None:
            return procesoSJF

        if procesoFCFS is not None:
            return procesoFCFS
        
        return None

    def buscarEnColaEspecifica(self,colaAct, nomProceso):
        for proceso in colaAct.colaTerminados:
            if proceso["nombre"] == nomProceso:
                return proceso

        for proceso in colaAct.colaBloqueados.colaComoLista():
            if proceso.nombre == nomProceso:
                return proceso.__dict__

        for proceso in colaAct.colaListo.colaComoLista():
            if proceso.nombre == nomProceso:
                return proceso.__dict__
        
        return None

    

    def paint(self):
        self.tick()
        self.gantContainer.simulateSegProgression()
        self.gantContainer.update()
        self.actualizarColas()    
