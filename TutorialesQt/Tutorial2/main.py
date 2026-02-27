import sys
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Slot

#Greetings
@Slot()
def say_hello():
    print("Button clicked, Hello!")

app = QApplication(sys.argv)
button = QPushButton("Click me")

#Connect the button to the function
button.clicked.connect(say_hello)

button.show()
app.exec()
 