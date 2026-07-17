"""
Módulo responsável pela janela principal da aplicação.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
)

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

        # Componentes principais
        self.canvas = CanvasWidget()
        self.painel = PainelControles()

    # -----------------------------------------------------

    def criar_layout(self):
        """
        Organiza os componentes da interface.
        """

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

    def resizeEvent(self, event):
        """
        Ajusta o canvas quando a janela é redimensionada.
        """

        super().resizeEvent(event)

        self.canvas.fitInView(
            self.canvas.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio,
        )

        self.canvas.centerOn(0, 0)