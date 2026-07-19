"""Algoritmos de preenchimento de polígonos: Flood Fill e Scanline."""

from math import ceil, floor
from typing import Optional

from algoritmos.bresenham import Bresenham

Ponto = tuple[int, int]
Limites = tuple[int, int, int, int]


class Preenchimento:
    LIMITE_SEGURANCA = 1_000_000
    MARGEM_LIMITES = 2

    # ---------- contorno ----------

    @staticmethod
    def calcular_contorno(vertices: list[Ponto]) -> Optional[list[Ponto]]:
        """Rasteriza as arestas com Bresenham, fechando o polígono."""
        if not vertices or len(vertices) < 3:
            return None

        contorno = []
        n = len(vertices)

        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            segmento = Bresenham.calcular_reta(x1, y1, x2, y2)

            if not segmento:
                return None

            # Tapa "furos" diagonais (ex: (5,5)->(6,6)), que só se tocam
            # pelo canto e deixariam o Flood Fill vazar do polígono.
            for (px, py), (qx, qy) in zip(segmento, segmento[1:]):
                if px != qx and py != qy:
                    contorno.append((qx, py))
            contorno.extend(segmento)

        return list(dict.fromkeys(contorno))  # remove duplicados, mantém ordem

    @staticmethod
    def calcular_bounding_box(vertices: list[Ponto], margem: int = MARGEM_LIMITES) -> Limites:
        xs, ys = [p[0] for p in vertices], [p[1] for p in vertices]
        return min(xs) - margem, max(xs) + margem, min(ys) - margem, max(ys) + margem

    @staticmethod
    def _dentro(x: int, y: int, limites: Limites) -> bool:
        x_min, x_max, y_min, y_max = limites
        return x_min <= x <= x_max and y_min <= y <= y_max

    # ---------- flood fill ----------

    @staticmethod
    def preencher_recursivo(
        vertices: list[Ponto], semente: Ponto, limites: Optional[Limites] = None
    ) -> Optional[tuple[list[Ponto], list[Ponto]]]:
        contorno = Preenchimento.calcular_contorno(vertices)
        if contorno is None:
            return None

        pixels_contorno = set(contorno)
        limites = limites or Preenchimento.calcular_bounding_box(vertices)

        if semente in pixels_contorno or not Preenchimento._dentro(*semente, limites):
            return None

        visitados = set()
        preenchidos = []
        pilha = [semente]

        while pilha:
            x, y = pilha.pop()
            atual = (x, y)

            if atual in visitados or atual in pixels_contorno:
                continue
            if not Preenchimento._dentro(x, y, limites):
                continue

            visitados.add(atual)
            preenchidos.append(atual)

            if len(preenchidos) > Preenchimento.LIMITE_SEGURANCA:
                return None

            pilha.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

        return contorno, preenchidos

    # ---------- scanline ----------

    @staticmethod
    def preencher_varredura(vertices: list[Ponto]) -> Optional[tuple[list[Ponto], list[Ponto]]]:
        contorno = Preenchimento.calcular_contorno(vertices)
        if contorno is None:
            return None

        n = len(vertices)
        ys = [y for _, y in vertices]
        preenchidos = set()

        for y in range(min(ys), max(ys) + 1):
            intersecoes = []

            for i in range(n):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % n]

                if y1 == y2:
                    continue
                if min(y1, y2) <= y < max(y1, y2):
                    intersecoes.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))

            intersecoes.sort()

            for i in range(0, len(intersecoes) - 1, 2):
                x_inicio, x_fim = ceil(intersecoes[i]), floor(intersecoes[i + 1])
                x_inicio, x_fim = min(x_inicio, x_fim), max(x_inicio, x_fim)
                preenchidos.update((x, y) for x in range(x_inicio, x_fim + 1))

        return contorno, list(preenchidos)