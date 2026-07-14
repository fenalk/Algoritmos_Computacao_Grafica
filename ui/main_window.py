from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Computação Gráfica")
        self.resize(900, 600)

        central_widget = QWidget()

        layout = QVBoxLayout()

        texto = QLabel("Trabalho Prático de Computação Gráfica")
        layout.addWidget(texto)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)