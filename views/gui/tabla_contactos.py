from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class TablaContactos(QTableWidget):

    def __init__(self):
        super().__init__()

        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(
            ["No.", "Nombre", "Apellidos", "Teléfono", "Email", "Dirección"]
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

            self.setItem(fila, 0, QTableWidgetItem(id_contacto))
            self.setItem(fila, 1, QTableWidgetItem(datos.get("nombre", "")))
            self.setItem(fila, 2, QTableWidgetItem(apellidos))
            self.setItem(fila, 3, QTableWidgetItem(datos.get("telefono", "")))
            self.setItem(fila, 4, QTableWidgetItem(datos.get("email", "")))
            self.setItem(fila, 5, QTableWidgetItem(direccion_formato))