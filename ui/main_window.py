"""
Objetivo: Responsável por construir a janela principal da aplicação.

Especificações:
- A janela principal deve ter um título, tamanho e layout definidos.
- A janela principal deve conter uma barra de menus, uma barra de status e um widget central.
- A barra de menus deve ter os menus "Arquivo", "Editar", "Visualizar" e "Ajuda".
- A barra de status deve exibir mensagens de status.    

Retorno:
- A classe MainWindow deve herdar de QMainWindow e implementar os métodos necessários para configurar a janela, criar os componentes e organizar o layout.

"""

from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    """
    Janela principal da aplicação.
    """

    def __init__(self):
        super().__init__()

        self.configurar_janela()

        self.criar_componentes()

        self.criar_layout()

    # ------------------------------------------------------------------

    def configurar_janela(self):
        """Configura as propriedades da janela."""

        self.setWindowTitle("Computação Gráfica")

        self.resize(1200, 800)

    # ------------------------------------------------------------------

    def criar_componentes(self):
        """Cria todos os componentes d interface."""

        # Widget central
        self.central_widget = QWidget()

        # Layout principal
        self.layout_principal = QVBoxLayout()

        # Barra de menus
        self.menu_bar = QMenuBar()
        self.menu_arquivo = self.menu_bar.addMenu("Arquivo")
        self.menu_editar = self.menu_bar.addMenu("Editar")
        self.menu_visualizar = self.menu_bar.addMenu("Visualizar")
        self.menu_ajuda = self.menu_bar.addMenu("Ajuda")

        # Barra de status

        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Aplicação iniciada.")

        # Título temporário
        self.label_titulo = QLabel("Projeto de Computação Gráfica")

        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # ------------------------------------------------------------------

    def criar_layout(self):
        """Organiza todos os componentes da interface."""

        # Layout
        self.layout_principal.addWidget(self.label_titulo)

        self.central_widget.setLayout(self.layout_principal)

        # MainWindow
        self.setMenuBar(self.menu_bar)

        self.setStatusBar(self.status_bar)

        self.setCentralWidget(self.central_widget)