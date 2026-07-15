"""
Módulo responsável pelo painel lateral de controles da aplicação.

Objetivo:
    Disponibilizar a interface de interação entre o usuário e os
    algoritmos de Computação Gráfica, permitindo selecionar o algoritmo,
    informar seus parâmetros e executar as ações disponíveis.

Especificidades:
    - Exibe a lista de algoritmos de síntese de imagem.
    - Disponibiliza um formulário para entrada de parâmetros.
    - Contém botões para desenhar e limpar o canvas.
    - A estrutura foi preparada para permitir alterações dinâmicas
      dos parâmetros conforme o algoritmo selecionado.

Retorno:
    O painel não retorna valores. Sua função é fornecer os componentes
    gráficos utilizados pela aplicação.
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

    Objetivo:
        Centralizar todos os controles da aplicação, permitindo a
        seleção dos algoritmos e a entrada de parâmetros necessários
        para sua execução.

    Especificidades:
        - Organiza os componentes utilizando layouts do Qt.
        - Disponibiliza uma lista de algoritmos.
        - Disponibiliza campos de entrada para parâmetros.
        - Disponibiliza botões para execução das ações.

    Retorno:
        Nenhum.
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
        """
        Inicializa o painel de controles.

        Parâmetros
        ----------
        parent : QWidget | None, opcional
            Widget pai do painel.

        Retorno
        -------
        None
        """
        super().__init__(parent)

        self.criar_componentes()
        self.criar_layout()
        self.conectar_sinais()

        self.atualizar_parametros(
        self.combo_algoritmos.currentText()
)

    # ------------------------------------------------------------------

    def criar_componentes(self):
        """
        Cria todos os componentes gráficos do painel.

        Especificidades
        ----------------
        Cria:
        - ComboBox para seleção dos algoritmos;
        - Campos de entrada de parâmetros;
        - Botões de ação;
        - GroupBox utilizados na organização da interface.

        Retorno
        -------
        None
        """

        self.setMinimumWidth(300)

        # Grupo de seleção
        self.grupo_algoritmo = QGroupBox("Algoritmo")

        # Grupo de parâmetros
        self.grupo_parametros = QGroupBox("Parâmetros")

        # ComboBox
        self.combo_algoritmos = QComboBox()
        self.combo_algoritmos.addItems(self.ALGORITMOS)

        # Campos
        self.campo_x1 = QLineEdit()
        self.campo_x1.setPlaceholderText("Digite X1")

        self.campo_y1 = QLineEdit()
        self.campo_y1.setPlaceholderText("Digite Y1")

        self.campo_x2 = QLineEdit()
        self.campo_x2.setPlaceholderText("Digite X2")

        self.campo_y2 = QLineEdit()
        self.campo_y2.setPlaceholderText("Digite Y2")

        # Botões
        self.botao_desenhar = QPushButton("Desenhar")
        self.botao_limpar = QPushButton("Limpar")

        self.botao_desenhar.setMinimumHeight(35)
        self.botao_limpar.setMinimumHeight(35)

    # ------------------------------------------------------------------

    def criar_layout(self):
        """
        Organiza todos os componentes da interface.

        Especificidades
        ----------------
        Estrutura o painel utilizando:
        - QVBoxLayout
        - QFormLayout
        - QHBoxLayout
        - QGroupBox

        Retorno
        -------
        None
        """

        layout_principal = QVBoxLayout()

        layout_principal.setContentsMargins(10, 10, 10, 10)

        layout_principal.setSpacing(10)

        # --------------------------------------------------
        # Algoritmos

        layout_algoritmo = QVBoxLayout()

        layout_algoritmo.addWidget(self.combo_algoritmos)

        self.grupo_algoritmo.setLayout(layout_algoritmo)

        # --------------------------------------------------
        # Parâmetros

        self.layout_parametros = QFormLayout()

        self.layout_parametros.addRow("X1:", self.campo_x1)
        self.layout_parametros.addRow("Y1:", self.campo_y1)
        self.layout_parametros.addRow("X2:", self.campo_x2)
        self.layout_parametros.addRow("Y2:", self.campo_y2)

        self.grupo_parametros.setLayout(self.layout_parametros)

        # --------------------------------------------------
        # Botões

        layout_botoes = QHBoxLayout()

        layout_botoes.addWidget(self.botao_desenhar)

        layout_botoes.addWidget(self.botao_limpar)

        # --------------------------------------------------
        # Organização Final

        layout_principal.addWidget(self.grupo_algoritmo)

        layout_principal.addWidget(self.grupo_parametros)

        layout_principal.addStretch()

        layout_principal.addLayout(layout_botoes)

        self.setLayout(layout_principal)

    # ------------------------------------------------------------------

    def conectar_sinais(self):
        """
        Conecta os sinais internos do painel.

        Especificidades
        ----------------
        Realiza conexões relacionadas apenas aos componentes internos
        do painel.

        A comunicação com a MainWindow será realizada externamente,
        mantendo a separação de responsabilidades.

        Retorno
        -------
        None
        """

        self.combo_algoritmos.currentTextChanged.connect(
            self.atualizar_parametros
        )

    # ------------------------------------------------------------------

    def atualizar_parametros(self, algoritmo):
        """
        Atualiza os campos de entrada conforme o algoritmo selecionado.

        Parâmetros
        ----------
        algoritmo : str
            Algoritmo selecionado no ComboBox.

        Retorno
        -------
        None
        """

        if algoritmo == "Bresenham":

            self.campo_x1.setPlaceholderText(
                "Digite X1"
            )

            self.campo_y1.setPlaceholderText(
                "Digite Y1"
            )

            self.campo_x2.setPlaceholderText(
                "Digite X2"
            )

            self.campo_y2.setPlaceholderText(
                "Digite Y2"
            )