"""
Módulo responsável pelo algoritmo de circunferência (ponto médio).
"""


class Circulo:
    """
    Implementação do algoritmo do ponto médio para rasterização
    de circunferências utilizando simetria de 8 octantes.
    """

    @staticmethod
    def calcular_circulo(xc: int, yc: int, raio: int) -> list[tuple[int, int]]:
        """
        Calcula os pixels de uma circunferência.

        Parâmetros:
            xc: coordenada X do centro.
            yc: coordenada Y do centro.
            raio: raio da circunferência.

        Retorno:
            Lista de pontos (x, y) pertencentes à circunferência.
        """

        if raio < 0:
            raise ValueError("O raio deve ser maior ou igual a zero.")

        pontos = []

        x = 0
        y = raio
        erro = 1 - raio

        Circulo._adicionar_pontos_simetricos(
            pontos, xc, yc, x, y
        )

        while x < y:

            if erro < 0:
                erro += 2 * x + 3
            else:
                erro += 2 * (x - y) + 5
                y -= 1

            x += 1

            Circulo._adicionar_pontos_simetricos(
                pontos, xc, yc, x, y
            )

        return pontos

    @staticmethod
    def _adicionar_pontos_simetricos(
        pontos: list[tuple[int, int]],
        xc: int,
        yc: int,
        x: int,
        y: int
    ):
        """
        Adiciona os pontos correspondentes aos 8 octantes
        da circunferência.
        """

        simetrias = [
            ( x,  y),
            (-x,  y),
            ( x, -y),
            (-x, -y),
            ( y,  x),
            (-y,  x),
            ( y, -x),
            (-y, -x),
        ]

        for dx, dy in simetrias:
            pontos.append((xc + dx, yc + dy))