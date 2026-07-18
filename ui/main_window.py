"""
Módulo responsável pela janela principal da aplicação.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
)

from algoritmos.curvas_de_bezier import Bezier
from algoritmos.bresenham import Bresenham
from algoritmos.circulo import Circulo
from ui.canvas_widget import CanvasWidget
from ui.painel_controles import PainelControles


class MainWindow(QMainWindow):
    """
    Janela principal da aplicação.
    """

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
        self.layout_principal.addWidget(self.canvas, 4)
        self.layout_principal.addWidget(self.painel, 1)

        self.layout_principal.setContentsMargins(5, 5, 5, 5)
        self.layout_principal.setSpacing(5)

        self.central_widget.setLayout(self.layout_principal)
        self.setCentralWidget(self.central_widget)

        self.canvas.centerOn(0, 0)

        self.canvas.fitInView(
            self.canvas.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )

    # -----------------------------------------------------
    # Novo: liga os botões do painel às ações do canvas/algoritmos.

    def conectar_sinais(self):
        self.painel.botao_desenhar.clicked.connect(self.executar_algoritmo)
        self.painel.botao_limpar.clicked.connect(self.canvas.limpar_canvas)

    # -----------------------------------------------------

    def executar_algoritmo(self):
        """
        Lê o algoritmo e os parâmetros escolhidos no painel e manda
        o canvas desenhar o resultado.
        """

        algoritmo = self.painel.algoritmo_selecionado()
        parametros = self.painel.obter_parametros()

        if parametros is None:
            self.statusBar().showMessage(
                "Preencha os parâmetros corretamente."
            )
            return

        if algoritmo == "Bresenham":
            x1, y1, x2, y2 = parametros
            pontos = Bresenham.calcular_reta(x1, y1, x2, y2)
            self.canvas.desenhar_linha(pontos)
            self.statusBar().showMessage(
                f"Reta de ({x1}, {y1}) a ({x2}, {y2}) desenhada "
                f"com {len(pontos)} pixels."
            )

        elif algoritmo == "Círculo":
            xc, yc, raio = parametros
            pontos = Circulo.calcular_circulo(xc, yc, raio)
            self.canvas.desenhar_linha(pontos)
            self.statusBar().showMessage(
                f"Círculo de centro ({xc}, {yc}) e raio {raio} "
                f"desenhado com {len(pontos)} pixels."
            )

        elif algoritmo == "Curva de Bézier":
            pontos_controle = parametros

            if len(pontos_controle) == 3:
                p0, p1, p2 = pontos_controle
                curva = Bezier.calcular_curva_quadratica(p0, p1, p2)
                grau_texto = "quadrática (grau 2)"
            else:
                p0, p1, p2, p3 = pontos_controle
                curva = Bezier.calcular_curva_cubica(p0, p1, p2, p3)
                grau_texto = "cúbica (grau 3)"

            pixels = Bezier.rasterizar(curva)
            self.canvas.desenhar_linha(pixels)

            self.statusBar().showMessage(
                f"Curva de Bézier {grau_texto} desenhada "
                f"com {len(pixels)} pixels."
            )

        else:
            self.statusBar().showMessage(
                f"Algoritmo '{algoritmo}' ainda não implementado."
            )

    # -----------------------------------------------------

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.canvas.fitInView(
            self.canvas.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )

        self.canvas.centerOn(0, 0)
