"""
Objetivo:

Implementar o componente responsável pela renderização dos algoritmos gráficos, permitindo criar a área de desenho, configurar a visualização, desenhar pixels e limpar o canvas.

Especificidades:

Inicializa a cena gráfica, configura o QGraphicsView, desenha pixels nas coordenadas informadas e remove todos os elementos da cena quando necessário.

Retorno:

Os métodos não retornam valores (None), apenas modificam o estado da cena gráfica e sua exibição.

"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)


class CanvasWidget(QGraphicsView):
    """
    Área responsável pela renderização dos algoritmos gráficos.
    """

    PIXEL_SIZE = 10

    def __init__(self, parent=None):
        super().__init__(parent)

        self.criar_cena()

        self.configurar_view()

    # ---------------------------------------------------------

    def criar_cena(self):
        """Cria a cena gráfica."""

        self.scene = QGraphicsScene(self)

        self.setScene(self.scene)

    # ---------------------------------------------------------

    def configurar_view(self):
        """Configura a área de visualização."""

        self.setSceneRect(-600, -400, 1200, 800)

        self.setRenderHint(self.renderHints())

        self.setBackgroundBrush(QBrush(Qt.white))

    # ---------------------------------------------------------

    def desenhar_pixel(self, x, y, cor=Qt.black):
        """
        Desenha um pixel na cena.
        """

        pixel = QGraphicsRectItem(
            x * self.PIXEL_SIZE,
            -y * self.PIXEL_SIZE,
            self.PIXEL_SIZE,
            self.PIXEL_SIZE,
        )

        pixel.setBrush(QBrush(QColor(cor)))
        pixel.setPen(QPen(Qt.NoPen))

        self.scene.addItem(pixel)

    # ---------------------------------------------------------

    def limpar_canvas(self):
        """
        Remove todos os desenhos.
        """

        self.scene.clear()