import sys
from PySide6.QtWidgets import QApplication

app = QApplication([])
label = QLabel("Hola Mundo")
label.show()
app.exec()