import ctypes

class Procesador:
    def __init__(self):
        self.nombre = "Procesador"
        self.siguiente = id(self)

class Proceso:
    def __init__(self, nombre, llegada, rafaga, rafagaTotalEjecutada=0, siguiente=None):
        self.nombre = nombre
        self.llegada = llegada
        self.rafaga = rafaga
        self.comienzo = None
        self.final = None
        self.retorno = None
        self.espera = None
        self.estadoSemaforo = "Listo"

        self.rafagaEjecutada = 0
        self.rafagaTotalEjecutada = rafagaTotalEjecutada
        
        self.siguiente = siguiente
        self.estaPintado = False
        self.estaBloqueado = False
        self.cambiaSemaforo = False
        self.agregadoTablaPPal = False


    def comenzar(self, tiempo):
        self.comienzo = tiempo


    def pausa(self):
        self.final = self.rafagaEjecutada + self.comienzo
        self.retorno = self.final - self.llegada
        self.espera = self.retorno - self.rafagaTotalEjecutada

    def terminar(self):
        self.final = self.rafaga + self.comienzo
        self.retorno = self.final - self.llegada
        self.espera = self.retorno - self.rafaga


class Cola:
    def __init__(self):  
        self.cab = Procesador()
        self.arrMemoria = []
        self.numClientes = 0

    def agregarProceso(self, proceso):
        proceso.siguiente = id(self.cab)
        self.arrMemoria.insert(len(self.arrMemoria),proceso)
        aux = ctypes.cast(self.cab.siguiente, ctypes.py_object).value
        aux2 = self.cab
        while(isinstance(aux, Proceso)):
            aux2 = aux
            aux = ctypes.cast(aux.siguiente, ctypes.py_object).value
        aux2.siguiente = id(self.arrMemoria[-1])
        self.numClientes += 1

    def agregar(self, nombre, llegada, rafaga, rafagaTotal = 0):
        self.arrMemoria.insert(len(self.arrMemoria),Proceso(nombre, llegada, rafaga, rafagaTotal, id(self.cab)))
        aux = ctypes.cast(self.cab.siguiente, ctypes.py_object).value
        aux2 = self.cab
        while(isinstance(aux, Proceso)):
            aux2 = aux
            aux = ctypes.cast(aux.siguiente, ctypes.py_object).value
        aux2.siguiente = id(self.arrMemoria[-1])
        self.numClientes += 1

    def recorrerCola(self):
        aux = ctypes.cast(self.cab.siguiente, ctypes.py_object).value
        print(aux.__dict__)
        while(isinstance(aux, Proceso)):
            aux = ctypes.cast(aux.siguiente, ctypes.py_object).value
            print(aux.__dict__)

    def colaComoLista(self):
        aux = ctypes.cast(self.cab.siguiente, ctypes.py_object).value
        resultado = []
        if (isinstance(aux, Procesador)):
            return resultado
        else:
            resultado.append(aux)
        
        while(isinstance(aux, Proceso)):
            aux = ctypes.cast(aux.siguiente, ctypes.py_object).value
            if (isinstance(aux, Proceso)):
                resultado.append(aux)
            
        return resultado

    def obtener(self, atender=False):
        atiendo = ctypes.cast(self.cab.siguiente, ctypes.py_object).value
        if (isinstance(atiendo, Procesador)):
            return "No hay mas procesos"
        if atender:
            self.cab.siguiente = atiendo.siguiente
            atiendo.siguiente = id(self.cab)
        return atiendo

    def deleteAt(self, nombreProceso):
        aux = ctypes.cast(self.cab.siguiente, ctypes.py_object).value
        aux2 = self.cab
        if (isinstance(aux, Procesador)):
            return False
        
        if(aux.nombre == nombreProceso):
            aux2.siguiente = aux.siguiente

            return True
        
        while(isinstance(aux, Proceso)):
            aux2 = aux
            aux = ctypes.cast(aux.siguiente, ctypes.py_object).value
            if (isinstance(aux, Proceso) and aux.nombre == nombreProceso):
                aux2.siguiente = aux.siguiente
                return True
            
        return False


