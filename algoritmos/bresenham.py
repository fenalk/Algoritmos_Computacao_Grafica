"""
Algoritmo de Bresenham

Calcula todos os pixels de uma reta utilizando o algoritmo de Bresenham.

Parâmetros
----------
x1 : int
    Coordenada X inicial.
y1 : int
    Coordenada Y inicial.
x2 : int
    Coordenada X final.
y2 : int
    Coordenada Y final.

Retorno
-------
list[tuple[int, int]]
    Lista contendo os pixels da reta.
"""

class Bresenham:
    """
    Classe responsável pela implementação do algoritmo de Bresenham.
    """

    @staticmethod
    def calcular_reta(x1, y1, x2, y2):
        """
        Objetivo: Calcular os pontos da reta.

        Parâmetros: x1, y1, x2, y2 (int): Coordenadas dos pontos
        inicial e final da reta.

        Retorno: List[Tuple[int, int]]: Lista de coordenadas dos
        pixels da reta.
        """

        pontos = []

        # Diferença entre os pontos
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        #Sentido do crescimento da reta
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        # Variável de erro  
        erro = dx - dy

        # Percorre todos os pixels da reta até atingir o ponto final (x2, y2).
        while True:
            pontos.append((x1, y1))

            if x1 == x2 and y1 == y2:
                break

            erro_duplo = 2 * erro
            if erro_duplo > -dy:
                erro -= dy
                x1 += sx

            if erro_duplo < dx:
                erro += dx
                y1 += sy

        return pontos
