from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox
)


class Paginador(QWidget):

    def __init__(self, on_change_callback=None, page_size_options=None, default_page_size=10):
        super().__init__()

        self._on_change_callback = on_change_callback
        self._page_size_options = page_size_options or [10, 20, 50, 100]
        self._page_size = default_page_size if default_page_size in self._page_size_options else self._page_size_options[0]
        self._current_page = 1
        self._total_items = 0

        self._crear_interfaz()
        self._actualizar_estado()

    def _crear_interfaz(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.lbl_total = QLabel()
        self.btn_anterior = QPushButton("<")
        self.btn_siguiente = QPushButton(">")
        self.btn_primera = QPushButton("<<")
        self.btn_ultima = QPushButton(">>")
        self.lbl_info = QLabel()

        self.lbl_mostrar = QLabel("Mostrar:")
        self.cmb_tamano = QComboBox()
        for opcion in self._page_size_options:
            self.cmb_tamano.addItem(str(opcion), opcion)
        self.cmb_tamano.setCurrentText(str(self._page_size))

        self.btn_primera.clicked.connect(self._ir_primera)
        self.btn_anterior.clicked.connect(self._ir_anterior)
        self.btn_siguiente.clicked.connect(self._ir_siguiente)
        self.btn_ultima.clicked.connect(self._ir_ultima)
        self.cmb_tamano.currentIndexChanged.connect(self._cambiar_tamano)

        layout.addStretch(1)
        layout.addWidget(self.lbl_total)
        layout.addWidget(self.btn_primera)
        layout.addWidget(self.btn_anterior)
        layout.addWidget(self.lbl_info)
        layout.addWidget(self.btn_siguiente)
        layout.addWidget(self.btn_ultima)
        layout.addWidget(self.lbl_mostrar)
        layout.addWidget(self.cmb_tamano)
        layout.addStretch(1)

    def _total_paginas(self):
        if self._page_size <= 0:
            return 1
        total = (self._total_items + self._page_size - 1) // self._page_size
        return max(1, total)

    def _actualizar_estado(self):
        total_paginas = self._total_paginas()
        if self._current_page > total_paginas:
            self._current_page = total_paginas
        if self._current_page < 1:
            self._current_page = 1

        self.btn_anterior.setEnabled(self._current_page > 1)
        self.btn_siguiente.setEnabled(self._current_page < total_paginas)
        self.btn_primera.setEnabled(self._current_page > 1)
        self.btn_ultima.setEnabled(self._current_page < total_paginas)
        self.lbl_total.setText(f"Total: {self._total_items}")
        self.lbl_info.setText(f"Pagina {self._current_page} de {total_paginas}")

    def _emitir_cambio(self):
        if self._on_change_callback:
            self._on_change_callback(self._current_page, self._page_size)

    def _ir_primera(self):
        if self._current_page != 1:
            self._current_page = 1
            self._actualizar_estado()
            self._emitir_cambio()

    def _ir_anterior(self):
        if self._current_page > 1:
            self._current_page -= 1
            self._actualizar_estado()
            self._emitir_cambio()

    def _ir_siguiente(self):
        if self._current_page < self._total_paginas():
            self._current_page += 1
            self._actualizar_estado()
            self._emitir_cambio()

    def _ir_ultima(self):
        ultima = self._total_paginas()
        if self._current_page != ultima:
            self._current_page = ultima
            self._actualizar_estado()
            self._emitir_cambio()

    def _cambiar_tamano(self):
        nuevo = self.cmb_tamano.currentData()
        if not nuevo:
            return
        if nuevo != self._page_size:
            self._page_size = nuevo
            self._current_page = 1
            self._actualizar_estado()
            self._emitir_cambio()

    def set_total_items(self, total_items):
        self._total_items = max(0, int(total_items))
        self._actualizar_estado()

    def set_current_page(self, page):
        self._current_page = max(1, int(page))
        self._actualizar_estado()

    def get_current_page(self):
        return self._current_page

    def get_page_size(self):
        return self._page_size
