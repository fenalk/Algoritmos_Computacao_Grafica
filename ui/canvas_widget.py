"""
Módulo responsável pela renderização dos algoritmos gráficos.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
)


class CanvasWidget(QGraphicsView):
    """
    Widget responsável pela renderização dos algoritmos gráficos.
    """

    PIXEL_SIZE = 30
    LARGURA_CENA = 690
    ALTURA_CENA = 690

    def __init__(self, parent=None):
        super().__init__(parent)

        self.criar_cena()
        self.configurar_view()
        self.desenhar_grade()
        self.desenhar_eixos()

    # ------------------------------------------------------------------

    def criar_cena(self):
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
        self.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )

        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

    # ------------------------------------------------------------------

    def desenhar_pixel(
        self,
        x: int,
        y: int,
        cor=Qt.GlobalColor.black,
    ):
        """
        Desenha um pixel na cena.
        """

        if not self.coordenada_valida(x, y):
            return

        x_tela, y_tela = self.mundo_para_tela(x, y)

        pixel_item = QGraphicsRectItem(
            x_tela,
            y_tela,
            self.PIXEL_SIZE,
            self.PIXEL_SIZE,
        )

        pixel_item.setBrush(QBrush(QColor(cor)))
        pixel_item.setPen(QPen(Qt.PenStyle.NoPen))
        pixel_item.setZValue(1)

        self.scene.addItem(pixel_item)

    # ------------------------------------------------------------------

    def desenhar_linha(
        self,
        pontos,
        cor=Qt.GlobalColor.black,
    ):
        """
        Desenha uma linha a partir da lista de pixels.
        """

        for x, y in pontos:
            self.desenhar_pixel(x, y, cor)

    # ------------------------------------------------------------------

    def limpar_canvas(self):
        self.scene.clear()
        self.desenhar_grade()
        self.desenhar_eixos()
        self.centerOn(0, 0)

    # ------------------------------------------------------------------

    def desenhar_grade(self):
        pen = QPen(QColor(220, 220, 220))
        pen.setWidth(1)

        largura = self.LARGURA_CENA // 2
        altura = self.ALTURA_CENA // 2

        passo = self.PIXEL_SIZE * 2

        for x in range(-largura, largura + 1, passo):
            linha = self.scene.addLine(x, -altura, x, altura, pen)
            linha.setZValue(-1)

        for y in range(-altura, altura + 1, passo):
            linha = self.scene.addLine(-largura, y, largura, y, pen)
            linha.setZValue(-1)

    # ------------------------------------------------------------------

    def desenhar_eixos(self):
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)

        largura = self.LARGURA_CENA // 2
        altura = self.ALTURA_CENA // 2

        eixo_x = self.scene.addLine(-largura, 0, largura, 0, pen)
        eixo_x.setZValue(0)

        eixo_y = self.scene.addLine(0, -altura, 0, altura, pen)
        eixo_y.setZValue(0)

    # ------------------------------------------------------------------

    def mundo_para_tela(self, x: int, y: int):
        return (
            x * self.PIXEL_SIZE,
            -(y + 1) * self.PIXEL_SIZE,
        )

    def tela_para_mundo(self, x_tela: int, y_tela: int):
        x = round(x_tela / self.PIXEL_SIZE)
        y = -(round(y_tela / self.PIXEL_SIZE) + 1)
        return x, y

    def coordenada_valida(self, x: int, y: int):
        limite_x = self.LARGURA_CENA // (2 * self.PIXEL_SIZE)
        limite_y = self.ALTURA_CENA // (2 * self.PIXEL_SIZE)

        return (
            -limite_x <= x < limite_x
            and
            -limite_y <= y < limite_y
        )