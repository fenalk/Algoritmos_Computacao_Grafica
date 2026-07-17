"""
Módulo responsável pela janela principal da aplicação.

Objetivo:
    Criar a estrutura principal da interface gráfica,
    integrando canvas, painel de controles e algoritmos.

- configurar_janela(): Configura a janela principal, definindo o título, tamanho e layout.

- criar_componentes(): Cria os componentes da janela principal, incluindo a barra de menus, barra de status e widget central. A barra de menus tem os menus 'Arquivo', 'Editar', 'Visualizar' e 'Ajuda'. A barra de status deve exibir mensagens de status.

- criar_layout(): Organiza os componentes na janela principal, definindo o layout e adicionando
  os widgets necessários.

Retorno:
- A classe MainWindow deve herdar de QMainWindow e implementar os métodos necessários para configurar a janela, criar os componentes e organizar o layout.
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
        """
        Configura a janela principal.
        """

        self.setWindowTitle("Computação Gráfica")
        self.resize(1200, 800)

    # -----------------------------------------------------

    def criar_componentes(self):
        """
        Cria os componentes da interface.
        """

        # Barra de menus
        self.menuBar().addMenu("Arquivo")
        self.menuBar().addMenu("Editar")
        self.menuBar().addMenu("Visualizar")
        self.menuBar().addMenu("Ajuda")

        # Barra de status
        self.statusBar().showMessage("Aplicação iniciada.")

        # Widget central
        self.central_widget = QWidget()

        # Layout principal
        self.layout_principal = QHBoxLayout()

        # Canvas
        self.canvas = CanvasWidget()

        # Painel lateral
        self.painel = PainelControles()

        # Apenas exemplo de label
        self.label = QLabel("Painel de ferramentas")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # -----------------------------------------------------

    def criar_layout(self):
        """
        Organiza os componentes da interface.
        """

        # Canvas ocupa a maior parte da tela
        self.layout_principal.addWidget(self.canvas, 4)

        # Painel lateral ocupa menos espaço
        self.layout_principal.addWidget(self.painel, 1)

        # Remove margens excessivas
        self.layout_principal.setContentsMargins(5, 5, 5, 5)
        self.layout_principal.setSpacing(5)

        # Define o layout no widget central
        self.central_widget.setLayout(self.layout_principal)

        # Define o widget central da janela
        self.setCentralWidget(self.central_widget)

        # Centraliza a visualização no ponto (0, 0)
        self.canvas.centerOn(0, 0)

        # Ajusta a cena ao tamanho disponível
        self.canvas.fitInView(
            self.canvas.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )


    # -----------------------------------------------------

    def resizeEvent(self, event):
        """
        Ajusta a visualização quando a janela é redimensionada.
        """

        super().resizeEvent(event)

        self.canvas.fitInView(
            self.canvas.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

        self.canvas.centerOn(0, 0)
