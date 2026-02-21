# Macro que hace que se haga click izquierdo repetidamente durante 30 segundos

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, GlobalHotKeys, Controller as KeyboardController, Listener
import time
import threading
import json


#Variables para el funcionamiento del programa
running = True
mouse = MouseController()
keyboard = KeyboardController()

# Configuraciones
config_awaiting_time_before_macro_starts = 5
options_tuple = (1, 2, 3)
language = "es"
messages_file = None
# ❓ Debería hacer un time para el sleep del final de cada vuelta del bucle de las marcos?


# 🔴 COMBINACIÓN PARA PARAR: Ctrl + Alt + Q
STOP_COMBO = {Key.ctrl_l, Key.alt_l, 'q'}

# Esta función carga los mensajes del archivo de idiomas correspondiente, actualmente solo hay uno (es.json) pero en el futuro se pretenden añadir mas idiomas, para ello solo
#   habría que crear un nuevo archivo json con los mensajes traducidos y añadir el código necesario para que el programa pueda elegir entre los diferentes idiomas, probablemente
#   añadiendo una opción en el menú principal para elegir el idioma.
def load_messages(language):
    with open(f"locales/{language}.json", "r", encoding="utf-8") as messages_file:
        return json.load(messages_file)
    
messages_file = load_messages(language)

def stop_macro():
    global running
    global messages_file
    running = False
    print(messages_file["macro_finishing_message"])
    #print("Finalizando macro...")

macro_stop_listener = GlobalHotKeys({
    '<ctrl>+<alt>+q': stop_macro
    })

def ask_key():
    global messages_file
    while True:
        try:
            tecla = input(messages_file["asking_key_to_press_message"])
            #tecla = input("Ingresa la tecla a presionar (Ctrl + C para salir): ")
            if len(tecla) != 1:
                return tecla
            else:
                #raise ValueError("Por favor ingresa solo una tecla.")
                raise ValueError(messages_file["value_error_press_just_one_key_message"])
        except KeyboardInterrupt:
            print(messages_file["program_exiting_message"])    
            #print("\nSaliendo del programa...")
            exit()
        except ValueError as exception:
            print(exception)

def ask_duration():
    global messages_file
    while True:
        try:
            duracion = int(input(messages_file["asking_macro_duration_message"]))
            if duracion <= 0:
                raise ValueError(messages_file["value_error_not_positive_number_message"])
            return duracion
        except KeyboardInterrupt:
            print(messages_file["program_exiting_message"])
            exit()
        except ValueError as exception:
            print(exception)

def ask_key_press_count():
    global messages_file
    while True:
        try:
            clicks = int(input(messages_file["asking_number_of_clicks_message"]))
            #clicks = int(input("Introduce la cantidad de clicks a realizar: (Ctrl + C para salir): "))
            if clicks <= 0:
                raise ValueError(messages_file["value_error_not_positive_number_message"])
                #raise ValueError("Por favor ingresa un número positivo.")
            return clicks
        except KeyboardInterrupt:
            print(messages_file["program_exiting_message"])
            #print("\nSaliendo del programa...")
            exit()
        except ValueError as exception:
            print(exception)


def mouse_dblclick():
    global messages_file
    duracion = ask_duration()

    print(messages_file["macro_starting_with_duration_message"].format(duracion=duracion))
    #print(f"Macro iniciada con duración {duracion} (Ctrl+Alt+Q para detener)\n")
    print(messages_file["macro_starting_time_for_macro_to_start_message"].format(config_awaiting_time_before_macro_starts=config_awaiting_time_before_macro_starts))
    #print(f"El macro se iniciará en {config_awaiting_time_before_macro_starts} segundos...\n")
    time.sleep(config_awaiting_time_before_macro_starts)

    # contador de tiempo que solo avanza, medido en segundos.
    tiempo_inicio = time.monotonic()

    while time.monotonic() - tiempo_inicio < duracion and running:
        mouse.click(Button.left, 2)
        time.sleep(1)


# He modificado el método, originalmente la IA me recomendó poner un sleep despues del release para que la cpu no se saturara, esto hacía que la tecla se soltase y no
#   simulaba correctamente el sostenido de la tecla, para solucionarlo he quitado el sleep despues del release y en cambio he puesto uno despues de presionar la tecla,
#   esto hace que la tecla se mantenga presionada durante 1 segundo, lo que simula un sostenido de la tecla, aunque no es exactamente lo mismo que mantenerla presionada sin soltarla,
#   pero es lo más cercano que he podido conseguir con pynput, ya que parece ser que pynput suelta la tecla si el programa no esta con el foco activo, probablemente
#   para evitar que la tecla se mantenga permanentemente apretada.
def hold_key(key, duracion):
    global messages_file
    key = ask_key()
    duracion = ask_duration()

    print(messages_file["macro_starting_with_duration_message"].format(duracion=duracion))
    #print(f"Macro iniciada con duración {duracion} (Ctrl+Alt+Q para detener)\n") 
    print(messages_file["macro_starting_time_for_macro_to_start_message"].format(config_awaiting_time_before_macro_starts=config_awaiting_time_before_macro_starts))
    #print(f"El macro se iniciará en {config_awaiting_time_before_macro_starts} segundos...\n")
    time.sleep(config_awaiting_time_before_macro_starts)

    tiempo_inicio = time.monotonic()
    try:
        while (time.monotonic() - tiempo_inicio < duracion) and running:

            #Se pretendía mantener la tecla, pero parece ser que pynput suelta la tecla si el programa no esta con el foco activo, probablemente para evitar que la tecla se mantenga permanentemente apretada
            keyboard.press(key)
            time.sleep(1)
            keyboard.release(key)
    finally:
        keyboard.release(key)