class ColaProcesos:
    
    def __init__(self, tipoCola):
        self.colaListo = Cola()
        self.procesoEnEjecucion = None
        self.colaTerminados = []
        self.colaBloqueados = Cola()
        self.tiempo = 0
        self.cuantum = 3
        self.tipoCola = tipoCola

    def buscarSJ(self):
        procesos = self.colaListo.colaComoLista()
        if len(procesos) > 0:
            procesoSel = procesos[0]
        else:
            return "No hay mas procesos"
        
        for proceso in procesos:
            if (proceso.rafaga - proceso.rafagaEjecutada) < (procesoSel.rafaga - procesoSel.rafagaEjecutada):
                procesoSel = proceso

        return procesoSel

    def avanzaTiempoSinEj(self):
        self.tiempo += 1
        return {"tiempo": self.tiempo}

    def tick(self):
        if self.tipoCola == "RR":
            if self.procesoEnEjecucion is None:
                procesoActual = self.colaListo.obtener()
            else:
                procesoActual = self.procesoEnEjecucion

            if procesoActual != "No hay mas procesos":

                if procesoActual.llegada <= self.tiempo and procesoActual.comienzo is None:
                    procesoActual.comenzar(self.tiempo)
                    self.colaListo.obtener(True)
                    procesoActual.rafagaEjecutada += 1
                    procesoActual.estadoSemaforo = "En ejecucion"
                    self.procesoEnEjecucion = procesoActual
                elif procesoActual.rafagaEjecutada == self.cuantum and procesoActual.rafaga > procesoActual.rafagaEjecutada:
                    #no ha ejecutado toda la rafaga 
                    procesoActual.rafagaTotalEjecutada = procesoActual.rafagaTotalEjecutada + procesoActual.rafagaEjecutada
                    procesoActual.pausa()
                    procesoActual.estadoSemaforo = "Expulsado"
                    procesoActual.cambiaSemaforo = True
                    self.colaTerminados.append(procesoActual.__dict__)
                    self.procesoEnEjecucion = None
                    num = int(procesoActual.nombre[1:]) + 1
                    nombreNuevo = procesoActual.nombre[0:1] + str(num)
                    llegadaNueva = procesoActual.llegada
                    rafagaNueva = procesoActual.rafaga - procesoActual.rafagaEjecutada
                    rafagaTotalEjecutadaNueva = procesoActual.rafagaTotalEjecutada
                    procesoNuevo = Proceso(nombreNuevo, llegadaNueva, rafagaNueva, rafagaTotalEjecutadaNueva)
                    procesoNuevo.estadoSemaforo = "Listo"
                    self.colaListo.agregarProceso(procesoNuevo)



                    proceso2Actual = self.colaListo.obtener()
                    if proceso2Actual != "No hay mas procesos":
                        if proceso2Actual.llegada <= self.tiempo and proceso2Actual.comienzo is None:
                            proceso2Actual.comenzar(self.tiempo)
                            self.colaListo.obtener(True)
                            proceso2Actual.rafagaEjecutada += 1
                            proceso2Actual.estadoSemaforo = "En ejecucion"
                            self.procesoEnEjecucion = proceso2Actual

                elif procesoActual.rafaga == procesoActual.rafagaEjecutada:
                    procesoActual.rafagaTotalEjecutada = procesoActual.rafagaTotalEjecutada + procesoActual.rafagaEjecutada
                    procesoActual.pausa()
                    procesoActual.estadoSemaforo = "Finalizado"
                    self.colaTerminados.append(procesoActual.__dict__)
                    self.procesoEnEjecucion = None                
                    proceso2Actual = self.colaListo.obtener()
                    if proceso2Actual != "No hay mas procesos":
                        if proceso2Actual.llegada <= self.tiempo and proceso2Actual.comienzo is None:
                            proceso2Actual.comenzar(self.tiempo)
                            self.colaListo.obtener(True)
                            proceso2Actual.estadoSemaforo = "En ejecucion"
                            proceso2Actual.rafagaEjecutada += 1
                            self.procesoEnEjecucion = proceso2Actual
                else:
                    procesoActual.rafagaEjecutada+=1

        elif self.tipoCola == "FCFS":
            if self.procesoEnEjecucion is None:
                
                procesoActual = self.colaListo.obtener()
            else:
                procesoActual = self.procesoEnEjecucion

            if procesoActual != "No hay mas procesos":

                if procesoActual.llegada <= self.tiempo and procesoActual.comienzo is None:
                    procesoActual.comenzar(self.tiempo)
                    self.colaListo.obtener(True)
                    procesoActual.rafagaEjecutada += 1
                    procesoActual.estadoSemaforo = "En ejecucion"
                    self.procesoEnEjecucion = procesoActual

                elif procesoActual.rafaga == procesoActual.rafagaEjecutada:
                    procesoActual.rafagaTotalEjecutada = procesoActual.rafagaTotalEjecutada + procesoActual.rafagaEjecutada
                    procesoActual.terminar()
                    procesoActual.estadoSemaforo = "Finalizado"
                    self.colaTerminados.append(procesoActual.__dict__)
                    self.procesoEnEjecucion = None                
                    proceso2Actual = self.colaListo.obtener()
                    if proceso2Actual != "No hay mas procesos":
                        if proceso2Actual.llegada <= self.tiempo and proceso2Actual.comienzo is None:
                            proceso2Actual.comenzar(self.tiempo)
                            self.colaListo.obtener(True)
                            proceso2Actual.estadoSemaforo = "En ejecucion"
                            proceso2Actual.rafagaEjecutada += 1
                            self.procesoEnEjecucion = proceso2Actual
                else:
                    procesoActual.rafagaEjecutada+=1

        elif self.tipoCola == "SJF":
            if self.procesoEnEjecucion is None:
                procesoActual = self.buscarSJ()
            else:
                procesoActual = self.procesoEnEjecucion

            if procesoActual != "No hay mas procesos":

                if procesoActual.llegada <= self.tiempo and procesoActual.comienzo is None:
                    procesoActual.comenzar(self.tiempo)
                    self.colaListo.deleteAt(procesoActual.nombre)
                    procesoActual.rafagaEjecutada += 1
                    procesoActual.estadoSemaforo = "En ejecucion"
                    self.procesoEnEjecucion = procesoActual

                elif procesoActual.rafaga == procesoActual.rafagaEjecutada:
                    procesoActual.rafagaTotalEjecutada = procesoActual.rafagaTotalEjecutada + procesoActual.rafagaEjecutada
                    procesoActual.terminar()
                    procesoActual.estadoSemaforo = "Finalizado"
                    self.colaTerminados.append(procesoActual.__dict__)
                    self.procesoEnEjecucion = None                
                    proceso2Actual = self.buscarSJ()
                    if proceso2Actual != "No hay mas procesos":
                        if proceso2Actual.llegada <= self.tiempo and proceso2Actual.comienzo is None:
                            proceso2Actual.comenzar(self.tiempo)
                            self.colaListo.deleteAt(proceso2Actual.nombre)
                            proceso2Actual.estadoSemaforo = "En ejecucion"
                            proceso2Actual.rafagaEjecutada += 1
                            self.procesoEnEjecucion = proceso2Actual
                else:
                    procesoActual.rafagaEjecutada+=1

        self.tiempo += 1
        return {"tiempo": self.tiempo}

    def bloquear(self):
        if self.procesoEnEjecucion is not None:
            procesoActual = self.procesoEnEjecucion
            if procesoActual.rafaga > procesoActual.rafagaEjecutada and self.cuantum > procesoActual.rafagaEjecutada:
                print("bloqueo a ",procesoActual.nombre, " en ",self.tiempo, " con rafaga ejecutada de ", procesoActual.rafagaEjecutada)

                procesoActual.estaBloqueado = True
                procesoActual.rafagaTotalEjecutada = procesoActual.rafagaTotalEjecutada + procesoActual.rafagaEjecutada
                procesoActual.estadoSemaforo = "Bloqueado"
                procesoActual.pausa()
                self.colaBloqueados.agregarProceso(procesoActual)
                self.colaTerminados.append(procesoActual.__dict__)
                self.procesoEnEjecucion = None

                if self.tipoCola == "SJF":
                    proceso2Actual = self.buscarSJ()
                else:
                    proceso2Actual = self.colaListo.obtener()
                
                if proceso2Actual != "No hay mas procesos":
                    if proceso2Actual.llegada <= self.tiempo and proceso2Actual.comienzo is None:
                        proceso2Actual.comenzar(self.tiempo)
                        proceso2Actual.estadoSemaforo = "En ejecucion"
                        if self.tipoCola == "SJF":
                            self.colaListo.deleteAt(proceso2Actual.nombre)
                        else:
                            self.colaListo.obtener(True)                        
                        self.procesoEnEjecucion = proceso2Actual
    
    def desbloquear(self):
        if self.colaBloqueados.obtener() != "No hay mas procesos":
            procesoActual = self.colaBloqueados.obtener(True)
            num = int(procesoActual.nombre[1:]) + 1
            nombreNuevo = procesoActual.nombre[0:1] + str(num)
            llegadaNueva = procesoActual.llegada
            rafagaNueva = procesoActual.rafaga - procesoActual.rafagaEjecutada
            rafagaTotalEjecutadaNueva = procesoActual.rafagaTotalEjecutada
            procesoNuevo = Proceso(nombreNuevo, llegadaNueva, rafagaNueva, rafagaTotalEjecutadaNueva)
            procesoNuevo.estadoSemaforo = "Listo"
            self.colaListo.agregarProceso(procesoNuevo)
            print("desbloqueado", procesoActual.nombre, "en", self.tiempo)



    def agregar(self,nombre,rafaga):
        self.colaListo.agregar(nombre, self.tiempo, rafaga)

    def agregarDeOtraCola(self, proceso):
        proceso.llegada = self.tiempo
        self.colaListo.agregarProceso(proceso)


