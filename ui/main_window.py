"""
Módulo responsável pela janela principal da aplicação.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
)

from algoritmos.bresenham import Bresenham
from algoritmos.circulo import Circulo
from algoritmos.curvas_de_bezier import Bezier
from algoritmos.elipse import Elipse
from algoritmos.polilinha import Polilinha
from algoritmos.preenchimento import Preenchimento
from algoritmos.recorte_linhas import RecorteLinhas
from algoritmos.recorte_poligono import RecortePoligonos
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

    def conectar_sinais(self):
        self.painel.botao_desenhar.clicked.connect(
            self.executar_algoritmo
        )
        self.painel.botao_limpar.clicked.connect(
            self.canvas.limpar_canvas
        )

    # -----------------------------------------------------

    def executar_algoritmo(self):
        """
        Lê o algoritmo selecionado e executa o desenho.
        """

        algoritmo = self.painel.algoritmo_selecionado()
        parametros = self.painel.obter_parametros()

        if parametros is None:
            if algoritmo == "Polilinha":
                self.statusBar().showMessage(
                    "Adicione pelo menos 4 pontos para desenhar a polilinha."
                )
            elif algoritmo == "Preenchimento":
                self.statusBar().showMessage(
                    "Informe um polígono válido e, no modo recursivo, um ponto semente."
                )
            elif algoritmo == "Recorte de Linhas":
                self.statusBar().showMessage(
                    "Informe a linha e uma janela de recorte válida (Xmin < Xmax e Ymin < Ymax)."
                )
            elif algoritmo == "Recorte de Polígonos":
                self.statusBar().showMessage(
                    "Informe pelo menos 3 vértices e uma janela de recorte válida "
                    "(Xmin < Xmax e Ymin < Ymax)."
                )
            else:
                self.statusBar().showMessage(
                    "Preencha os parâmetros corretamente."
                )
            return

        # -------------------------------------------------
        # Bresenham
        # -------------------------------------------------

        if algoritmo == "Bresenham":

            x1, y1, x2, y2 = parametros

            pontos = Bresenham.calcular_reta(
                x1,
                y1,
                x2,
                y2,
            )

            self.canvas.desenhar_linha(pontos)

            self.statusBar().showMessage(
                f"Reta de ({x1}, {y1}) a ({x2}, {y2}) "
                f"desenhada com {len(pontos)} pixels."
            )

        # -------------------------------------------------
        # Círculo
        # -------------------------------------------------

        elif algoritmo == "Círculo":

            xc, yc, raio = parametros

            pontos = Circulo.calcular_circulo(
                xc,
                yc,
                raio,
            )

            self.canvas.desenhar_linha(pontos)

            self.statusBar().showMessage(
                f"Círculo de centro ({xc}, {yc}) "
                f"e raio {raio} desenhado "
                f"com {len(pontos)} pixels."
            )

        # -------------------------------------------------
        # Elipse
        # -------------------------------------------------

        elif algoritmo == "Elipse":

            xc, yc, rx, ry = parametros

            pontos = Elipse.calcular_elipse(
                xc,
                yc,
                rx,
                ry,
            )

            self.canvas.desenhar_linha(pontos)

            self.statusBar().showMessage(
                f"Elipse de centro ({xc}, {yc}), "
                f"rx={rx}, ry={ry} desenhada "
                f"com {len(pontos)} pixels."
            )

        # -------------------------------------------------
        # Bézier
        # -------------------------------------------------

        elif algoritmo == "Curva de Bézier":

            pontos_controle = parametros

            if len(pontos_controle) == 3:

                p0, p1, p2 = pontos_controle

                curva = Bezier.calcular_curva_quadratica(
                    p0,
                    p1,
                    p2,
                )

                descricao = "quadrática"

            else:

                p0, p1, p2, p3 = pontos_controle

                curva = Bezier.calcular_curva_cubica(
                    p0,
                    p1,
                    p2,
                    p3,
                )

                descricao = "cúbica"

            pixels = Bezier.rasterizar(curva)

            self.canvas.desenhar_linha(pixels)

            self.statusBar().showMessage(
                f"Curva de Bézier {descricao} "
                f"desenhada com {len(pixels)} pixels."
            )

        # -------------------------------------------------
        # Polilinha
        # -------------------------------------------------

        elif algoritmo == "Polilinha":

            pontos = parametros

            fechada = self.painel.polilinha_fechada()

            pixels = Polilinha.calcular_polilinha(
                pontos,
                fechada=fechada,
            )

            self.canvas.desenhar_linha(pixels)

            sufixo = " fechada." if fechada else " aberta."

            self.statusBar().showMessage(
                f"Polilinha desenhada com "
                f"{len(pixels)} pixels ({len(pontos)} vértices){sufixo}"
            )

        # -------------------------------------------------
        # Preenchimento
        # -------------------------------------------------

        elif algoritmo == "Preenchimento":

            pontos = parametros["pontos"]
            tipo = parametros["tipo"]
            semente = parametros["semente"]

            if tipo == "recursivo":

                resultado = Preenchimento.preencher_recursivo(
                    pontos,
                    semente,
                )

                if resultado is None:

                    self.statusBar().showMessage(
                        "Não foi possível realizar o preenchimento recursivo."
                    )

                    return

            else:

                resultado = Preenchimento.preencher_varredura(
                    pontos
                )

                if resultado is None:

                    self.statusBar().showMessage(
                        "Polígono inválido."
                    )

                    return

            contorno, preenchidos = resultado

            # Desenha o contorno em preto
            self.canvas.desenhar_linha(contorno)

            # Desenha o preenchimento em laranja
            self.canvas.desenhar_linha(
                preenchidos,
                cor="darkorange",
            )

            self.statusBar().showMessage(
                f"Preenchimento concluído. "
                f"{len(preenchidos)} pixels preenchidos."
            )

        # -------------------------------------------------
        # Recorte de Linhas (Cohen-Sutherland)
        # -------------------------------------------------

        elif algoritmo == "Recorte de Linhas":

            x1, y1, x2, y2 = parametros["linha"]
            xmin, ymin, xmax, ymax = parametros["janela"]

            # Desenha a janela de recorte como um contorno fino, sempre
            # visível por cima de qualquer conteúdo (mesmo que coincida
            # com o resultado do recorte)
            self.canvas.desenhar_retangulo(xmin, ymin, xmax, ymax, cor="blue")

            # Desenha a linha original inteira em cinza, como referência
            pontos_original = Bresenham.calcular_reta(x1, y1, x2, y2)
            self.canvas.desenhar_linha(pontos_original, cor="lightgray")

            resultado = RecorteLinhas.recortar(
                x1, y1, x2, y2, xmin, ymin, xmax, ymax
            )

            if resultado is None:
                self.statusBar().showMessage(
                    "A linha está totalmente fora da janela de recorte "
                    "(nada foi recortado)."
                )
            else:
                xr1, yr1, xr2, yr2 = resultado

                pixels_recortados = Bresenham.calcular_reta(
                    xr1, yr1, xr2, yr2
                )

                # Desenha a parte recortada (visível) em vermelho, por
                # cima da linha original em cinza
                self.canvas.desenhar_linha(pixels_recortados, cor="red")

                self.statusBar().showMessage(
                    f"Linha recortada de ({xr1}, {yr1}) a ({xr2}, {yr2}) "
                    f"com {len(pixels_recortados)} pixels visíveis "
                    f"dentro da janela."
                )

        # -------------------------------------------------
        # Recorte de Polígonos (Sutherland-Hodgman)
        # -------------------------------------------------

        elif algoritmo == "Recorte de Polígonos":

            vertices = parametros["pontos"]
            xmin, ymin, xmax, ymax = parametros["janela"]

            # Desenha a janela de recorte como um contorno fino, sempre
            # visível por cima de qualquer conteúdo (mesmo que coincida
            # com o resultado do recorte)
            self.canvas.desenhar_retangulo(xmin, ymin, xmax, ymax, cor="blue")

            # Desenha o polígono original inteiro em cinza, como referência
            pixels_original = Polilinha.calcular_polilinha(
                vertices, fechada=True
            )
            self.canvas.desenhar_linha(pixels_original, cor="lightgray")

            resultado = RecortePoligonos.recortar(
                vertices, xmin, ymin, xmax, ymax
            )

            if resultado is None:
                self.statusBar().showMessage(
                    "O polígono está totalmente fora da janela de recorte "
                    "(nada foi recortado)."
                )
            else:
                pixels_recortado = Polilinha.calcular_polilinha(
                    resultado, fechada=True
                )

                # Desenha o polígono recortado (visível) em vermelho, por
                # cima do polígono original em cinza
                self.canvas.desenhar_linha(pixels_recortado, cor="red")

                self.statusBar().showMessage(
                    f"Polígono recortado com {len(resultado)} vértices "
                    f"e {len(pixels_recortado)} pixels visíveis dentro "
                    f"da janela."
                )

        # -------------------------------------------------

        else:

            self.statusBar().showMessage(
                f"Algoritmo '{algoritmo}' ainda não implementado."
            )

        # Força a atualização da view
        self.canvas.viewport().update()

    # -----------------------------------------------------

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.canvas.fitInView(
            self.canvas.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )

        self.canvas.centerOn(0, 0)