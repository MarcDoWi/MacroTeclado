import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel("Hola Mundo")
label.show()
app.exec()