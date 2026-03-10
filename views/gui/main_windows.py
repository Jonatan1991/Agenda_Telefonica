from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)

from controllers.agenda_controller import AgendaController


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.controller = AgendaController()

        self.setWindowTitle("Agenda Telefónica")
        self.setMinimumSize(800, 500)

        self._crear_interfaz()

        self.cargar_contactos()


    def _crear_interfaz(self):

        contenedor = QWidget()
        layout = QVBoxLayout()

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(
            # ["ID", "Nombre", "Teléfono", "Email"]
            ["Nombre", "Teléfono", "Email"]
        )

        layout.addWidget(self.tabla)

        self.btn_refrescar = QPushButton("Actualizar contactos")
        self.btn_refrescar.clicked.connect(self.cargar_contactos)

        layout.addWidget(self.btn_refrescar)

        contenedor.setLayout(layout)

        self.setCentralWidget(contenedor)


    def cargar_contactos(self):

        contactos = self.controller.obtener_contactos()

        self.tabla.setRowCount(len(contactos))

        for fila, (id_contacto, datos) in enumerate(contactos.items()):

            # self.tabla.setItem(fila, 0, QTableWidgetItem(id_contacto))
            self.tabla.setItem(fila, 1, QTableWidgetItem(datos["nombre"]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(datos["telefono"]))
            self.tabla.setItem(fila, 3, QTableWidgetItem(datos["email"]))