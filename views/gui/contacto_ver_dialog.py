from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QHBoxLayout
)


class ContactoVerDialog(QDialog):

    def __init__(self, contacto):
        super().__init__()

        self.contacto = contacto or {}

        self.setWindowTitle("Ver contacto")
        self.setMinimumSize(500, 650)

        self._crear_interfaz()

    def _crear_interfaz(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        info = self.contacto.get("info_contactos", {})
        direccion = self.contacto.get("direccion", {})

        form.addRow("Nombre", self._label(self.contacto.get("nombre")))
        form.addRow("Apellido 1", self._label(self.contacto.get("apellido_1")))
        form.addRow("Apellido 2", self._label(self.contacto.get("apellido_2")))

        form.addRow("Email", self._label(info.get("email")))
        form.addRow("Telefono 1", self._label(info.get("telefono_1")))
        form.addRow("Nota 1", self._label(info.get("nota_1")))
        form.addRow("Telefono 2", self._label(info.get("telefono_2")))
        form.addRow("Nota 2", self._label(info.get("nota_2")))
        form.addRow("Telefono 3", self._label(info.get("telefono_3")))
        form.addRow("Nota 3", self._label(info.get("nota_3")))
        form.addRow("Telefono 4", self._label(info.get("telefono_4")))
        form.addRow("Nota 4", self._label(info.get("nota_4")))
        form.addRow("Auxiliar", self._label(info.get("auxiliar")))
        form.addRow("Observaciones", self._label(info.get("observaciones")))

        form.addRow("Calle", self._label(direccion.get("calle")))
        form.addRow("Numero", self._label(direccion.get("numero")))
        form.addRow("Piso", self._label(direccion.get("piso")))
        form.addRow("Puerta", self._label(direccion.get("puerta")))
        form.addRow("Escalera", self._label(direccion.get("escalera")))
        form.addRow("CP", self._label(direccion.get("cp")))
        form.addRow("Provincia", self._label(direccion.get("provincia")))

        layout.addLayout(form)

        botones = QHBoxLayout()
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        botones.addWidget(btn_cerrar)
        layout.addLayout(botones)

        self.setLayout(layout)

    def _label(self, valor):
        texto = valor if valor else "N/A"
        label = QLabel(str(texto))
        label.setWordWrap(True)
        return label
