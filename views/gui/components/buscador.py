from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)


class Buscador(QWidget):

    def __init__(self, on_change_callback=None, placeholder="Buscar..."):
        super().__init__()
        self._on_change_callback = on_change_callback
        self._crear_interfaz(placeholder)

    def _crear_interfaz(self, placeholder):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.lbl_buscar = QLabel("Buscar:")
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText(placeholder)

        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.clicked.connect(self.limpiar)

        self.txt_buscar.textChanged.connect(self._emitir_cambio)

        layout.addWidget(self.lbl_buscar)
        layout.addWidget(self.txt_buscar)
        layout.addWidget(self.btn_limpiar)

    def _emitir_cambio(self):
        if self._on_change_callback:
            self._on_change_callback(self.txt_buscar.text())

    def set_text(self, text):
        self.txt_buscar.setText(text)

    def get_text(self):
        return self.txt_buscar.text()
    
    def limpiar(self):
        self.txt_buscar.clear()