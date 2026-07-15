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

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from ui.canvas_widget import CanvasWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.configurar_janela()

        self.criar_componentes()

        self.criar_layout()

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

        self.label = QLabel("Painel de ferramentas")

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # -----------------------------------------------------

    def criar_layout(self):

        painel = QVBoxLayout()

        painel.addWidget(self.label)

        self.layout_principal.addWidget(self.canvas, 4)

        painel_widget = QWidget()
        painel_widget.setLayout(painel)

        self.layout_principal.addWidget(painel_widget, 1)

        self.central_widget.setLayout(self.layout_principal)

        self.setCentralWidget(self.central_widget)

        self.canvas.desenhar_pixel(0, 0)

        self.canvas.desenhar_pixel(5, 5)

        self.canvas.desenhar_pixel(-8, 3)

        self.canvas.desenhar_pixel(10, -6)