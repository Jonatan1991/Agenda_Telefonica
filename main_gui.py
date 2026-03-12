from PySide6.QtWidgets import QApplication
from views.gui.main_window import MainWindow
import sys

def main():

    app = QApplication(sys.argv)

    ventana = MainWindow()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()