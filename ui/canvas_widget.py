"""
CanvasWidget

Objetivo:
Implementar o componente responsável pela renderização dos algoritmos gráficos,
fornecendo uma área de desenho baseada em QGraphicsView/QGraphicsScene.

Funcionalidades:
- Inicializar a cena gráfica;
- Configurar a visualização do canvas;
- Desenhar pixels;
- Limpar o canvas.

Retorno:
- A classe CanvasWidget deve herdar de QGraphicsView e implementar os métodos necessários para criar.
- configurar e gerenciar a cena gráfica, bem como desenhar pixels e limpar o canvas.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)


class CanvasWidget(QGraphicsView):
    """
    Widget responsável pela renderização dos algoritmos gráficos.
    """

    PIXEL_SIZE = 10
    LARGURA_CENA = 1200
    ALTURA_CENA = 800

    def __init__(self, parent=None):
        """
        Inicializa o CanvasWidget.
        """
        super().__init__(parent)

        self.criar_cena()
        self.configurar_view()

    # ------------------------------------------------------------------

    def criar_cena(self):
        """
        Cria e configura a cena gráfica.
        """

        self.scene = QGraphicsScene(self)

        self.scene.setSceneRect(
            -self.LARGURA_CENA // 2,
            -self.ALTURA_CENA // 2,
            self.LARGURA_CENA,
            self.ALTURA_CENA,
        )

        self.setScene(self.scene)

    # ------------------------------------------------------------------

    def configurar_view(self):
        """
        Configura as propriedades da área de visualização.
        """

        # Cor de fundo
        self.setBackgroundBrush(QBrush(Qt.GlobalColor.white))

        # Centraliza a cena
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Remove barras de rolagem
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Atualização da viewport
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )

        # Desabilita arrastar a cena
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        # Âncora das transformações
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

        # Melhora a renderização das formas
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

    # ------------------------------------------------------------------

    def desenhar_pixel(
        self,
        x: int,
        y: int,
        cor=Qt.GlobalColor.black,
    ):
        """
        Desenha um pixel na posição informada.

        Parameters
        ----------
        x : int
            Coordenada X.

        y : int
            Coordenada Y.

        cor : Qt.GlobalColor
            Cor utilizada para desenhar o pixel.
        """

        pixel_item = QGraphicsRectItem(
            x * self.PIXEL_SIZE,
            -y * self.PIXEL_SIZE,
            self.PIXEL_SIZE,
            self.PIXEL_SIZE,
        )

        pixel_item.setBrush(QBrush(QColor(cor)))
        pixel_item.setPen(QPen(Qt.PenStyle.NoPen))

        self.scene.addItem(pixel_item)

    # ------------------------------------------------------------------

    def limpar_canvas(self):
        """
        Remove todos os elementos desenhados na cena.
        """

        self.scene.clear()