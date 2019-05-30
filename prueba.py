import threading
import time


lista = []

segundos = 0.1
def contar():
    contador = 0
    inicial = time.time()
    limite = inicial + segundos
    nombre = threading.current_thread().getName()
    while inicial<=limite:
        contador+=1
        inicial = time.time()
        lista.append(contador)
        print("se agregó el elem ",contador)


    
def size():
    inicial = time.time()
    limite = inicial + segundos
    nombre = threading.current_thread().getName()
    while inicial<=limite:
        inicial = time.time()
        print("El tam de la lista es: ",len(lista))


lista = []

thread1 = threading.Thread(target=contar)
thread2 = threading.Thread(target=size)
thread1.start()
thread2.start()
