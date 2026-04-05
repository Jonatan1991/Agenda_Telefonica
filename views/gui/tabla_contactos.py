from PySide6.QtCore import QPoint
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QStyle
)


class TablaContactos(QTableWidget):

    def __init__(self, on_editar_callback=None, on_eliminar_callback=None, on_ver_callback=None):
        super().__init__()

        self.on_editar_callback = on_editar_callback
        self.on_eliminar_callback = on_eliminar_callback
        self.on_ver_callback = on_ver_callback

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Apellidos", "TelÃ©fono", "Email", "DirecciÃ³n", "Acciones"]
        )

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        self.setSortingEnabled(True)
        self.setColumnHidden(0, True)

    def _id_desde_boton(self, boton):
        pos = boton.parent().mapTo(self.viewport(), QPoint(0, 0))
        row = self.indexAt(pos).row()
        if row < 0:
            return None
        id_item = self.item(row, 0)
        if id_item:
            return id_item.text()
        return None

    def _formatear_direccion(self, direccion):
        """Formatea direcciÃ³n de forma limpia, omitiendo campos vacÃ­os."""
        if not direccion:
            return "N/A"
        
        partes = []
        
        # Calle y nÃºmero juntos
        if direccion.get("calle"):
            calle_num = f"{direccion['calle']} {direccion.get('numero', '')}".strip()
            partes.append(calle_num )
        
        # Piso
        if direccion.get("piso"):
            partes.append(f"{direccion['piso']}")
        
        # Puerta con etiqueta corta
        if direccion.get("puerta"):
            partes.append(f"Pta. {direccion['puerta']}")
        
        # Escalera con etiqueta corta
        if direccion.get("escalera"):
            partes.append(f"Esc. {direccion['escalera']}")
        
        # CP
        if direccion.get("cp"):
            partes.append(f"{direccion['cp']}")
        
        # Provincia/Municipio
        if direccion.get("provincia"):
            partes.append(f"{direccion['provincia']}")
        
        return ", ".join(partes) if partes else "N/A"

    def cargar_datos(self, contactos):

        sorting_activo = self.isSortingEnabled()
        if sorting_activo:
            self.setSortingEnabled(False)

        self.setRowCount(len(contactos))

        for fila, (id_contacto, datos) in enumerate(contactos.items()):

            direccion = datos.get("direccion", {})
            direccion_formato = self._formatear_direccion(direccion)

            apellidos = f"{datos.get("apellido_1", "")} {datos.get("apellido_2", "")}"

            info_contactos = datos.get("info_contactos", {})

           
            self.setItem(fila, 0, QTableWidgetItem(str(id_contacto)))
            self.setItem(fila, 1, QTableWidgetItem(datos.get("nombre", "")))
            self.setItem(fila, 2, QTableWidgetItem(apellidos))
            self.setItem(fila, 3, QTableWidgetItem(info_contactos.get("telefono_1", "")))
            self.setItem(fila, 4, QTableWidgetItem(info_contactos.get("email", "")))
            self.setItem(fila, 5, QTableWidgetItem(direccion_formato))
            
            widget_acciones = QWidget()
            layout_acciones = QHBoxLayout(widget_acciones)
            layout_acciones.setContentsMargins(0, 0, 0, 0)
            layout_acciones.setSpacing(2)

            btn_ver = QPushButton("")
            btn_editar = QPushButton("")
            btn_eliminar = QPushButton("")

            btn_ver.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))
            btn_editar.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
            btn_eliminar.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))

            btn_ver.setToolTip("Ver detalles")
            btn_editar.setToolTip("Editar contacto")
            btn_eliminar.setToolTip("Eliminar contacto")

            btn_ver.clicked.connect(
                lambda checked, b=btn_ver: self.on_ver_callback(self._id_desde_boton(b)) if self.on_ver_callback else None
            )
            btn_editar.clicked.connect(
                lambda checked, b=btn_editar: self.on_editar_callback(self._id_desde_boton(b)) if self.on_editar_callback else None
            )
            btn_eliminar.clicked.connect(
                lambda checked, b=btn_eliminar: self.on_eliminar_callback(self._id_desde_boton(b)) if self.on_eliminar_callback else None
            )

            layout_acciones.addWidget(btn_ver)
            layout_acciones.addWidget(btn_editar)
            layout_acciones.addWidget(btn_eliminar)

            self.setCellWidget(fila, 6, widget_acciones)

        if sorting_activo:
            self.setSortingEnabled(True)




