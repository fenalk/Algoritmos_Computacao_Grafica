"""
Módulo responsável pelo algoritmo de Curvas de Bézier (graus 2 e 3).
"""

from algoritmos.bresenham import Bresenham


class Bezier:
    """
    Implementação das curvas de Bézier quadrática e cúbica,
    utilizando o algoritmo de De Casteljau para geração dos
    pontos e Bresenham para rasterização.
    """

    RESOLUCAO_PADRAO = 100

    @staticmethod
    def calcular_curva_quadratica(
        p0: tuple[int, int],
        p1: tuple[int, int],
        p2: tuple[int, int],
        resolucao: int = RESOLUCAO_PADRAO
    ) -> list[tuple[int, int]]:
        """
        Calcula uma curva de Bézier de grau 2.
        """

        return Bezier._calcular_pontos(
            [p0, p1, p2],
            resolucao
        )

    @staticmethod
    def calcular_curva_cubica(
        p0: tuple[int, int],
        p1: tuple[int, int],
        p2: tuple[int, int],
        p3: tuple[int, int],
        resolucao: int = RESOLUCAO_PADRAO
    ) -> list[tuple[int, int]]:
        """
        Calcula uma curva de Bézier de grau 3.
        """

        return Bezier._calcular_pontos(
            [p0, p1, p2, p3],
            resolucao
        )

    @staticmethod
    def _calcular_pontos(
        pontos_controle: list[tuple[int, int]],
        resolucao: int
    ) -> list[tuple[int, int]]:
        """
        Gera os pontos da curva utilizando o algoritmo
        de De Casteljau.
        """

        if resolucao <= 0:
            raise ValueError(
                "A resolução deve ser maior que zero."
            )

        curva = []

        # laço principal
        for i in range(resolucao + 1):

            t = i / resolucao

            x, y = Bezier._de_casteljau(
                pontos_controle,
                t
            )

            curva.append((round(x), round(y)))

        return curva

    @staticmethod
    def _de_casteljau(
        pontos: list[tuple[int, int]],
        t: float
    ) -> tuple[float, float]:
        """
        Executa a interpolação de De Casteljau.
        """

        pontos_intermediarios = list(pontos)

        while len(pontos_intermediarios) > 1:

            proxima_iteracao = []

            for i in range(len(pontos_intermediarios) - 1):

                x0, y0 = pontos_intermediarios[i]
                x1, y1 = pontos_intermediarios[i + 1]

                proxima_iteracao.append((
                    x0 + (x1 - x0) * t,
                    y0 + (y1 - y0) * t
                ))

            pontos_intermediarios = proxima_iteracao

        return pontos_intermediarios[0]

    @staticmethod
    def rasterizar(
        pontos_curva: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """
        Rasteriza a curva ligando os pontos consecutivos
        através do algoritmo de Bresenham.
        """

        pixels = []
        pixels_visitados = set()

        for ponto_inicial, ponto_final in zip(
            pontos_curva,
            pontos_curva[1:]
        ):

            segmento = Bresenham.calcular_reta(
                ponto_inicial[0],
                ponto_inicial[1],
                ponto_final[0],
                ponto_final[1]
            )

            for pixel in segmento:
                if pixel not in pixels_visitados:
                    pixels_visitados.add(pixel)
                    pixels.append(pixel)

        return pixels