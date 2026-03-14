from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)


class ContactoDialog(QDialog):

    def __init__(self, controller, contacto=None):
        super().__init__()

        self.controller = controller
        self.contacto = contacto

        self.setWindowTitle("Nuevo contacto")

        self._crear_interfaz()

        if contacto:
            self._cargar_datos()

    def _crear_interfaz(self):

        layout = QVBoxLayout()

        form = QFormLayout()

        # CAMPOS
        self.input_nombre = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_email = QLineEdit()

        self.input_calle = QLineEdit()
        self.input_numero = QLineEdit()
        self.input_municipio = QLineEdit()
        self.input_cp = QLineEdit()

        form.addRow("Nombre", self.input_nombre)
        form.addRow("Teléfono", self.input_telefono)
        form.addRow("Email", self.input_email)

        form.addRow("Calle", self.input_calle)
        form.addRow("Número", self.input_numero)
        form.addRow("Municipio", self.input_municipio)
        form.addRow("CP", self.input_cp)

        layout.addLayout(form)

        # BOTONES
        botones = QHBoxLayout()

        self.btn_guardar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")

        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_cancelar)

        layout.addLayout(botones)

        self.setLayout(layout)

        # EVENTOS
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_cancelar.clicked.connect(self.reject)

    def guardar(self):

        nombre = self.input_nombre.text()
        telefono = self.input_telefono.text()
        email = self.input_email.text()

        direccion = {
            "calle": self.input_calle.text(),
            "numero": self.input_numero.text(),
            "municipio": self.input_municipio.text(),
            "cp": self.input_cp.text()
        }

        try:

            if self.contacto:

                self.controller.editar_contacto(
                    self.contacto["id"],
                    nombre=nombre,
                    telefono=telefono,
                    email=email,
                    direccion=direccion
                )

            else:

                self.controller.agregar_contacto(
                    nombre,
                    telefono,
                    email,
                    direccion
                )

            self.accept()

        except ValueError as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

            
    def _cargar_datos(self):

        self.input_nombre.setText(self.contacto["nombre"])
        self.input_telefono.setText(self.contacto["telefono"])
        self.input_email.setText(self.contacto["email"])

        direccion = self.contacto.get("direccion", {})

        self.input_calle.setText(direccion.get("calle", ""))
        self.input_numero.setText(direccion.get("numero", ""))
        self.input_municipio.setText(direccion.get("municipio", ""))
        self.input_cp.setText(direccion.get("cp", ""))