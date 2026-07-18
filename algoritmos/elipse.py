"""
Módulo responsável pelo algoritmo de elipse (ponto médio).
"""


class Elipse:
    """
    Implementação do algoritmo do ponto médio para rasterização
    de elipses utilizando simetria dos 4 quadrantes.
    """

    @staticmethod
    def calcular_elipse(
        xc: int,
        yc: int,
        rx: int,
        ry: int
    ) -> list[tuple[int, int]]:
        """
        Calcula os pixels de uma elipse.

        Parâmetros:
            xc: coordenada X do centro.
            yc: coordenada Y do centro.
            rx: semieixo horizontal.
            ry: semieixo vertical.

        Retorno:
            Lista de pontos pertencentes à elipse.
        """

        if rx <= 0 or ry <= 0:
            raise ValueError(
                "Os semieixos devem ser maiores que zero."
            )

        pontos = []

        x = 0
        y = ry

        rx2 = rx ** 2
        ry2 = ry ** 2

        dx = 2 * ry2 * x
        dy = 2 * rx2 * y

        # Região 1: inclinação da curva menor que 1
        parametro1 = ry2 - (rx2 * ry) + (0.25 * rx2)

        Elipse._adicionar_pontos_simetricos(
            pontos, xc, yc, x, y
        )

        while dx < dy:

            x += 1
            dx += 2 * ry2

            if parametro1 < 0:
                parametro1 += dx + ry2
            else:
                y -= 1
                dy -= 2 * rx2
                parametro1 += dx - dy + ry2

            Elipse._adicionar_pontos_simetricos(
                pontos, xc, yc, x, y
            )

        # Região 2: inclinação da curva maior ou igual a 1
        parametro2 = (
            ry2 * (x + 0.5) ** 2
            + rx2 * (y - 1) ** 2
            - rx2 * ry2
        )

        while y > 0:

            y -= 1
            dy -= 2 * rx2

            if parametro2 > 0:
                parametro2 += rx2 - dy
            else:
                x += 1
                dx += 2 * ry2
                parametro2 += dx - dy + rx2

            Elipse._adicionar_pontos_simetricos(
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
        Adiciona os pontos equivalentes nos 4 quadrantes da elipse.
        """

        simetrias = [
            ( x,  y),
            (-x,  y),
            ( x, -y),
            (-x, -y),
        ]

        for dx, dy in simetrias:
            pontos.append((xc + dx, yc + dy))