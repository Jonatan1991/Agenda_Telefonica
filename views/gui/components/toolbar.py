from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar, QWidgetAction, QMenu, QToolButton


def crear_toolbar(parent):
    toolbar = QToolBar("Acciones")
    toolbar.setMovable(False)
    parent.addToolBar(toolbar)

    accion_agregar = QWidgetAction(parent)
    accion_importar = QWidgetAction(parent)
    accion_refrescar = QWidgetAction(parent)

    accion_agregar.triggered.connect(parent.abrir_formulario)
    accion_importar.triggered.connect(parent.importar_excel)
    accion_refrescar.triggered.connect(parent.cargar_contactos)

    accion_salir = QAction("Salir", parent)
    accion_salir.triggered.connect(parent.close)

    # toolbar.addAction(accion_agregar)
    # toolbar.addAction(accion_importar)
    # toolbar.addAction(accion_refrescar)

    menu_acciones = QMenu("Archivo", parent)
    menu_acciones.addAction(accion_agregar)
    menu_acciones.addAction(accion_importar)
    menu_acciones.addAction(accion_refrescar)
    menu_acciones.addSeparator()
    menu_acciones.addAction(accion_salir)

    # toolbar.addSeparator()
    # toolbar.addAction(accion_salir)

    accion_agregar.setText("Añadir")
    accion_importar.setText("Importar Excel")
    accion_refrescar.setText("Actualizar")

    boton_menu = QToolButton()
    boton_menu.setText("Archivo")
    boton_menu.setMenu(menu_acciones)
    boton_menu.setPopupMode(QToolButton.InstantPopup)
    toolbar.addWidget(boton_menu)

    

    

    return toolbar