# Método que permite hacer x clicks repetidos a una tecla
# ‼️ Falta testear
def press_key_repeatedly(key, clicks):
    global messages_file
    key = ask_key()
    clicks = ask_key_press_count()

    print(messages_file["macro_starting_with_clicks_count_and_key_message"].format(key=key, clicks=clicks))
    # print(f"Presionando la tecla {key} {clicks} veces (Ctrl+Alt+Q para detener)\n")
    print(messages_file["macro_starting_time_for_macro_to_start_message"].format(config_awaiting_time_before_macro_starts=config_awaiting_time_before_macro_starts))
    # print(f"El macro se iniciará en {config_awaiting_time_before_macro_starts} segundos...\n")
    time.sleep(config_awaiting_time_before_macro_starts)

    for i in range(clicks):
        if not running:
            break
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(1)
    



# Aqui creamos un hilo secundario (sabemos que es secundario por daemon=True, que indica que es secundario y hace que cuando el programa termine el hilo se muera solo, evitando un proceso "zombie")
threading.Thread(target=macro_stop_listener.start, daemon=True).start()

print(messages_file["welcome_message"])
# print("\n\nEste es un Macro desarrollado por Marc Hernández Martínez")
print(messages_file["Software_on_development_message"])
# print("El software aun esta en desarrollo, así que ten paciencia con los bugs :)\n")
print(messages_file["Future_graphical_interface_message"])
# print("Temporalmente con finalidades de testeos se implementará un menú por consola para elegir entre diferentes macros, pero en un futuro se implementará una interfaz gráfica\n")

print(messages_file["display_options_message"])
# print("Opcion 1 -> Doble click izquierdo repetido")
# print("Opcion 2 -> Mantener tecla presionada")
# print("Opcion 3 -> Realizar x clicks de una tecla\n")


# Bloque que solicita una opción de las disponibles y maneja la excepción en caso de que el usuario ingrese algo que no sea un número entero
while True:
    try:
        opcion = int(input(messages_file["choose_option_message"]))
        # opcion = int(input("Elige una opción (Ctrl + C para salir): "))
        if opcion not in options_tuple:
            # Aunque se que el mensaje del ValueError no se mostrará al usuario, lo pongo para mantener la coherencia con el resto del código,
            #   que utiliza mensajes personalizados para cada error.
            raise ValueError(messages_file["option_not_valid_message"].format(options_tuple=options_tuple))
        break
    except KeyboardInterrupt:
        print(messages_file["program_exiting_message"])
        # print("\nSaliendo del programa...")
        exit()
    except ValueError:
        print(messages_file["option_not_valid_message"].format(options_tuple=options_tuple))
        # print("Opción no válida, por favor ingresa un número.")

# ❓ Redundante? En cada case se vuelve a imprimir la opción elegida
print(messages_file["option_chosen_message"].format(opcion=opcion))
# print(f"Has elegido la opción {opcion}\n")


# Aqui manejamos las diferentes opciones del menú, en caso de que el usuario ingrese una opción que no sea 1 o 2, se le indicará que la opción no es válida
match opcion:
    case 1:
        print(messages_file["option_selected_click_left_repeated_message"])
        #print("Has elegido la opción click izquierdo repetido")
        mouse_dblclick()
    case 2:
        print(messages_file["option_selected_hold_key_message"])
        #print("Has elegido la opción de mantener una tecla presionada")
        hold_key()
    case 3:
        print(messages_file["option_selected_press_key_repeatedly_message"])
        #print("Has elegido la opción de realizar x clicks de una tecla")
        press_key_repeatedly()
    case _:
        print(messages_file["option_not_available_message"].format(option = opcion))
        # print("Esta opción no esta disponible, Si sale este mensaje es un error, por favor reportalo al desarrollador")


#Posibles expansiones:
    # 💡 El programa podría preguntar una cantidad de teclas a intercalar -> Posibilidad de abrir huevos pokemon para ello crearemos una estructura del tamaño que diga el usuario y con esto haremos la presion de las teclas

#Implementaciones a futuro:
    # 💡 Comprobar si el programa diferencia entre por ejemplo alt izquierda y alt derecha.
    # 💡 Añadir método para hacer x cantidades de clicks de x tecla.
    # 💡 Añadir un método que permita abrir huevos pokemon.
    # 💡 En el futuro se puede añadir un método que permita ejecutar diferentes métodos, (ej: click repetido x veces, luego mantener una tecla presionada, luego volver a hacer click repetido, etc.)
    # 💡 Hacer funciones para pedir la tecla, duración del macro y cantidad de clicks

#Próximo:
    #1. 💡 Testear los mensajes del JSON (recordar que el del case_ no se puede testear sin quitar el previo checkeo de la opción que selecciona el usuario).
    #2. 💡 Tengo que mover el pedir la duración del macro solo a los cases que correspondan. -> He creado los métodos, falta implementarlos. -> Estan implementados, falta testear.
