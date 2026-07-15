"""
Algoritmo de Bresenham

Objetivo:
- Implementar o algoritmo de Bresenham para rasterização de retas utilizando apenas operações inteiras.

Especificidades:
- Recebe dois pontos (x1, y1) e (x2, y2) do sistema cartesiano como entrada e calcula todos os pixels pertencentes à reta que conecta esses pontos.

Retorno:
- Uma lista contendo as coordenadas dos pixels da reta, representadas como tuplas (x, y).
"""

class Bresenham:
    """
    Classe responsável pela implementação do algoritmo de Bresenham.
    """

    @staticmethod
    def calcular_reta(x1, y1, x2, y2):
        """
        Objetivo: Calcular os pontos da reta.

        Parâmetros: x1, y1, x2, y2 (int): Coordenadas dos pontos inicial e final da reta.

        Retorno: List[Tuple[int, int]]: Lista de coordenadas dos pixels da reta.
        """

        pontos = []

        dx = abs(x2 - x1)
        dy = abs (y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        erro = dx - dy 

        while True:
            pontos.append((x1, y1))

            if x1 == x2 and y1 == y2:
                break

            e2 = 2 * erro
            if e2 > -dy:
                erro -= dy
                x1 += sx
            
            if e2 < dx:
                erro += dx
                y1 += sy

        return pontos 