class ColasProcesos:
    def __init__(self):
        self.tiempo = 0
        self.rr = ColaProcesos("RR")
        self.sjf = ColaProcesos("SJF")
        self.fcfs = ColaProcesos("FCFS")
        self.procesoEnEjecucion = None
        self.colaActiva = ""
        self.tiempoIntentoSJF = 0
        self.tiempoIntentoFCFS = 0
    
    def bloquear(self):
        if self.colaActiva == "RR":
            self.rr.bloquear()
        elif self.colaActiva == "SJF":
            self.sjf.bloquear()
        elif self.colaActiva == "FCFS":
            self.fcfs.bloquear()


    def desbloquear(self):
        self.rr.desbloquear()
        self.sjf.desbloquear()
        self.fcfs.desbloquear()
        
    def agregarRR(self,nombre,rafaga):
        self.rr.agregar(nombre, rafaga)
    
    def agregarFCFS(self,nombre,rafaga):
        self.fcfs.agregar(nombre, rafaga)
    
    def agregarSJF(self,nombre,rafaga):
        self.sjf.agregar(nombre, rafaga)


    def tick(self):
        if self.rr.procesoEnEjecucion is not None:
            self.colaActiva = "RR"
            self.procesoEnEjecucion = self.rr.procesoEnEjecucion
        elif self.sjf.procesoEnEjecucion is not None:
            self.colaActiva = "SFJ"
            self.procesoEnEjecucion = self.sjf.procesoEnEjecucion
        elif self.fcfs.procesoEnEjecucion is not None:
            self.colaActiva = "FCFS"
            self.procesoEnEjecucion = self.fcfs.procesoEnEjecucion
        else:    
            self.colaActiva = ""
            self.procesoEnEjecucion = None

        procesoEnRR = self.rr.colaListo.obtener()
        procesoEnSFJ = self.sjf.buscarSJ()
        procesoEnFCFS = self.fcfs.colaListo.obtener()   
        
        if self.procesoEnEjecucion is not None and self.colaActiva == "SFJ" and procesoEnRR != "No hay mas procesos":
            #pauso actual en SFJ
            procesoActual = self.procesoEnEjecucion
            procesoActual.rafagaTotalEjecutada = procesoActual.rafagaTotalEjecutada + procesoActual.rafagaEjecutada
            procesoActual.pausa()
            procesoActual.estadoSemaforo = "Expulsado"
            procesoActual.cambiaSemaforo = True
            self.sjf.colaTerminados.append(procesoActual.__dict__)
            num = int(procesoActual.nombre[1:]) + 1
            nombreNuevo = procesoActual.nombre[0:1] + str(num)
            llegadaNueva = procesoActual.llegada
            rafagaNueva = procesoActual.rafaga - procesoActual.rafagaEjecutada
            rafagaTotalEjecutadaNueva = procesoActual.rafagaTotalEjecutada
            procesoNuevo = Proceso(nombreNuevo, llegadaNueva, rafagaNueva, rafagaTotalEjecutadaNueva)
            procesoNuevo.estadoSemaforo = "Listo"
            self.sjf.colaListo.agregarProceso(procesoNuevo)
            self.procesoEnEjecucion = None
            self.sjf.procesoEnEjecucion = None

        elif self.procesoEnEjecucion is not None and self.colaActiva == "FCFS" and procesoEnRR != "No hay mas procesos":
            #pauso actual en FCFS
            procesoActual = self.procesoEnEjecucion
            procesoActual.rafagaTotalEjecutada = procesoActual.rafagaTotalEjecutada + procesoActual.rafagaEjecutada
            procesoActual.pausa()
            procesoActual.estadoSemaforo = "Expulsado"
            procesoActual.cambiaSemaforo = True
            self.fcfs.colaTerminados.append(procesoActual.__dict__)
            num = int(procesoActual.nombre[1:]) + 1
            nombreNuevo = procesoActual.nombre[0:1] + str(num)
            llegadaNueva = procesoActual.llegada
            rafagaNueva = procesoActual.rafaga - procesoActual.rafagaEjecutada
            rafagaTotalEjecutadaNueva = procesoActual.rafagaTotalEjecutada
            procesoNuevo = Proceso(nombreNuevo, llegadaNueva, rafagaNueva, rafagaTotalEjecutadaNueva)
            procesoNuevo.estadoSemaforo = "Listo"
            self.fcfs.colaListo.agregarProceso(procesoNuevo)
            self.procesoEnEjecucion = None
            self.fcfs.procesoEnEjecucion = None

        elif self.procesoEnEjecucion is not None and self.colaActiva == "FCFS" and procesoEnSFJ != "No hay mas procesos":
            #pauso actual en FCFS
            procesoActual = self.procesoEnEjecucion
            procesoActual.rafagaTotalEjecutada = procesoActual.rafagaTotalEjecutada + procesoActual.rafagaEjecutada
            procesoActual.pausa()
            procesoActual.estadoSemaforo = "Expulsado"
            procesoActual.cambiaSemaforo = True
            self.fcfs.colaTerminados.append(procesoActual.__dict__)
            num = int(procesoActual.nombre[1:]) + 1
            nombreNuevo = procesoActual.nombre[0:1] + str(num)
            llegadaNueva = procesoActual.llegada
            rafagaNueva = procesoActual.rafaga - procesoActual.rafagaEjecutada
            rafagaTotalEjecutadaNueva = procesoActual.rafagaTotalEjecutada
            procesoNuevo = Proceso(nombreNuevo, llegadaNueva, rafagaNueva, rafagaTotalEjecutadaNueva)
            procesoNuevo.estadoSemaforo = "Listo"
            self.fcfs.colaListo.agregarProceso(procesoNuevo)
            self.procesoEnEjecucion = None
            self.fcfs.procesoEnEjecucion = None



        if self.procesoEnEjecucion is None:
            if procesoEnRR != "No hay mas procesos":
                self.rr.tick()
                self.sjf.avanzaTiempoSinEj()
                self.fcfs.avanzaTiempoSinEj()
                self.colaActiva = "RR"
                self.procesoEnEjecucion = self.rr.procesoEnEjecucion
                if procesoEnSFJ != "No hay mas procesos":
                    self.tiempoIntentoSJF += 1
                if procesoEnFCFS != "No hay mas procesos":
                    self.tiempoIntentoFCFS += 1

            elif procesoEnSFJ != "No hay mas procesos":
                self.rr.avanzaTiempoSinEj()
                self.sjf.tick()
                self.fcfs.avanzaTiempoSinEj()                
                self.colaActiva = "SFJ"
                self.procesoEnEjecucion = self.sjf.procesoEnEjecucion
                if procesoEnFCFS != "No hay mas procesos":
                    self.tiempoIntentoFCFS += 1

            elif procesoEnFCFS != "No hay mas procesos":
                self.rr.avanzaTiempoSinEj()
                self.sjf.avanzaTiempoSinEj()
                self.fcfs.tick()
                self.colaActiva = "FCFS"
                self.procesoEnEjecucion = self.fcfs.procesoEnEjecucion  
            else:
                self.rr.avanzaTiempoSinEj()
                self.sjf.avanzaTiempoSinEj()
                self.fcfs.avanzaTiempoSinEj()  
        else:
            if self.colaActiva == "RR":
                self.rr.tick()
                self.procesoEnEjecucion = self.rr.procesoEnEjecucion                
                if self.procesoEnEjecucion is None:
                    #No hay mas procesos en la cola de RR, verifica si puede hacer tick en otra
                    self.sjf.tick()
                    self.procesoEnEjecucion = self.sjf.procesoEnEjecucion
                    self.colaActiva = "SJF"
                    self.tiempoIntentoSJF = 0
                    if self.procesoEnEjecucion is None:
                        #No hay mas procesos en la cola de SJF, verifica si puede hacer tick en FCFS
                        self.fcfs.tick()   
                        self.procesoEnEjecucion = self.fcfs.procesoEnEjecucion
                        self.colaActiva = "FCFS"
                        self.tiempoIntentoFCFS = 0
                    else:
                        self.fcfs.avanzaTiempoSinEj()
                        self.tiempoIntentoFCFS += 1
                else:
                    self.sjf.avanzaTiempoSinEj()
                    self.fcfs.avanzaTiempoSinEj()
                    if procesoEnSFJ != "No hay mas procesos":
                        self.tiempoIntentoSJF += 1
                    if procesoEnFCFS != "No hay mas procesos":
                        self.tiempoIntentoFCFS += 1
                
            elif self.colaActiva == "SFJ":
                self.rr.avanzaTiempoSinEj()
                self.sjf.tick()
                self.procesoEnEjecucion = self.sjf.procesoEnEjecucion
                self.colaActiva = "SJF"
                self.tiempoIntentoSJF = 0
                if self.procesoEnEjecucion is None:
                    #No hay mas procesos en la cola de SJF, verifica si puede hacer tick en FCFS
                    self.fcfs.tick()   
                    self.procesoEnEjecucion = self.fcfs.procesoEnEjecucion
                    self.colaActiva = "FCFS"
                    self.tiempoIntentoFCFS = 0
                else:
                    self.fcfs.avanzaTiempoSinEj()
                    self.tiempoIntentoFCFS += 1

            elif self.colaActiva == "FCFS":
                self.rr.avanzaTiempoSinEj()
                self.sjf.avanzaTiempoSinEj()
                self.fcfs.tick()
                self.colaActiva = "FCFS"
                self.procesoEnEjecucion = self.fcfs.procesoEnEjecucion  
        
        if self.tiempoIntentoSJF >= 5 and procesoEnSFJ != "No hay mas procesos":
            self.tiempoIntentoSJF = 0
            self.sjf.colaListo.deleteAt(procesoEnSFJ.nombre)
            self.rr.agregarDeOtraCola(procesoEnSFJ)
            

        if self.tiempoIntentoFCFS >= 5 and procesoEnFCFS != "No hay mas procesos":
            self.tiempoIntentoFCFS = 0
            self.fcfs.colaListo.obtener(True)  
            self.sjf.agregarDeOtraCola(procesoEnFCFS)
           

        self.tiempo += 1
        return {"tiempo": self.tiempo}