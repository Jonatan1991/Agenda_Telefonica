from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QTextEdit
)

from models.contacto_models import Contacto
from models.direccion_models import Direccion
from models.contacto_info_models import InfoContactos


class ContactoDialog(QDialog):

    def __init__(self, controller, contacto=None):
        super().__init__()

        self.controller = controller
        self.contacto = contacto

        self.setWindowTitle("Nuevo contacto" if not contacto else "Editar contacto")
        self.setMinimumSize(400, 900)

        self._crear_interfaz()

        if contacto:
            self._cargar_datos()

    def _crear_interfaz(self):

        layout = QVBoxLayout()

        form = QFormLayout()

        # CAMPOS
        self.input_nombre = QLineEdit()
        self.input_apellido_1 = QLineEdit()
        self.input_apellido_2 = QLineEdit()
        self.input_email = QLineEdit()
        self.input_telefono_1 = QLineEdit()
        self.input_nota_1 = QTextEdit()
        self.input_nota_1.setMaximumHeight(60)

        self.input_calle = QLineEdit()
        self.input_numero = QLineEdit()
        self.input_piso = QLineEdit()
        self.input_puerta = QLineEdit()
        self.input_escalera = QLineEdit()
        self.input_cp = QLineEdit()
        self.input_provincia = QLineEdit()

        self.input_telefono_2 = QLineEdit()
        self.input_nota_2 = QTextEdit()
        self.input_nota_2.setMaximumHeight(60)
        
        self.input_telefono_3 = QLineEdit()
        self.input_nota_3 = QTextEdit()
        self.input_nota_3.setMaximumHeight(60)
        
        self.input_telefono_4 = QLineEdit()
        self.input_nota_4 = QTextEdit()
        self.input_nota_4.setMaximumHeight(60)
        
        self.input_auxiliar = QLineEdit()
        self.input_observaciones = QTextEdit()
        self.input_observaciones.setMinimumHeight(80)

        form.addRow("Nombre", self.input_nombre)
        form.addRow("Apellido 1", self.input_apellido_1)
        form.addRow("Apellido 2", self.input_apellido_2)
        form.addRow("Email", self.input_email)
        form.addRow("Teléfono 1", self.input_telefono_1)
        form.addRow("Nota 1", self.input_nota_1)

        form.addRow("Calle", self.input_calle)
        form.addRow("Número", self.input_numero)
        form.addRow("Piso", self.input_piso)
        form.addRow("Puerta", self.input_puerta)
        form.addRow("Escalera", self.input_escalera)
        form.addRow("CP", self.input_cp)
        form.addRow("Provincia", self.input_provincia)

        form.addRow("Teléfono 2", self.input_telefono_2)
        form.addRow("Nota 2", self.input_nota_2)
        form.addRow("Teléfono 3", self.input_telefono_3)
        form.addRow("Nota 3", self.input_nota_3)
        form.addRow("Teléfono 4", self.input_telefono_4)
        form.addRow("Nota 4", self.input_nota_4)
        form.addRow("Auxiliar", self.input_auxiliar)
        form.addRow("Observaciones", self.input_observaciones)

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
        apellido_1 = self.input_apellido_1.text()
        apellido_2 = self.input_apellido_2.text()
        # telefono = self.input_telefono.text()
        # email = self.input_email.text()

        info_contacto = InfoContactos(
            email=self.input_email.text(),
            telefono_1=self.input_telefono_1.text(),
            nota_1=self.input_nota_1.toPlainText(),
            telefono_2=self.input_telefono_2.text(),
            nota_2=self.input_nota_2.toPlainText(),
            telefono_3=self.input_telefono_3.text(),
            nota_3=self.input_nota_3.toPlainText(),
            telefono_4=self.input_telefono_4.text(),
            nota_4=self.input_nota_4.toPlainText(),
            auxiliar=self.input_auxiliar.text(),
            observaciones=self.input_observaciones.toPlainText()
        )

        direccion = Direccion(
            calle=self.input_calle.text(),
            numero=self.input_numero.text(),
            piso=self.input_piso.text(),
            puerta=self.input_puerta.text(),
            escalera=self.input_escalera.text(),
            cp=self.input_cp.text(),
            provincia=self.input_provincia.text()
        )

        try:

            contacto_obj = Contacto(
                nombre=nombre,
                apellido_1=apellido_1,
                apellido_2=apellido_2,

                direccion=direccion,
                info_contactos=info_contacto
            )

            if self.contacto:

                self.controller.editar_contacto(
                    self.contacto["id"],
                    contacto_obj
                )

            else:

                self.controller.agregar_contacto(contacto_obj)

            self.accept()

        except ValueError as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

            
    def _cargar_datos(self):

        self.input_nombre.setText(self.contacto.get("nombre", ""))
        self.input_apellido_1.setText(self.contacto.get("apellido_1", ""))
        self.input_apellido_2.setText(self.contacto.get("apellido_2", ""))
        info_contactos = self.contacto.get("info_contactos", {})

        self.input_email.setText(info_contactos.get("email", ""))
        self.input_telefono_1.setText(info_contactos.get("telefono_1", ""))
        self.input_nota_1.setPlainText(info_contactos.get("nota_1", ""))
        self.input_telefono_2.setText(info_contactos.get("telefono_2", ""))
        self.input_nota_2.setPlainText(info_contactos.get("nota_2", ""))
        self.input_telefono_3.setText(info_contactos.get("telefono_3", ""))
        self.input_nota_3.setPlainText(info_contactos.get("nota_3", ""))
        self.input_telefono_4.setText(info_contactos.get("telefono_4", ""))
        self.input_nota_4.setPlainText(info_contactos.get("nota_4", ""))
        self.input_observaciones.setPlainText(info_contactos.get("observaciones", ""))
        self.input_auxiliar.setText(info_contactos.get("auxiliar", ""))

        direccion = self.contacto.get("direccion", {})

        self.input_calle.setText(direccion.get("calle", ""))
        self.input_numero.setText(direccion.get("numero", ""))
        self.input_piso.setText(direccion.get("piso", ""))
        self.input_puerta.setText(direccion.get("puerta", ""))
        self.input_escalera.setText(direccion.get("escalera", ""))
        self.input_cp.setText(direccion.get("cp", ""))
        self.input_provincia.setText(direccion.get("provincia", ""))