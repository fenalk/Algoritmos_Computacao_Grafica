"""
Módulo responsável pelo painel lateral de controles da aplicação.
"""

from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PainelControles(QWidget):
    """
    Painel lateral responsável pela interação do usuário.
    """

    ALGORITMOS = [
        "Bresenham",
        "Círculo",
        "Elipse",
        "Curva de Bézier",
        "Polilinha",
        "Preenchimento",
        "Recorte",
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
        self.layout_parametros.addRow("X1:", self.campo_x1)
        self.layout_parametros.addRow("Y1:", self.campo_y1)
        self.layout_parametros.addRow("Ctrl1 X:", self.campo_ctrl1_x)
        self.layout_parametros.addRow("Ctrl1 Y:", self.campo_ctrl1_y)
        self.layout_parametros.addRow("Ctrl2 X:", self.campo_ctrl2_x)
        self.layout_parametros.addRow("Ctrl2 Y:", self.campo_ctrl2_y)
        self.layout_parametros.addRow("X2:", self.campo_x2)
        self.layout_parametros.addRow("Y2:", self.campo_y2)
        self.grupo_parametros.setLayout(self.layout_parametros)

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.botao_desenhar)
        layout_botoes.addWidget(self.botao_limpar)

        layout_principal.addWidget(self.grupo_algoritmo)
        layout_principal.addWidget(self.grupo_parametros)
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

    # ------------------------------------------------------------------

    def atualizar_parametros(self, algoritmo):
        # Por padrão, esconde tudo que é específico de Bézier
        self.layout_parametros.setRowVisible(self.combo_grau_bezier, False)
        self.layout_parametros.setRowVisible(self.campo_ctrl1_x, False)
        self.layout_parametros.setRowVisible(self.campo_ctrl1_y, False)
        self.layout_parametros.setRowVisible(self.campo_ctrl2_x, False)
        self.layout_parametros.setRowVisible(self.campo_ctrl2_y, False)
        self.layout_parametros.setRowVisible(self.campo_y2, True)

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

        elif algoritmo == "Curva de Bézier":
            self.campo_x1.setPlaceholderText("Inicial X")
            self.campo_y1.setPlaceholderText("Inicial Y")
            self.campo_x2.setPlaceholderText("Final X")
            self.campo_y2.setPlaceholderText("Final Y")

            self.layout_parametros.setRowVisible(self.combo_grau_bezier, True)
            self.layout_parametros.setRowVisible(self.campo_ctrl1_x, True)
            self.layout_parametros.setRowVisible(self.campo_ctrl1_y, True)

            # Ponto de controle 2 só existe na curva cúbica (grau 3)
            grau_cubico = self.combo_grau_bezier.currentText().startswith(
                "Cúbica"
            )
            self.layout_parametros.setRowVisible(
                self.campo_ctrl2_x, grau_cubico
            )
            self.layout_parametros.setRowVisible(
                self.campo_ctrl2_y, grau_cubico
            )

    # ------------------------------------------------------------------
    # Novo: expõe os valores digitados para quem conectar os botões
    # (a MainWindow), mantendo o painel sem conhecer os algoritmos.

    def obter_parametros(self):
        """
        Lê e valida os campos de acordo com o algoritmo selecionado.

        Retorno
        -------
        tuple | None
            - Bresenham: (x1, y1, x2, y2)
            - Círculo:   (xc, yc, raio)
            - Bézier:    lista de pontos [P0, P1, ..., Pn]
            ou None caso algum campo esteja vazio/inválido.
        """

        algoritmo = self.algoritmo_selecionado()

        try:
            if algoritmo == "Círculo":
                xc = int(self.campo_x1.text())
                yc = int(self.campo_y1.text())
                raio = int(self.campo_x2.text())

                if raio <= 0:
                    return None

                return xc, yc, raio

            if algoritmo == "Curva de Bézier":
                p0 = (int(self.campo_x1.text()), int(self.campo_y1.text()))
                p_final = (int(self.campo_x2.text()), int(self.campo_y2.text()))
                ctrl1 = (
                    int(self.campo_ctrl1_x.text()),
                    int(self.campo_ctrl1_y.text()),
                )

                grau_cubico = self.combo_grau_bezier.currentText().startswith(
                    "Cúbica"
                )

                if grau_cubico:
                    ctrl2 = (
                        int(self.campo_ctrl2_x.text()),
                        int(self.campo_ctrl2_y.text()),
                    )
                    return [p0, ctrl1, ctrl2, p_final]

                return [p0, ctrl1, p_final]

            x1 = int(self.campo_x1.text())
            y1 = int(self.campo_y1.text())
            x2 = int(self.campo_x2.text())
            y2 = int(self.campo_y2.text())
        except ValueError:
            return None

        return x1, y1, x2, y2

    def algoritmo_selecionado(self):
        return self.combo_algoritmos.currentText()
