"""
Módulo responsável pelo painel lateral de controles da aplicação.
"""

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.canvas_widget import CanvasWidget


class PainelControles(QWidget):
    """
    Painel lateral responsável pela interação do usuário.
    """

    # Limite de coordenadas válidas da área de desenho (canvas), usado
    # para validar que a janela de recorte é sempre MENOR que a área
    # de desenho, nunca igual ou maior.
    LIMITE_CANVAS_X = CanvasWidget.LARGURA_CENA // (2 * CanvasWidget.PIXEL_SIZE)
    LIMITE_CANVAS_Y = CanvasWidget.ALTURA_CENA // (2 * CanvasWidget.PIXEL_SIZE)

    ALGORITMOS = [
        "Bresenham",
        "Círculo",
        "Elipse",
        "Curva de Bézier",
        "Polilinha",
        "Preenchimento",
        "Recorte de Linhas",
        "Recorte de Polígonos",
        "Transformações Geométricas",
        "Projeções",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.criar_componentes()
        self.criar_layout()
        self.conectar_sinais()

        self.atualizar_parametros(self.combo_algoritmos.currentText())

    # ------------------------------------------------------------------

    def criar_componentes(self):
        self.setMinimumWidth(300)

        self.grupo_algoritmo = QGroupBox("Algoritmo")
        self.grupo_parametros = QGroupBox("Parâmetros")

        self.combo_algoritmos = QComboBox()
        self.combo_algoritmos.addItems(self.ALGORITMOS)

        self.combo_grau_bezier = QComboBox()
        self.combo_grau_bezier.addItems(
            ["Quadrática (grau 2)", "Cúbica (grau 3)"]
        )

        self.campo_x1 = QLineEdit()
        self.campo_x1.setPlaceholderText("Digite X1")

        self.campo_y1 = QLineEdit()
        self.campo_y1.setPlaceholderText("Digite Y1")

        self.campo_ctrl1_x = QLineEdit()
        self.campo_ctrl1_x.setPlaceholderText("Controle 1 X")

        self.campo_ctrl1_y = QLineEdit()
        self.campo_ctrl1_y.setPlaceholderText("Controle 1 Y")

        self.campo_ctrl2_x = QLineEdit()
        self.campo_ctrl2_x.setPlaceholderText("Controle 2 X")

        self.campo_ctrl2_y = QLineEdit()
        self.campo_ctrl2_y.setPlaceholderText("Controle 2 Y")

        self.campo_x2 = QLineEdit()
        self.campo_x2.setPlaceholderText("Digite X2")

        self.campo_y2 = QLineEdit()
        self.campo_y2.setPlaceholderText("Digite Y2")

        self.botao_desenhar = QPushButton("Desenhar")
        self.botao_limpar = QPushButton("Limpar")

        self.botao_desenhar.setMinimumHeight(35)
        self.botao_limpar.setMinimumHeight(35)

        # --- Polilinha: entrada de N > 3 pontos quaisquer ---

        self.grupo_pontos_polilinha = QGroupBox("Pontos da Polilinha (N > 3)")

        self.campo_ponto_x = QLineEdit()
        self.campo_ponto_x.setPlaceholderText("X")

        self.campo_ponto_y = QLineEdit()
        self.campo_ponto_y.setPlaceholderText("Y")

        self.botao_adicionar_ponto = QPushButton("Adicionar")
        self.botao_remover_ponto = QPushButton("Remover selecionado")

        self.lista_pontos_polilinha = QListWidget()
        self.lista_pontos_polilinha.setMinimumHeight(120)

        self.checkbox_fechar_poligono = QCheckBox(
            "Fechar (ligar último ao primeiro)"
        )

        # --- Preenchimento: tipo (recursivo/varredura) + semente ---

        self.combo_tipo_preenchimento = QComboBox()
        self.combo_tipo_preenchimento.addItems(
            ["Recursivo (flood fill)", "Varredura (scanline)"]
        )

        # --- Recorte de Linhas: janela de recorte (xmin, ymin, xmax, ymax) ---
        # A janela precisa ser sempre menor que a área de desenho, por isso
        # os placeholders já indicam o intervalo válido de coordenadas.

        limite_x = self.LIMITE_CANVAS_X - 1
        limite_y = self.LIMITE_CANVAS_Y - 1

        self.campo_clip_xmin = QLineEdit()
        self.campo_clip_xmin.setPlaceholderText(f"Xmin (> -{limite_x})")

        self.campo_clip_ymin = QLineEdit()
        self.campo_clip_ymin.setPlaceholderText(f"Ymin (> -{limite_y})")

        self.campo_clip_xmax = QLineEdit()
        self.campo_clip_xmax.setPlaceholderText(f"Xmax (< {limite_x})")

        self.campo_clip_ymax = QLineEdit()
        self.campo_clip_ymax.setPlaceholderText(f"Ymax (< {limite_y})")

    # ------------------------------------------------------------------

    def criar_layout(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(10, 10, 10, 10)
        layout_principal.setSpacing(10)

        layout_algoritmo = QVBoxLayout()
        layout_algoritmo.addWidget(self.combo_algoritmos)
        self.grupo_algoritmo.setLayout(layout_algoritmo)

        self.layout_parametros = QFormLayout()
        self.layout_parametros.addRow("Grau:", self.combo_grau_bezier)
        self.layout_parametros.addRow("Tipo:", self.combo_tipo_preenchimento)
        self.layout_parametros.addRow("X1:", self.campo_x1)
        self.layout_parametros.addRow("Y1:", self.campo_y1)
        self.layout_parametros.addRow("Ctrl1 X:", self.campo_ctrl1_x)
        self.layout_parametros.addRow("Ctrl1 Y:", self.campo_ctrl1_y)
        self.layout_parametros.addRow("Ctrl2 X:", self.campo_ctrl2_x)
        self.layout_parametros.addRow("Ctrl2 Y:", self.campo_ctrl2_y)
        self.layout_parametros.addRow("X2:", self.campo_x2)
        self.layout_parametros.addRow("Y2:", self.campo_y2)
        self.layout_parametros.addRow("Xmin:", self.campo_clip_xmin)
        self.layout_parametros.addRow("Ymin:", self.campo_clip_ymin)
        self.layout_parametros.addRow("Xmax:", self.campo_clip_xmax)
        self.layout_parametros.addRow("Ymax:", self.campo_clip_ymax)
        self.grupo_parametros.setLayout(self.layout_parametros)

        # --- Grupo de pontos da Polilinha ---

        layout_pontos = QVBoxLayout()

        layout_campo_ponto = QHBoxLayout()
        layout_campo_ponto.addWidget(self.campo_ponto_x)
        layout_campo_ponto.addWidget(self.campo_ponto_y)
        layout_campo_ponto.addWidget(self.botao_adicionar_ponto)

        layout_pontos.addLayout(layout_campo_ponto)
        layout_pontos.addWidget(self.lista_pontos_polilinha)
        layout_pontos.addWidget(self.botao_remover_ponto)
        layout_pontos.addWidget(self.checkbox_fechar_poligono)

        self.grupo_pontos_polilinha.setLayout(layout_pontos)

        # --- Botões ---

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.botao_desenhar)
        layout_botoes.addWidget(self.botao_limpar)

        # --- Montagem final ---

        layout_principal.addWidget(self.grupo_algoritmo)
        layout_principal.addWidget(self.grupo_parametros)
        layout_principal.addWidget(self.grupo_pontos_polilinha)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_botoes)

        self.setLayout(layout_principal)

    # ------------------------------------------------------------------

    def conectar_sinais(self):
        self.combo_algoritmos.currentTextChanged.connect(
            self.atualizar_parametros
        )
        self.combo_grau_bezier.currentTextChanged.connect(
            lambda _: self.atualizar_parametros(self.algoritmo_selecionado())
        )
        self.botao_adicionar_ponto.clicked.connect(
            self.adicionar_ponto_polilinha
        )
        self.botao_remover_ponto.clicked.connect(
            self.remover_ponto_polilinha
        )
        self.combo_tipo_preenchimento.currentTextChanged.connect(
            lambda _: self.atualizar_parametros(self.algoritmo_selecionado())
        )

    # ------------------------------------------------------------------

    def atualizar_parametros(self, algoritmo):
        eh_pontos_dinamicos = algoritmo in (
            "Polilinha",
            "Preenchimento",
            "Recorte de Polígonos",
        )

        self.grupo_pontos_polilinha.setVisible(eh_pontos_dinamicos)

        # Por padrão, oculta tudo que é específico de outros modos
        self.layout_parametros.setRowVisible(self.combo_grau_bezier, False)
        self.layout_parametros.setRowVisible(self.combo_tipo_preenchimento, False)
        self.layout_parametros.setRowVisible(self.campo_ctrl1_x, False)
        self.layout_parametros.setRowVisible(self.campo_ctrl1_y, False)
        self.layout_parametros.setRowVisible(self.campo_ctrl2_x, False)
        self.layout_parametros.setRowVisible(self.campo_ctrl2_y, False)
        self.layout_parametros.setRowVisible(self.campo_clip_xmin, False)
        self.layout_parametros.setRowVisible(self.campo_clip_ymin, False)
        self.layout_parametros.setRowVisible(self.campo_clip_xmax, False)
        self.layout_parametros.setRowVisible(self.campo_clip_ymax, False)

        # Visibilidade padrão dos campos numéricos comuns
        self.layout_parametros.setRowVisible(self.campo_x1, True)
        self.layout_parametros.setRowVisible(self.campo_y1, True)
        self.layout_parametros.setRowVisible(self.campo_x2, True)
        self.layout_parametros.setRowVisible(self.campo_y2, True)

        self.grupo_parametros.setVisible(not eh_pontos_dinamicos)

        if algoritmo == "Bresenham":
            self.campo_x1.setPlaceholderText("Digite X1")
            self.campo_y1.setPlaceholderText("Digite Y1")
            self.campo_x2.setPlaceholderText("Digite X2")
            self.campo_y2.setPlaceholderText("Digite Y2")

        elif algoritmo == "Círculo":
            self.campo_x1.setPlaceholderText("Centro X")
            self.campo_y1.setPlaceholderText("Centro Y")
            self.campo_x2.setPlaceholderText("Raio")
            self.layout_parametros.setRowVisible(self.campo_y2, False)

        elif algoritmo == "Elipse":
            self.campo_x1.setPlaceholderText("Centro X")
            self.campo_y1.setPlaceholderText("Centro Y")
            self.campo_x2.setPlaceholderText("Rx (semieixo horizontal)")
            self.campo_y2.setPlaceholderText("Ry (semieixo vertical)")

        elif algoritmo == "Curva de Bézier":
            self.campo_x1.setPlaceholderText("Inicial X")
            self.campo_y1.setPlaceholderText("Inicial Y")
            self.campo_x2.setPlaceholderText("Final X")
            self.campo_y2.setPlaceholderText("Final Y")

            self.layout_parametros.setRowVisible(self.combo_grau_bezier, True)
            self.layout_parametros.setRowVisible(self.campo_ctrl1_x, True)
            self.layout_parametros.setRowVisible(self.campo_ctrl1_y, True)

            grau_cubico = self.combo_grau_bezier.currentText().startswith("Cúbica")
            self.layout_parametros.setRowVisible(self.campo_ctrl2_x, grau_cubico)
            self.layout_parametros.setRowVisible(self.campo_ctrl2_y, grau_cubico)

        elif algoritmo == "Polilinha":
            self.grupo_pontos_polilinha.setTitle("Pontos da Polilinha (N > 3)")
            self.checkbox_fechar_poligono.setVisible(True)

        elif algoritmo == "Preenchimento":
            self.grupo_pontos_polilinha.setTitle("Vértices do Polígono (N ≥ 3)")
            self.checkbox_fechar_poligono.setVisible(False)
            self.checkbox_fechar_poligono.setChecked(True)

            self.layout_parametros.setRowVisible(self.combo_tipo_preenchimento, True)

            eh_recursivo = self.combo_tipo_preenchimento.currentText().startswith("Recursivo")

            # Gerencia de forma limpa o comportamento dinâmico do container de parâmetros
            self.grupo_parametros.setVisible(True)
            self.layout_parametros.setRowVisible(self.campo_x1, eh_recursivo)
            self.layout_parametros.setRowVisible(self.campo_y1, eh_recursivo)
            self.layout_parametros.setRowVisible(self.campo_x2, False)
            self.layout_parametros.setRowVisible(self.campo_y2, False)

            self.campo_x1.setPlaceholderText("Semente X")
            self.campo_y1.setPlaceholderText("Semente Y")

        elif algoritmo == "Recorte de Polígonos":
            self.grupo_pontos_polilinha.setTitle("Vértices do Polígono (N ≥ 3)")
            self.checkbox_fechar_poligono.setVisible(False)
            self.checkbox_fechar_poligono.setChecked(True)

            # Reaproveita o grupo de parâmetros apenas para a janela de recorte
            self.grupo_parametros.setVisible(True)
            self.layout_parametros.setRowVisible(self.campo_x1, False)
            self.layout_parametros.setRowVisible(self.campo_y1, False)
            self.layout_parametros.setRowVisible(self.campo_x2, False)
            self.layout_parametros.setRowVisible(self.campo_y2, False)

            self.layout_parametros.setRowVisible(self.campo_clip_xmin, True)
            self.layout_parametros.setRowVisible(self.campo_clip_ymin, True)
            self.layout_parametros.setRowVisible(self.campo_clip_xmax, True)
            self.layout_parametros.setRowVisible(self.campo_clip_ymax, True)

        elif algoritmo == "Recorte de Linhas":
            self.campo_x1.setPlaceholderText("Linha - X1")
            self.campo_y1.setPlaceholderText("Linha - Y1")
            self.campo_x2.setPlaceholderText("Linha - X2")
            self.campo_y2.setPlaceholderText("Linha - Y2")

            self.layout_parametros.setRowVisible(self.campo_clip_xmin, True)
            self.layout_parametros.setRowVisible(self.campo_clip_ymin, True)
            self.layout_parametros.setRowVisible(self.campo_clip_xmax, True)
            self.layout_parametros.setRowVisible(self.campo_clip_ymax, True)

    # ------------------------------------------------------------------

    def obter_parametros(self):
        """
        Lê e valida os campos de acordo com o algoritmo selecionado.
        """
        algoritmo = self.algoritmo_selecionado()

        if algoritmo == "Polilinha":
            pontos = self.obter_pontos_polilinha()
            return pontos if len(pontos) > 3 else None

        if algoritmo == "Preenchimento":
            tipo_texto = self.combo_tipo_preenchimento.currentText()
            tipo = "recursivo" if tipo_texto.startswith("Recursivo") else "varredura"
            vertices = self.obter_pontos_polilinha()

            if not vertices or len(vertices) < 3:
                return None

            if tipo == "recursivo":
                try:
                    sx = int(self.campo_x1.text())
                    sy = int(self.campo_y1.text())
                    return {
                        "tipo": "recursivo",
                        "pontos": vertices,
                        "semente": (sx, sy)
                    }
                except ValueError:
                    return None
            else:
                return {
                    "tipo": "varredura",
                    "pontos": vertices,
                    "semente": None
                }

        if algoritmo == "Recorte de Polígonos":
            vertices = self.obter_pontos_polilinha()

            if not vertices or len(vertices) < 3:
                return None

            try:
                xmin = int(self.campo_clip_xmin.text())
                ymin = int(self.campo_clip_ymin.text())
                xmax = int(self.campo_clip_xmax.text())
                ymax = int(self.campo_clip_ymax.text())
            except ValueError:
                return None

            if xmin >= xmax or ymin >= ymax:
                return None

            return {
                "pontos": vertices,
                "janela": (xmin, ymin, xmax, ymax),
            }

        if algoritmo == "Recorte de Linhas":
            try:
                x1 = int(self.campo_x1.text())
                y1 = int(self.campo_y1.text())
                x2 = int(self.campo_x2.text())
                y2 = int(self.campo_y2.text())

                xmin = int(self.campo_clip_xmin.text())
                ymin = int(self.campo_clip_ymin.text())
                xmax = int(self.campo_clip_xmax.text())
                ymax = int(self.campo_clip_ymax.text())

                if not self.janela_recorte_valida(xmin, ymin, xmax, ymax):
                    return None

                return {
                    "linha": (x1, y1, x2, y2),
                    "janela": (xmin, ymin, xmax, ymax),
                }
            except ValueError:
                return None

        try:
            if algoritmo == "Círculo":
                xc = int(self.campo_x1.text())
                yc = int(self.campo_y1.text())
                raio = int(self.campo_x2.text())
                return (xc, yc, raio) if raio > 0 else None
        
            if algoritmo == "Elipse":
                xc = int(self.campo_x1.text())
                yc = int(self.campo_y1.text())
                rx = int(self.campo_x2.text())
                ry = int(self.campo_y2.text())
                return (xc, yc, rx, ry) if (rx > 0 and ry > 0) else None

            if algoritmo == "Curva de Bézier":
                p0 = (int(self.campo_x1.text()), int(self.campo_y1.text()))
                p_final = (int(self.campo_x2.text()), int(self.campo_y2.text()))
                ctrl1 = (int(self.campo_ctrl1_x.text()), int(self.campo_ctrl1_y.text()))

                if self.combo_grau_bezier.currentText().startswith("Cúbica"):
                    ctrl2 = (int(self.campo_ctrl2_x.text()), int(self.campo_ctrl2_y.text()))
                    return [p0, ctrl1, ctrl2, p_final]
                return [p0, ctrl1, p_final]

            # Por fim, trata o Bresenham (e os modos padrão estruturados de 4 pontos)
            x1 = int(self.campo_x1.text())
            y1 = int(self.campo_y1.text())
            x2 = int(self.campo_x2.text())
            y2 = int(self.campo_y2.text())
            return x1, y1, x2, y2

        except ValueError:
            return None

    def algoritmo_selecionado(self):
        return self.combo_algoritmos.currentText()

    # ------------------------------------------------------------------

    def adicionar_ponto_polilinha(self):
        try:
            x = int(self.campo_ponto_x.text())
            y = int(self.campo_ponto_y.text())
        except ValueError:
            return

        self.lista_pontos_polilinha.addItem(f"({x}, {y})")
        self.campo_ponto_x.clear()
        self.campo_ponto_y.clear()
        self.campo_ponto_x.setFocus()

    def remover_ponto_polilinha(self):
        linha_selecionada = self.lista_pontos_polilinha.currentRow()
        if linha_selecionada >= 0:
            self.lista_pontos_polilinha.takeItem(linha_selecionada)

    def obter_pontos_polilinha(self):
        pontos = []
        for i in range(self.lista_pontos_polilinha.count()):
            texto = self.lista_pontos_polilinha.item(i).text()
            texto = texto.strip("()")
            x_str, y_str = texto.split(",")
            pontos.append((int(x_str.strip()), int(y_str.strip())))
        return pontos

    def polilinha_fechada(self):
        return self.checkbox_fechar_poligono.isChecked()