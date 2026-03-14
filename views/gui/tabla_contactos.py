from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class TablaContactos(QTableWidget):

    def __init__(self):
        super().__init__()

        self.setColumnCount(8)
        self.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Teléfono", "Email", "Calle", "Número", "Municipio", "CP"]
        )

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        self.setSortingEnabled(True)

    def cargar_datos(self, contactos):

        self.setRowCount(len(contactos))

        for fila, (id_contacto, datos) in enumerate(contactos.items()):

            self.setItem(fila, 0, QTableWidgetItem(id_contacto))
            self.setItem(fila, 1, QTableWidgetItem(datos["nombre"]))
            self.setItem(fila, 2, QTableWidgetItem(datos["telefono"]))
            self.setItem(fila, 3, QTableWidgetItem(datos["email"]))

            direccion = datos.get("direccion", {})
            self.setItem(fila, 4, QTableWidgetItem(direccion.get("calle", "")))
            self.setItem(fila, 5, QTableWidgetItem(direccion.get("numero", "")))
            self.setItem(fila, 6, QTableWidgetItem(direccion.get("municipio", "")))
            self.setItem(fila, 7, QTableWidgetItem(direccion.get("cp", "")))
