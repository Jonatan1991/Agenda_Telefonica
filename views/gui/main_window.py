from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QFileDialog
)

from controllers.agenda_controller import AgendaController
from views.gui.tabla_contactos import TablaContactos
from views.gui.contacto_dialog import ContactoDialog
from views.gui.contacto_ver_dialog import ContactoVerDialog


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
            on_eliminar_callback=self.eliminar_contacto_por_id,
            on_ver_callback=self.ver_contacto_por_id
        )
        layout_principal.addWidget(self.tabla)

        # BOTONES
        layout_botones = QHBoxLayout()

        self.btn_agregar = QPushButton("Añadir")
        self.btn_editar = QPushButton("Editar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_importar = QPushButton("Importar Excel")
        self.btn_refrescar = QPushButton("Actualizar")

        self.btn_agregar.clicked.connect(self.abrir_formulario)
        self.btn_editar.clicked.connect(self.editar_contacto)
        self.btn_eliminar.clicked.connect(self.eliminar_contacto)
        self.btn_importar.clicked.connect(self.importar_excel)

        layout_botones.addWidget(self.btn_agregar)
        layout_botones.addWidget(self.btn_editar)
        layout_botones.addWidget(self.btn_eliminar)
        layout_botones.addWidget(self.btn_importar)
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

    def ver_contacto_por_id(self, id_contacto):
        contactos = self.controller.obtener_contactos()
        contacto = contactos.get(id_contacto)
        if not contacto:
            return
        contacto = contacto.copy()
        contacto["id"] = id_contacto
        dialogo = ContactoVerDialog(contacto)
        dialogo.exec()

    def importar_excel(self):
        """Importa contactos desde un archivo Excel."""
        # Seleccionar archivo
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo Excel",
            "",
            "Archivos Excel (*.xlsx);;Todos los archivos (*.*)"
        )
        
        if not ruta_archivo:
            return
        
        try:
            # Importar contactos
            resultado = self.controller.importar_contactos_excel(ruta_archivo)
            
            # Mostrar resultados
            mensaje = f"Importación completada:\n\n"
            mensaje += f"Contactos importados: {resultado['contactos_importados']}\n"
            mensaje += f"Errores de importación: {len(resultado['errores_importacion'])}\n"
            mensaje += f"Errores de agregado: {len(resultado['errores_agregado'])}\n\n"
            
            if resultado['errores_importacion']:
                mensaje += "Errores de importación:\n" + "\n".join(resultado['errores_importacion'][:5]) + "\n..."
            
            if resultado['errores_agregado']:
                mensaje += "\nErrores de agregado:\n" + "\n".join(resultado['errores_agregado'][:5]) + "\n..."
                
            QMessageBox.information(self, "Resultado de Importación", mensaje)
            
            # Recargar la tabla
            self.cargar_contactos()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error durante la importación: {str(e)}")

