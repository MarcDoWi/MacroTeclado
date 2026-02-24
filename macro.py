# Macro que hace que se haga click izquierdo repetidamente durante 30 segundos

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, GlobalHotKeys, Controller as KeyboardController
from errors import MoreThanOneKeyError, NumberIsNotPositiveError, OptionNotValidError
import time
import threading
import json


#Variables para el funcionamiento del programa
running = True
mouse = MouseController()
keyboard = KeyboardController()

# Configuraciones
config_awaiting_time_before_macro_starts = 5
options_tuple = (1, 2, 3, 4)
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

macro_stop_listener = GlobalHotKeys({
    '<ctrl>+<alt>+q': stop_macro
    })

def ask_key():
    global messages_file
    while True:
        try:
            tecla = input(messages_file["asking_key_to_press_message"])
            if len(tecla) == 1:
                return tecla
            else:
                raise MoreThanOneKeyError(messages_file["value_error_press_just_one_key_message"])
        except KeyboardInterrupt:
            print(messages_file["program_exiting_message"])
            exit()
        except MoreThanOneKeyError as exception:
            print(exception)

def ask_duration():
    global messages_file
    while True:
        try:
            duracion = int(input(messages_file["asking_macro_duration_message"]))
            if duracion <= 0:
                raise NumberIsNotPositiveError
            return duracion
        except KeyboardInterrupt:
            print(messages_file["program_exiting_message"])
            exit()
        except ValueError as exception:
            print(messages_file["value_error_value_is_not_a_number_message"])
        except NumberIsNotPositiveError as exception:
            print(exception)

def ask_key_press_count():
    global messages_file
    while True:
        try:
            clicks = int(input(messages_file["asking_number_of_clicks_message"]))
            if clicks <= 0:
                raise NumberIsNotPositiveError
            return clicks
        except KeyboardInterrupt:
            print(messages_file["program_exiting_message"])
            exit()
        except ValueError as exception:
            print(exception)
        except NumberIsNotPositiveError as exception:
            print(exception)


def mouse_dblclick():
    global messages_file
    duracion = ask_duration()

    print(messages_file["macro_starting_with_duration_message"].format(duracion=duracion))
    print(messages_file["macro_starting_time_for_macro_to_start_message"].format(config_awaiting_time_before_macro_starts=config_awaiting_time_before_macro_starts))
    time.sleep(config_awaiting_time_before_macro_starts)

    # contador de tiempo que solo avanza, medido en segundos.
    tiempo_inicio = time.monotonic()

    while time.monotonic() - tiempo_inicio < duracion and running:
        mouse.click(Button.left, 2)
        time.sleep(0.5)


# He modificado el método, originalmente la IA me recomendó poner un sleep despues del release para que la cpu no se saturara, esto hacía que la tecla se soltase y no
#   simulaba correctamente el sostenido de la tecla, para solucionarlo he quitado el sleep despues del release y en cambio he puesto uno despues de presionar la tecla,
#   esto hace que la tecla se mantenga presionada durante 1 segundo, lo que simula un sostenido de la tecla, aunque no es exactamente lo mismo que mantenerla presionada sin soltarla,
#   pero es lo más cercano que he podido conseguir con pynput, ya que parece ser que pynput suelta la tecla si el programa no esta con el foco activo, probablemente
#   para evitar que la tecla se mantenga permanentemente apretada.
def hold_key():
    global messages_file
    key = ask_key()
    duracion = ask_duration()

    print(messages_file["macro_starting_with_duration_message"].format(duracion=duracion))
    print(messages_file["macro_starting_time_for_macro_to_start_message"].format(config_awaiting_time_before_macro_starts=config_awaiting_time_before_macro_starts))
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
def press_key_repeatedly():
    global messages_file
    key = ask_key()
    clicks = ask_key_press_count()

    print(messages_file["macro_starting_with_clicks_count_and_key_message"].format(key=key, clicks=clicks))
    print(messages_file["macro_starting_time_for_macro_to_start_message"].format(config_awaiting_time_before_macro_starts=config_awaiting_time_before_macro_starts))
    time.sleep(config_awaiting_time_before_macro_starts)

    for i in range(clicks):
        if not running:
            break
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(1)

def macro_open_pokemon_eggs():
    global messages_file
    duration = ask_duration()

    print(messages_file["macro_starting_with_duration_message"].format(duracion=duration))
    print(messages_file["macro_starting_time_for_macro_to_start_message"].format(config_awaiting_time_before_macro_starts=config_awaiting_time_before_macro_starts))
    time.sleep(config_awaiting_time_before_macro_starts)

    starting_time = time.monotonic()
    while time.monotonic() - starting_time < duration and running:
        keyboard.press("a")
        keyboard.press(Key.right)
        time.sleep(0.5)
        keyboard.release(Key.right)
        time.sleep(1.5)
        keyboard.release("a")

        keyboard.press("d")
        keyboard.press(Key.right)
        time.sleep(0.5)
        keyboard.release(Key.right)
        time.sleep(1.5)
        keyboard.release("d")
    



# Aqui creamos un hilo secundario (sabemos que es secundario por daemon=True, que indica que es secundario y hace que cuando el programa termine el hilo se muera solo, evitando un proceso "zombie")
threading.Thread(target=macro_stop_listener.start, daemon=True).start()

print(messages_file["welcome_message"])
print(messages_file["Software_on_development_message"])
print(messages_file["Future_graphical_interface_message"])

print(messages_file["display_options_message"])

# Bloque que solicita una opción de las disponibles y maneja la excepción en caso de que el usuario ingrese algo que no sea un número entero
while True:
    try:
        opcion = int(input(messages_file["choose_option_message"]))
        if opcion not in options_tuple:
            raise OptionNotValidError(options_tuple)
        break
    except KeyboardInterrupt:
        print(messages_file["program_exiting_message"])
        exit()
    except ValueError:
        print(messages_file["value_error_value_is_not_a_number_message"])
    except OptionNotValidError as exception:
        print(exception)

# Aqui manejamos las diferentes opciones del menú, en caso de que el usuario ingrese una opción que no sea 1 o 2, se le indicará que la opción no es válida
match opcion:
    case 1:
        print(messages_file["option_selected_click_left_repeated_message"])
        mouse_dblclick()
    case 2:
        print(messages_file["option_selected_hold_key_message"])
        hold_key()
    case 3:
        print(messages_file["option_selected_press_key_repeatedly_message"])
        press_key_repeatedly()
    case 4:
        print(messages_file["option_selected_open_pokemon_eggs_message"])
        macro_open_pokemon_eggs()
    case _:
        print(messages_file["option_not_available_message"].format(option = opcion))


#Posibles expansiones:
    # 💡 El programa podría preguntar una cantidad de teclas a intercalar -> Posibilidad de abrir huevos pokemon para ello crearemos una estructura del tamaño que diga el usuario y con esto haremos la presion de las teclas

#Implementaciones a futuro:
    # 💡 En el futuro se puede añadir un método que permita ejecutar diferentes métodos, (ej: click repetido x veces, luego mantener una tecla presionada, luego volver a hacer click repetido, etc.)
    # 💡 Implementar interfaz gráfica
    # 💡 Hacer un .exe.
    # 💡 me gustaría que el usuario no tenga que instalar Python para usar el programa

#Próximo:
#1. 💡Implementar interfaz gráfica.
#2. 💡Implementar teclas como flechas, alt, intro, etc (Osea, que el usuario pueda introducir estas teclas) -> Creo que esto será mas fácil de solucionar con interfaz gráfica
#3. 💡Comprobar si el programa diferencia entre por ejemplo alt izquierda y alt derecha.
