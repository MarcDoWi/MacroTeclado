# Macro que hace que se haga click izquierdo repetidamente durante 30 segundos

from pynput.mouse import Button, Controller as MouseController

# Este sirve para poder cambiar la macro a clicks de teclado
from pynput.keyboard import Key, GlobalHotKeys, Controller as KeyboardController, Listener
import time
import threading



running = True
mouse = MouseController()
keyboard = KeyboardController()


# 🔴 COMBINACIÓN PARA PARAR: Ctrl + Alt + Q
STOP_COMBO = {Key.ctrl_l, Key.alt_l, 'q'}


def stop_macro():
    global running
    running = False
    print("Finalizando macro...")

macro_stop_listener = GlobalHotKeys({
    '<ctrl>+<alt>+q': stop_macro
    })


#REVISAR
def mouse_dblclick():

# Temporalizador x segundos:
    duracion = 5

    print(f"Iniciando macro durante {duracion} segundos...")
    time.sleep(1)

    # contador de tiempo que solo avanza, medido en segundos.
    tiempo_inicio = time.monotonic()

    while time.monotonic() - tiempo_inicio < duracion:
        mouse.click(Button.left, 1)
        mouse.click(Button.left, 1)
        time.sleep(1)



def hold_key(key):
    
    duracion = 120

    print(f"Macro iniciada con duración {duracion} (Ctrl+Alt+Q para detener)\n") 
    time.sleep(5)

    tiempo_inicio = time.monotonic()
    try:
        while (time.monotonic() - tiempo_inicio < duracion) and running:

            #Se pretendía mantener la tecla, pero parece ser que pynput suelta la tecla si el programa no esta con el foco activo, probablemente para evitar que la tecla se mantenga permanentemente apretada
            keyboard.press(key)
            keyboard.release(key)
            time.sleep(1)
    finally:
        keyboard.release(key)


# Aqui creamos un hilo secundario (sabemos que es secundario por daemon=True, que indica que es secundario y hace que cuando el programa termine el hilo se muera solo, evitando un proceso "zombie")
threading.Thread(target=macro_stop_listener.start, daemon=True).start()

print("Este es un Macro desarrollado por Marc Hernández Martínez")
print("El software aun esta en desarrollo, así que ten paciencia con los bugs :)")

hold_key('a')


#Posibles expansiones: El programa podría preguntar una cantidad de teclas a intercalar -> Posibilidad de abrir huevos pokemon para ello crearemos una estructura del tamaño que diga el usuario y con esto haremos la presion de las teclas
#Preguntar cuanto tiempo se quiere que dure el macro
#Subir a GitHub y llevar control de versiones