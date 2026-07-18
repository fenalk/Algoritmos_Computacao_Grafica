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

        self.campo_x1 = QLineEdit()
        self.campo_x1.setPlaceholderText("Digite X1")

        self.campo_y1 = QLineEdit()
        self.campo_y1.setPlaceholderText("Digite Y1")

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
        self.layout_parametros.addRow("X1:", self.campo_x1)
        self.layout_parametros.addRow("Y1:", self.campo_y1)
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

    # ------------------------------------------------------------------

    def atualizar_parametros(self, algoritmo):
        if algoritmo == "Bresenham":
            self.campo_x1.setPlaceholderText("Digite X1")
            self.campo_y1.setPlaceholderText("Digite Y1")
            self.campo_x2.setPlaceholderText("Digite X2")
            self.campo_y2.setPlaceholderText("Digite Y2")

            self.layout_parametros.setRowVisible(self.campo_y2, True)

        elif algoritmo == "Círculo":
            self.campo_x1.setPlaceholderText("Centro X")
            self.campo_y1.setPlaceholderText("Centro Y")
            self.campo_x2.setPlaceholderText("Raio")

            self.layout_parametros.setRowVisible(self.campo_y2, False)

        elif algoritmo == "Elipse":
            self.campo_x1.setPlaceholderText("Centro X")
            self.campo_y1.setPlaceholderText("Centro Y")
            self.campo_x2.setPlaceholderText("Raio X (rx)")
            self.campo_y2.setPlaceholderText("Raio Y (ry)")

            self.layout_parametros.setRowVisible(self.campo_y2, True)

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
            - Elipse:    (xc, yc, rx, ry)
            ou None caso algum campo esteja vazio, inválido, ou
            (círculo/elipse) algum raio não seja positivo.
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

            if algoritmo == "Elipse":
                xc = int(self.campo_x1.text())
                yc = int(self.campo_y1.text())
                rx = int(self.campo_x2.text())
                ry = int(self.campo_y2.text())

                if rx <= 0 or ry <= 0:
                    return None

                return xc, yc, rx, ry

            x1 = int(self.campo_x1.text())
            y1 = int(self.campo_y1.text())
            x2 = int(self.campo_x2.text())
            y2 = int(self.campo_y2.text())
        except ValueError:
            return None

        return x1, y1, x2, y2

    def algoritmo_selecionado(self):
        return self.combo_algoritmos.currentText()
