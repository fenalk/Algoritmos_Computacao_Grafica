"""
CanvasWidget

Objetivo:
    Implementar o componente responsável pela renderização dos algoritmos
    gráficos, fornecendo uma área de desenho baseada em QGraphicsView e
    QGraphicsScene.

Especificidades:
    - Inicializar e configurar a cena gráfica;
    - Configurar a área de visualização (canvas);
    - Realizar a conversão entre coordenadas do sistema cartesiano
      (mundo) e coordenadas da tela;
    - Desenhar pixels na cena;
    - Limpar o conteúdo do canvas.

Retorno:
    A classe CanvasWidget herda de QGraphicsView e disponibiliza os
    métodos necessários para gerenciar a renderização gráfica da aplicação.
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

    Objetivo
    --------
    Centralizar toda a lógica relacionada à renderização gráfica da
    aplicação, incluindo a criação da cena, configuração da área de
    desenho, conversão de coordenadas e desenho dos elementos.

    Retorno
    -------
    Nenhum.
    """

    PIXEL_SIZE = 10
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

        self.centerOn(0,0)

    # ------------------------------------------------------------------

    def mundo_para_tela(self, x: int, y: int) -> tuple[int, int]:
        """
        Converte coordenadas do sistema cartesiano para a tela.

        Objetivo
        --------
        Converter coordenadas do sistema de coordenadas do mundo para
        coordenadas utilizadas pela QGraphicsScene.

        Parâmetros
        ----------
        x : int
            Coordenada X no sistema cartesiano.

        y : int
            Coordenada Y no sistema cartesiano.

        Observação
        ----------
        O eixo Y da tela possui orientação inversa ao eixo Y do sistema
        cartesiano. Por esse motivo o valor é invertido durante a
        conversão.

        Retorno
        -------
        tuple[int, int]
            Coordenadas convertidas para a tela.
        """

        x_tela = x * self.PIXEL_SIZE
        y_tela = -y * self.PIXEL_SIZE

        return x_tela, y_tela

    # ------------------------------------------------------------------

    def tela_para_mundo(self, x: int, y: int) -> tuple[int, int]:
        """
        Converte coordenadas da tela para o sistema cartesiano.

        Objetivo
        --------
        Converter coordenadas provenientes da QGraphicsView para o
        sistema de coordenadas do mundo.

        Parâmetros
        ----------
        x : int
            Coordenada X da tela.

        y : int
            Coordenada Y da tela.

        Observação
        ----------
        Utiliza a função round() para garantir que o retorno seja um
        ponto pertencente à malha cartesiana.

        Retorno
        -------
        tuple[int, int]
            Coordenadas convertidas para o sistema cartesiano.
        """

        x_mundo = round(x / self.PIXEL_SIZE)
        y_mundo = round(-y / self.PIXEL_SIZE)

        return x_mundo, y_mundo
    


    # ------------------------------------------------------------------

    def desenhar_pixel(
        self,
        x: int,
        y: int,
        cor=Qt.GlobalColor.black,
    ):
        """
        Desenha um pixel na cena.

        Objetivo
        --------
        Renderizar um pixel na posição informada utilizando um
        QGraphicsRectItem.

        Parâmetros
        ----------
        x : int
            Coordenada X no sistema cartesiano.

        y : int
            Coordenada Y no sistema cartesiano.

        cor : Qt.GlobalColor, opcional
            Cor utilizada para desenhar o pixel.

        Retorno
        -------
        None
        """

        x_tela, y_tela = self.mundo_para_tela(x, y)

        pixel_item = QGraphicsRectItem(
            x_tela,
            y_tela,
            self.PIXEL_SIZE,
            self.PIXEL_SIZE,
        )

        pixel_item.setBrush(QBrush(QColor(cor)))
        pixel_item.setPen(QPen(Qt.PenStyle.NoPen))

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
        self.centerOn(0, 0)

        ##############




    # ------------------------------------------------------------------
    # Métodos previstos para as próximas etapas do projeto:
    #
    # - desenhar_grade()
    # - desenhar_eixos()
    # - mousePressEvent()
    # - wheelEvent()
    #
    # Esses métodos serão implementados nas próximas Issues.
    # ------------------------------------------------------------------