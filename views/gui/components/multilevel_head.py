from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter


class MultiLevelHeader(QHeaderView):

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

        self.grupos = []

        self.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(40)

    def set_grupos(self, grupos):
        """
        grupos = [
            ("Datos personales", 0, 4),
            ("Dirección", 4, 4)
        ]
        """
        self.grupos = grupos
        self.viewport().update()

    def paintSection(self, painter, rect, logicalIndex):

        super().paintSection(painter, rect, logicalIndex)

        painter.save()

        for texto, inicio, cantidad in self.grupos:

            if logicalIndex == inicio:

                ancho = 0
                for i in range(inicio, inicio + cantidad):
                    ancho += self.sectionSize(i)

                r = QRect(rect.left(), rect.top() - 20, ancho, 20)

                painter.drawRect(r)
                painter.drawText(r, Qt.AlignmentFlag.AlignCenter, texto)

        painter.restore()
