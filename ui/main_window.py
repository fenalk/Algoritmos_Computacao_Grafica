"""
Módulo responsável pela janela principal da aplicação.

Objetivo:
    Criar a estrutura principal da interface gráfica,
    integrando canvas, painel de controles e algoritmos.

Especificidades:
    - Configura a janela principal.
    - Cria menus.
    - Cria barra de status.
    - Integra CanvasWidget.
    - Integra PainelControles.

Retorno:
    A classe MainWindow gerencia a aplicação gráfica.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QWidget,
)

from ui.canvas_widget import CanvasWidget
from ui.painel_controles import PainelControles
from algoritmos.bresenham import Bresenham


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.configurar_janela()

        self.criar_componentes()

        self.criar_layout()

        self.conectar_sinais()


    # -----------------------------------------------------

    def configurar_janela(self):

        self.setWindowTitle("Computação Gráfica")

        self.resize(1200, 800)

    # -----------------------------------------------------

    def criar_componentes(self):
        """
        Cria os componentes da interface.
        """

        self.menuBar().addMenu("Arquivo")
        self.menuBar().addMenu("Editar")
        self.menuBar().addMenu("Visualizar")
        self.menuBar().addMenu("Ajuda")

        self.statusBar().showMessage("Aplicação iniciada.")

        self.central_widget = QWidget()

        self.layout_principal = QHBoxLayout()

        self.canvas = CanvasWidget()

        self.painel = PainelControles()

    # -----------------------------------------------------

    def criar_layout(self):
        """
        Organiza os componentes da interface.
        """

        self.layout_principal.addWidget(self.canvas, 4)

        self.layout_principal.addWidget(self.painel, 1)

        self.central_widget.setLayout(self.layout_principal)

        self.setCentralWidget(self.central_widget)

    
    # -----------------------------------------------------
    def conectar_sinais(self):

        self.painel.botao_desenhar.clicked.connect(
            self.desenhar_bresenham
        )

        self.painel.botao_limpar.clicked.connect(
            self.canvas.limpar_canvas
        )

   # -----------------------------------------------------
   # ALgoritmo de Bresenham

    def desenhar_bresenham(self):

        try:

            x1 = int(self.painel.campo_x1.text())
            y1 = int(self.painel.campo_y1.text())

            x2 = int(self.painel.campo_x2.text())
            y2 = int(self.painel.campo_y2.text())


            pontos = Bresenham.calcular_reta(
                x1,
                y1,
                x2,
                y2
            )


            self.canvas.limpar_canvas()

            self.canvas.desenhar_linha(pontos)


            self.statusBar().showMessage(
                "Linha Bresenham desenhada."
            )


        except ValueError:

            self.statusBar().showMessage(
                "Informe valores válidos."
            )