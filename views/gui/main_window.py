from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox
)

from controllers.agenda_controller import AgendaController
from views.gui.tabla_contactos import TablaContactos
from views.gui.contacto_dialog import ContactoDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controller = AgendaController()

        self.setWindowTitle("Agenda Telefónica")
        self.setMinimumSize(1200, 600)

        self._crear_interfaz()

        self.cargar_contactos()

    def _crear_interfaz(self):

        contenedor = QWidget()

        layout_principal = QVBoxLayout()

        # TABLA
        self.tabla = TablaContactos(
            on_editar_callback=self.editar_contacto_por_id,
            on_eliminar_callback=self.eliminar_contacto_por_id
        )
        layout_principal.addWidget(self.tabla)

        # BOTONES
        layout_botones = QHBoxLayout()

        self.btn_agregar = QPushButton("Añadir")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_refrescar = QPushButton("Actualizar")

        self.btn_agregar.clicked.connect(self.abrir_formulario)
        self.btn_editar.clicked.connect(self.editar_contacto)
        self.btn_eliminar.clicked.connect(self.eliminar_contacto)

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

    def obtener_id_seleccionado(self):

        fila = self.tabla.currentRow()

        if fila == -1:
            return None

        id_item = self.tabla.item(fila, 0)

        if id_item:
            return id_item.text()

        return None
    
    def editar_contacto(self):

        id_contacto = self.obtener_id_seleccionado()

        if not id_contacto:
            return

        contactos = self.controller.obtener_contactos()

        contacto = contactos.get(id_contacto)

        if not contacto:
            return

        contacto = contacto.copy()
        contacto["id"] = id_contacto

        dialogo = ContactoDialog(
            self.controller,
            contacto
        )

        if dialogo.exec():
            self.cargar_contactos()

    def eliminar_contacto(self):

        id_contacto = self.obtener_id_seleccionado()

        if not id_contacto:
            return

        confirmacion = QMessageBox.question(
            self,
            "Eliminar contacto",
            "¿Seguro que quieres eliminar este contacto?"
        )

        if confirmacion == QMessageBox.Yes:

            self.controller.eliminar_contacto(id_contacto)

            self.cargar_contactos()

    def editar_contacto_por_id(self, id_contacto):
        contactos = self.controller.obtener_contactos()
        contacto = contactos.get(id_contacto)
        if not contacto:
         return
        contacto = contacto.copy()
        contacto["id"] = id_contacto
        dialogo = ContactoDialog(self.controller, contacto)
        if dialogo.exec():
            self.cargar_contactos()

    def eliminar_contacto_por_id(self, id_contacto):
        confirmacion = QMessageBox.question(
            self,
            "Eliminar contacto",
            "¿Seguro que quieres eliminar este contacto?"
        )
        if confirmacion == QMessageBox.Yes:
            self.controller.eliminar_contacto(id_contacto)
            self.cargar_contactos()
