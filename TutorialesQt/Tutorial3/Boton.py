from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QPushButton

class Boton(QPushButton):

    clicked = Signal(Qt.MouseButton)

    ...

    def mousePressEvent(self, event):
        self.clicked.emit(event.button())
    