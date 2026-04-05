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
from views.gui.paginador import Paginador


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controller = AgendaController()

        self.setWindowTitle("Agenda TelefÃ³nica")
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

        # PAGINADOR
        self.paginador = Paginador(on_change_callback=self._refrescar_tabla_paginada)
        layout_principal.addWidget(self.paginador)

        # BOTONES
        layout_botones = QHBoxLayout()

        self.btn_agregar = QPushButton("AÃ±adir")
        self.btn_importar = QPushButton("Importar Excel")
        self.btn_refrescar = QPushButton("Actualizar")

        self.btn_agregar.clicked.connect(self.abrir_formulario)
        self.btn_importar.clicked.connect(self.importar_excel)

        layout_botones.addWidget(self.btn_agregar)
        layout_botones.addWidget(self.btn_importar)
        layout_botones.addWidget(self.btn_refrescar)

        layout_principal.addLayout(layout_botones)

        contenedor.setLayout(layout_principal)

        self.setCentralWidget(contenedor)

        # EVENTOS
        self.btn_refrescar.clicked.connect(self.cargar_contactos)

    def cargar_contactos(self):

        contactos = self.controller.obtener_contactos()
        self._contactos = contactos
        self.paginador.set_total_items(len(contactos))
        self._refrescar_tabla_paginada()

    def abrir_formulario(self):

        dialogo = ContactoDialog(self.controller)

        if dialogo.exec():
            self.cargar_contactos()

    def _refrescar_tabla_paginada(self, *_):
        contactos = getattr(self, "_contactos", {})
        self.tabla.cargar_datos(self._paginar_contactos(contactos))

    def _paginar_contactos(self, contactos):
        pagina = self.paginador.get_current_page()
        tamano = self.paginador.get_page_size()
        items = list(contactos.items())
        inicio = (pagina - 1) * tamano
        fin = inicio + tamano
        return dict(items[inicio:fin])

    def editar_contacto_por_id(self, id_contacto):
        if not id_contacto:
            return
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
        if not id_contacto:
            return
        confirmacion = QMessageBox.question(
            self,
            "Eliminar contacto",
            "Â¿Seguro que quieres eliminar este contacto?"
        )
        if confirmacion == QMessageBox.Yes:
            self.controller.eliminar_contacto(id_contacto)
            self.cargar_contactos()

    def ver_contacto_por_id(self, id_contacto):
        if not id_contacto:
            return
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
            mensaje = f"ImportaciÃ³n completada:\n\n"
            mensaje += f"Contactos importados: {resultado['contactos_importados']}\n"
            mensaje += f"Errores de importaciÃ³n: {len(resultado['errores_importacion'])}\n"
            mensaje += f"Errores de agregado: {len(resultado['errores_agregado'])}\n\n"
            
            if resultado['errores_importacion']:
                mensaje += "Errores de importaciÃ³n:\n" + "\n".join(resultado['errores_importacion'][:5]) + "\n..."
            
            if resultado['errores_agregado']:
                mensaje += "\nErrores de agregado:\n" + "\n".join(resultado['errores_agregado'][:5]) + "\n..."
                
            QMessageBox.information(self, "Resultado de ImportaciÃ³n", mensaje)
            
            # Recargar la tabla
            self.cargar_contactos()
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error durante la importaciÃ³n: {str(e)}")




