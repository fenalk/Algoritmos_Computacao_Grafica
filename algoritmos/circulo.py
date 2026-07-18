"""
Módulo responsável pelo algoritmo de circunferência (ponto médio).
"""


class Circulo:
    """
    Implementação do algoritmo do ponto médio (Midpoint Circle
    Algorithm) para o traçado de circunferências.
    """

    @staticmethod
    def calcular_circulo(xc: int, yc: int, raio: int):
        """
        Calcula os pixels de uma circunferência de centro (xc, yc)
        e raio `raio`, usando o algoritmo do ponto médio com
        simetria de 8 partes.

        Retorno
        -------
        list[tuple[int, int]]
            Lista de pontos (x, y) que compõem a circunferência.
        """

        pontos = []

        x = 0
        y = raio
        d = 1 - raio

        Circulo._adicionar_pontos_simetricos(pontos, xc, yc, x, y)

        while x < y:
            if d < 0:
                # Ponto médio dentro do círculo -> escolhe E
                d += 2 * x + 3
            else:
                # Ponto médio fora do círculo -> escolhe SE
                d += 2 * (x - y) + 5
                y -= 1

            x += 1

            Circulo._adicionar_pontos_simetricos(pontos, xc, yc, x, y)

        return pontos

    # ------------------------------------------------------------------

    @staticmethod
    def _adicionar_pontos_simetricos(pontos, xc, yc, x, y):
        """
        Replica o ponto (x, y) calculado para os 8 octantes da
        circunferência.
        """

        pontos.append((xc + x, yc + y))
        pontos.append((xc - x, yc + y))
        pontos.append((xc + x, yc - y))
        pontos.append((xc - x, yc - y))
        pontos.append((xc + y, yc + x))
        pontos.append((xc - y, yc + x))
        pontos.append((xc + y, yc - x))
        pontos.append((xc - y, yc - x))