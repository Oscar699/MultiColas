import random
import sys
import threading

import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from Window import Window
from procesos import ColasProcesos

# Funcion que genera un random
def generarRandom(max):
    return random.randint(1, max)

# Hilo que agrega procesos a las colas
# La cola depende de un random generado
def agregarProcesosThread(cola, numProceso, totalProcesos, maxRafaga):
    for i in range(0, totalProcesos):
        tipoCola = generarRandom(3)
        segEspera = generarRandom(5)
        time.sleep(segEspera)
        rafaga = generarRandom(maxRafaga)
        if tipoCola == 1:
            cola.agregarRR(f"{chr(numProceso + 65)}0", rafaga)
        elif tipoCola == 2:
            cola.agregarSJF(f"{chr(numProceso + 65)}0", rafaga)
        elif tipoCola == 3:
            cola.agregarFCFS(f"{chr(numProceso + 65)}0", rafaga)

        numProceso += 1

# Hilo que bloquea a los procesos segun la cola activa en ese momento
# Vease la funcion bloquear en la clase ColaProcesos
def bloquearProcesosThread(cola):
    for i in range(0, 7):
        segEspera = generarRandom(5)
        time.sleep(segEspera)
        cola.bloquear()
        segEspera = 1 + generarRandom(5)
        time.sleep(segEspera)
        cola.desbloquear()


if __name__ == "__main__":

    # Variables de control de simulacion
    maxProcesosIniciales = 4                                    # Numero maximo de procesos iniciales
    numProcesosIniciales = generarRandom(maxProcesosIniciales)  # Numero procesos iniciales segun maximo
    # numProcesosIniciales = 20
    maxProcesosThread = 4                                       # Numero maximo de procesos que seran añadidos con el tiempo
    numProcesosThread = generarRandom(maxProcesosThread)        # Numero de procesos añadidos segun maximo
    maxRafaga = 7                                               # Numero maximo para la rafaga de los procesos


    app = QApplication(sys.argv)
    timer = QTimer()

    
    cola = ColasProcesos()
    numProceso = 0

    # Ciclo para agregar los procesos iniciales a cada cola de manera aleatoria
    for numProceso in range(numProcesosIniciales):
        tipoCola = generarRandom(3)
        if tipoCola == 1:
            cola.agregarRR(f"{chr(numProceso + 65)}0", generarRandom(maxRafaga))
        elif tipoCola == 2:
            cola.agregarSJF(f"{chr(numProceso + 65)}0", generarRandom(maxRafaga))
        elif tipoCola == 3:
            cola.agregarFCFS(f"{chr(numProceso + 65)}0", generarRandom(maxRafaga))

    # Comprobacion del numero total de procesos
    numProcesoSimulacion = numProcesosIniciales + numProcesosThread
    print(f"numProcesoSimulacion:{numProcesosIniciales} -- numProcesosThread:{numProcesosThread}")

    window = Window(cola)

    agregando_procesos = threading.Thread(target=agregarProcesosThread, args=(cola, numProceso+1, numProcesosThread, maxRafaga,))
    agregando_procesos.start()

    bloquear_procesos = threading.Thread(target=bloquearProcesosThread, args=(cola,))
    bloquear_procesos.start()

    timer.timeout.connect(window.paint)
    timer.start(1000)

    app.exec()