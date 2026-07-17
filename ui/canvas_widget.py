
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

    Objetivo
    --------
    Centralizar toda a lógica relacionada à renderização gráfica da
    aplicação, incluindo a criação da cena, configuração da área de
    desenho, conversão de coordenadas e desenho dos elementos.

    Retorno
    -------
    Nenhum.
    """

    PIXEL_SIZE = 20
    LARGURA_CENA = 1200
    ALTURA_CENA = 800

    def __init__(self, parent=None):
        """
        Inicializa o CanvasWidget.

        Parâmetros
        ----------
        parent : QWidget | None, opcional
            Widget pai.

        Retorno
        -------
        None
        """
        super().__init__(parent)

        self.criar_cena()
        self.configurar_view()
        self.desenhar_grade()
        self.desenhar_eixos()

    # ------------------------------------------------------------------

    def criar_cena(self):
        """
        Cria e configura a cena gráfica.

        Objetivo
        --------
        Inicializar o objeto QGraphicsScene que armazenará todos os
        elementos desenhados na aplicação.

        Retorno
        -------
        None
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
        Configura a área de visualização da cena.

        Objetivo
        --------
        Definir as propriedades da QGraphicsView utilizadas pela
        aplicação.

        Configurações
        -------------
        - Cor de fundo;
        - Centralização da cena;
        - Remoção das barras de rolagem;
        - Atualização da viewport;
        - Desabilitação do arraste da cena;
        - Configuração da âncora das transformações.

        Retorno
        -------
        None
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

        # Desabilita movimentação da cena
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        # Centraliza transformações futuras
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

        # Mantém aspecto de pixels
        #self.setRenderHint(QPainter.RenderHint.Antialiasing, False)

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

        #------------------------------------------------------------------
        # Algoritmo de Bresenham
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
        """
        Remove todos os elementos da cena.

        Objetivo
        --------
        Limpar completamente o canvas, removendo todos os objetos
        desenhados.

        Retorno
        -------
        None
        """

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

        passo = self.PIXEL_SIZE * 2      # grade duas vezes maior

        for x in range(-largura, largura + 1, passo):
            linha = self.scene.addLine(x, -altura, x, altura, pen)
            linha.setZValue(-1)

        for y in range(-altura, altura + 1, passo):
            linha = self.scene.addLine(-largura, y, largura, y, pen)
            linha.setZValue(-1)

    # ------------------------------------------------------------------

    def desenhar_eixos(self):
        """
        Desenha os eixos X e Y.
        """

        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)

        largura = self.LARGURA_CENA // 2
        altura = self.ALTURA_CENA // 2

        eixo_x = self.scene.addLine(
            -largura,
            0,
            largura,
            0,
            pen,
        )
        eixo_x.setZValue(0)

        eixo_y = self.scene.addLine(
            0,
            -altura,
            0,
            altura,
            pen,
        )
        eixo_y.setZValue(0)


    #------------------------------------------------------------------
    # Mundo Tela -> Tela Mundo -> Validar Coordenadas Negativas
    def mundo_para_tela(self, x: int, y: int):
        
        """
        Converte coordenadas cartesianas para coordenadas da tela.
        """

        return (
            x * self.PIXEL_SIZE,
            -(y + 1) * self.PIXEL_SIZE,
        )
    
    def tela_para_mundo(self, x_tela: int, y_tela: int):
        """
        Converte coordenadas da tela para coordenadas cartesianas.
        """

        x = round(x_tela / self.PIXEL_SIZE)
        y = -(round(y_tela / self.PIXEL_SIZE) + 1)

        return x, y
    
    def coordenada_valida(self, x: int, y: int):
        """
        Verifica se uma coordenada pertence aos limites da cena.
        """

        limite_x = self.LARGURA_CENA // (2 * self.PIXEL_SIZE)
        limite_y = self.ALTURA_CENA // (2 * self.PIXEL_SIZE)

        return (
            -limite_x <= x < limite_x
            and
            -limite_y <= y < limite_y
        )
    
    #------------------------------------------------------------------