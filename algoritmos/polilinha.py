"""
Módulo responsável pelo algoritmo de Polilinha.
"""

from algoritmos.bresenham import Bresenham


class Polilinha:
    """
    Implementação do algoritmo de polilinha.

    Conecta uma sequência de pontos utilizando segmentos
    de reta rasterizados pelo algoritmo de Bresenham.
    """

    MINIMO_PONTOS = 4

    @staticmethod
    def validar_pontos(
        pontos: list[tuple[int, int]] | None
    ) -> bool:
        """
        Verifica se a quantidade de pontos é válida.
        """

        return (
            pontos is not None
            and len(pontos) >= Polilinha.MINIMO_PONTOS
        )

    @staticmethod
    def calcular_polilinha(
        pontos: list[tuple[int, int]],
        fechada: bool = False
    ) -> list[tuple[int, int]] | None:
        """
        Calcula os pixels da polilinha.

        Parâmetros:
            pontos: sequência de pontos da polilinha.
            fechada: indica se o último ponto será ligado ao primeiro.

        Retorno:
            Lista de pixels da polilinha ou None caso
            a entrada seja inválida.
        """

        if not Polilinha.validar_pontos(pontos):
            return None

        pixels = []
        pixels_visitados = set()

        quantidade_segmentos = (
            len(pontos)
            if fechada
            else len(pontos) - 1
        )

        for indice in range(quantidade_segmentos):

            ponto_inicial = pontos[indice]
            ponto_final = pontos[
                (indice + 1) % len(pontos)
            ]

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