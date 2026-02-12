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
def mouse_dblclick(duracion):

# Temporalizador x segundos:

    print(f"Macro iniciada con duración {duracion} (Ctrl+Alt+Q para detener)\n") 
    time.sleep(1)

    # contador de tiempo que solo avanza, medido en segundos.
    tiempo_inicio = time.monotonic()

    while time.monotonic() - tiempo_inicio < duracion and running:
        mouse.click(Button.left, 1)
        mouse.click(Button.left, 1)
        time.sleep(1)



def hold_key(key, duracion):

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

print("\n\nEste es un Macro desarrollado por Marc Hernández Martínez")
print("El software aun esta en desarrollo, así que ten paciencia con los bugs :)\n")

print("Temporalmente con finalidades de testeos se implementará un menú por consola para elegir entre diferentes macros, pero en un futuro se implementará una interfaz gráfica\n")
print("Opcion 1 -> Doble click izquierdo repetido")
print("Opcion 2 -> Mantener tecla presionada\n")


# Bloque que solicita una opción de las disponibles y maneja la excepción en caso de que el usuario ingrese algo que no sea un número entero
while True:
    try:
        opcion = int(input("Elige una opción: "))
        if opcion not in [1, 2]:
            print("Opción no válida, por favor elige una opción entre 1 y 2.")
            continue
        break
    except ValueError:
        print("Opción no válida, por favor ingresa un número.")

print("Has elegido la opción ", opcion)


# Bloque que solicita la duración del macro y maneja la excepción en caso de que el usuario ingrese algo que no sea un número entero
while True:
    try:
        duracion = int(input("Durante cuantos segundos deseas ejecutar el macro? "))
        break
    except ValueError:
        print("\nOpción no válida, por favor ingresa un número.\n")

# Aqui manejamos las diferentes opciones del menú, en caso de que el usuario ingrese una opción que no sea 1 o 2, se le indicará que la opción no es válida
match opcion:
    case 1:
        mouse_dblclick(duracion)
    case 2:
        print("Has elegido la opción de mantener una tecla presionada, por favor ingresa la tecla que quieres mantener presionada (ejemplo: 'a', 'b', 'c', etc.)")
        while True:
            try:
                tecla = input("Ingresa la tecla: ")
                if len(tecla)   != 1:
                    raise ValueError("Por favor ingresa solo una tecla.")
                else:
                    break
            except ValueError as exception:
                print(exception)
        hold_key(tecla, duracion)
    case _:
        print("Esta opción no esta disponible, Si sale este mensaje es un error, por favor reportalo al desarrollador")


#Posibles expansiones: El programa podría preguntar una cantidad de teclas a intercalar -> Posibilidad de abrir huevos pokemon para ello crearemos una estructura del tamaño que diga el usuario y con esto haremos la presion de las teclas
#Preguntar cuanto tiempo se quiere que dure el macro
#Subir a GitHub y llevar control de versiones -> Realizado el 11/02/2026