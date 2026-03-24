from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout


class TablaContactos(QTableWidget):

    def __init__(self, on_editar_callback=None, on_eliminar_callback=None):
        super().__init__()

        self.on_editar_callback = on_editar_callback
        self.on_eliminar_callback = on_eliminar_callback

        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(
            ["No.", "Nombre", "Apellidos", "Teléfono", "Email", "Dirección", "Acciones"]
        )

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        self.setSortingEnabled(True)

    def _formatear_direccion(self, direccion):
        """Formatea dirección de forma limpia, omitiendo campos vacíos."""
        if not direccion:
            return "N/A"
        
        partes = []
        
        # Calle y número juntos
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

        self.setRowCount(len(contactos))

        for fila, (id_contacto, datos) in enumerate(contactos.items()):

            direccion = datos.get("direccion", {})
            direccion_formato = self._formatear_direccion(direccion)

            apellidos = f"{datos.get("apellido_1", "")} {datos.get("apellido_2", "")}"

            info_contactos = datos.get("info_contactos", {})

            self.setItem(fila, 0, QTableWidgetItem(id_contacto))
            self.setItem(fila, 1, QTableWidgetItem(datos.get("nombre", "")))
            self.setItem(fila, 2, QTableWidgetItem(apellidos))
            self.setItem(fila, 3, QTableWidgetItem(info_contactos.get("telefono_1", "")))
            self.setItem(fila, 4, QTableWidgetItem(info_contactos.get("email", "")))
            self.setItem(fila, 5, QTableWidgetItem(direccion_formato))
            
            widget_acciones = QWidget()
            layout_acciones = QHBoxLayout(widget_acciones)
            layout_acciones.setContentsMargins(0, 0, 0, 0)
            layout_acciones.setSpacing(5)

            btn_editar = QPushButton("Editar")
            btn_eliminar = QPushButton("Eliminar")

            btn_editar.clicked.connect(lambda checked, id=id_contacto: self.on_editar_callback(id) if self.on_editar_callback else None)
            btn_eliminar.clicked.connect(lambda checked, id=id_contacto: self.on_eliminar_callback(id) if self.on_eliminar_callback else None)

            layout_acciones.addWidget(btn_editar)
            layout_acciones.addWidget(btn_eliminar)

            self.setCellWidget(fila, 6, widget_acciones)