"""
Módulo responsável pelos algoritmos de preenchimento
de polígonos: Flood Fill e Scanline.
"""

from algoritmos.polilinha import Polilinha


class Preenchimento:
    """
    Implementação dos algoritmos de preenchimento
    recursivo (Flood Fill) e por varredura (Scanline).
    """

    LIMITE_SEGURANCA = 5000

    @staticmethod
    def calcular_contorno(
        vertices: list[tuple[int, int]]
    ) -> list[tuple[int, int]] | None:
        """
        Calculo do contorno do polígono utilizando
        o algoritmo de Bresenham.
        """
        if vertices is None or len(vertices) < 3:
            return None

        return Polilinha.calcular_polilinha(
            vertices,
            fechada=True
        )

    @staticmethod
    def preencher_recursivo(
        vertices: list[tuple[int, int]],
        semente: tuple[int, int],
        limites: tuple[int, int, int, int] = (-15, 15, -15, 15) # <--- CORREÇÃO: Limites iniciais mais condizentes com sua grade mundial
    ) -> tuple[
        list[tuple[int, int]],
        list[tuple[int, int]]
    ] | None:
        """
        Executa o preenchimento Flood Fill usando pilha (iterativo para evitar RecursionError).
        """
        contorno = Preenchimento.calcular_contorno(vertices)

        if contorno is None:
            return None

        contorno_pixels = set(contorno)

        if semente in contorno_pixels:
            return None

        x_min, x_max, y_min, y_max = limites

        pixels_visitados = set()
        pixels_preenchidos = []

        pilha = [semente]

        while pilha:
            x, y = pilha.pop()

            if (x, y) in pixels_visitados or (x, y) in contorno_pixels:
                continue

            # Garante que o preenchimento não vai tentar renderizar infinitamente fora da área visível do canvas
            if not (x_min <= x <= x_max and y_min <= y <= y_max):
                continue

            pixels_visitados.add((x, y))
            pixels_preenchidos.append((x, y))

            if len(pixels_preenchidos) > Preenchimento.LIMITE_SEGURANCA:
                return None

            pilha.extend([
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ])

        return contorno, pixels_preenchidos

    @staticmethod
    def preencher_varredura(
        vertices: list[tuple[int, int]]
    ) -> tuple[
        list[tuple[int, int]],
        list[tuple[int, int]]
    ] | None:
        """
        Executa o preenchimento por varredura (Scanline).
        """
        contorno = Preenchimento.calcular_contorno(vertices)

        if contorno is None:
            return None

        pixels_preenchidos = []
        quantidade_vertices = len(vertices)
        coordenadas_y = [y for _, y in vertices]

        y_min = min(coordenadas_y)
        y_max = max(coordenadas_y)

        for y in range(y_min, y_max + 1):
            intersecoes = []

            for indice in range(quantidade_vertices):
                x1, y1 = vertices[indice]
                x2, y2 = vertices[(indice + 1) % quantidade_vertices]

                if y1 == y2:
                    continue

                if min(y1, y2) <= y < max(y1, y2):
                    x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersecoes.append(x)

            intersecoes.sort()

            for indice in range(0, len(intersecoes) - 1, 2):
                x_inicio = round(intersecoes[indice])
                x_fim = round(intersecoes[indice + 1])

                for x in range(x_inicio, x_fim + 1):
                    pixels_preenchidos.append((x, y))

        return contorno, pixels_preenchidos