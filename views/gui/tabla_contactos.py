from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class TablaContactos(QTableWidget):

    def __init__(self):
        super().__init__()

        self.setColumnCount(12)
        self.setHorizontalHeaderLabels(
            ["No.", "Nombre", "Apellido 1", "Apellido 2", "Teléfono", "Email", "Calle", "Número", "Piso", "Puerta", "CP", "Provincia"]
        )

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        self.setSortingEnabled(True)

    def cargar_datos(self, contactos):

        self.setRowCount(len(contactos))

        for fila, (id_contacto, datos) in enumerate(contactos.items()):

            self.setItem(fila, 0, QTableWidgetItem(id_contacto))
            self.setItem(fila, 1, QTableWidgetItem(datos.get("nombre", "")))
            self.setItem(fila, 2, QTableWidgetItem(datos.get("apellido_1", "")))
            self.setItem(fila, 3, QTableWidgetItem(datos.get("apellido_2", "")))
            self.setItem(fila, 4, QTableWidgetItem(datos.get("telefono", "")))
            self.setItem(fila, 5, QTableWidgetItem(datos.get("email", "")))

            direccion = datos.get("direccion", {})
            self.setItem(fila, 6, QTableWidgetItem(direccion.get("calle", "")))
            self.setItem(fila, 7, QTableWidgetItem(direccion.get("numero", "")))
            self.setItem(fila, 8, QTableWidgetItem(direccion.get("piso", "")))
            self.setItem(fila, 9, QTableWidgetItem(direccion.get("puerta", "")))
            self.setItem(fila, 10, QTableWidgetItem(direccion.get("cp", "")))
            self.setItem(fila, 11, QTableWidgetItem(direccion.get("provincia", "")))
