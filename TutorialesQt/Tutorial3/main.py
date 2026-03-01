import sys
from PySide6.QtWidgets import QApplication, QPushButton
from Boton import Boton

def function():
    print("The 'function' has been called!")

app = QApplication(sys.argv)
button = Boton("Call function")
button.clicked.connect(function)
button.show()
sys.exit(app.exec())