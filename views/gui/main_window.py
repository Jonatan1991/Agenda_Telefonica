from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)

from controllers.agenda_controller import AgendaController
from views.gui.tabla_contactos import TablaContactos
from views.gui.contacto_dialog import ContactoDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controller = AgendaController()

        self.setWindowTitle("Agenda Telefónica")
        self.setMinimumSize(900, 600)

        self._crear_interfaz()

        self.cargar_contactos()

    def _crear_interfaz(self):

        contenedor = QWidget()

        layout_principal = QVBoxLayout()

        # TABLA
        self.tabla = TablaContactos()
        layout_principal.addWidget(self.tabla)

        # BOTONES
        layout_botones = QHBoxLayout()

        self.btn_agregar = QPushButton("Añadir")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_refrescar = QPushButton("Actualizar")

        self.btn_agregar.clicked.connect(self.abrir_formulario)

        layout_botones.addWidget(self.btn_agregar)
        layout_botones.addWidget(self.btn_editar)
        layout_botones.addWidget(self.btn_eliminar)
        layout_botones.addWidget(self.btn_refrescar)

        layout_principal.addLayout(layout_botones)

        contenedor.setLayout(layout_principal)

        self.setCentralWidget(contenedor)

        # EVENTOS
        self.btn_refrescar.clicked.connect(self.cargar_contactos)

    def cargar_contactos(self):

        contactos = self.controller.obtener_contactos()

        self.tabla.cargar_datos(contactos)

    def abrir_formulario(self):

        dialogo = ContactoDialog(self.controller)

        if dialogo.exec():
            self.cargar_contactos()