from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


class TablaContactos(QTableWidget):

    def __init__(self):
        super().__init__()

        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Teléfono", "Email"]
        )

        self.setSortingEnabled(True)

    def cargar_datos(self, contactos):

        self.setRowCount(len(contactos))

        for fila, (id_contacto, datos) in enumerate(contactos.items()):

            self.setItem(fila, 0, QTableWidgetItem(id_contacto))
            self.setItem(fila, 1, QTableWidgetItem(datos["nombre"]))
            self.setItem(fila, 2, QTableWidgetItem(datos["telefono"]))
            self.setItem(fila, 3, QTableWidgetItem(datos["email"]))