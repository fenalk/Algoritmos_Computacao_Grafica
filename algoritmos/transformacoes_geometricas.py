"""
Módulo responsável pelas transformações geométricas 2D: translação,
escala (com ponto fixo) e rotação (com pivô arbitrário), usando
matrizes de transformação em coordenadas homogêneas.
"""

import math


class Transformacoes:
    """
    Implementação das transformações geométricas básicas sobre um
    polígono (lista de vértices (x, y)):

    - Translação: desloca todos os vértices por (dx, dy).
    - Escala: aplica um fator de escala (sx, sy) em relação a um
      ponto fixo qualquer (não necessariamente a origem).
    - Rotação: rotaciona os vértices por um ângulo (em graus, sentido
      anti-horário) em torno de um pivô arbitrário.

    Cada transformação é construída como uma matriz 3x3 (coordenadas
    homogêneas) e aplicada a cada vértice do polígono.
    """

    # ------------------------------------------------------------------
    # Utilitários de matriz
    # ------------------------------------------------------------------

    @staticmethod
    def _multiplicar_matrizes(a, b):
        """
        Multiplica duas matrizes 3x3.
        """

        resultado = [[0.0, 0.0, 0.0] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                resultado[i][j] = sum(a[i][k] * b[k][j] for k in range(3))

        return resultado

    @staticmethod
    def _aplicar_matriz(vertices, matriz):
        """
        Aplica uma matriz de transformação 3x3 a cada vértice
        (coordenadas homogêneas: (x, y, 1)).
        """

        transformados = []

        for x, y in vertices:
            vetor = (x, y, 1)
            x_novo = sum(matriz[0][i] * vetor[i] for i in range(3))
            y_novo = sum(matriz[1][i] * vetor[i] for i in range(3))
            transformados.append((x_novo, y_novo))

        return transformados

    # ------------------------------------------------------------------
    # Translação
    # ------------------------------------------------------------------

    @staticmethod
    def matriz_translacao(dx, dy):
        return [
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1],
        ]

    @staticmethod
    def transladar(vertices, dx, dy):
        """
        Translada o polígono por (dx, dy).
        """

        matriz = Transformacoes.matriz_translacao(dx, dy)
        pontos = Transformacoes._aplicar_matriz(vertices, matriz)

        return [(round(x), round(y)) for x, y in pontos]

    # ------------------------------------------------------------------
    # Escala com ponto fixo
    # ------------------------------------------------------------------

    @staticmethod
    def matriz_escala(sx, sy, ponto_fixo):
        """
        Monta a matriz de escala (sx, sy) em torno de um ponto fixo
        arbitrário (px, py), combinando:
        T(px, py) * S(sx, sy) * T(-px, -py)
        """

        px, py = ponto_fixo

        t_para_origem = Transformacoes.matriz_translacao(-px, -py)
        escala = [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1],
        ]
        t_de_volta = Transformacoes.matriz_translacao(px, py)

        return Transformacoes._multiplicar_matrizes(
            t_de_volta,
            Transformacoes._multiplicar_matrizes(escala, t_para_origem),
        )

    @staticmethod
    def escalar(vertices, sx, sy, ponto_fixo):
        """
        Escala o polígono por (sx, sy) em torno de `ponto_fixo`.
        """

        matriz = Transformacoes.matriz_escala(sx, sy, ponto_fixo)
        pontos = Transformacoes._aplicar_matriz(vertices, matriz)

        return [(round(x), round(y)) for x, y in pontos]

    # ------------------------------------------------------------------
    # Rotação com pivô
    # ------------------------------------------------------------------

    @staticmethod
    def matriz_rotacao(angulo_graus, pivo):
        """
        Monta a matriz de rotação de `angulo_graus` (sentido
        anti-horário) em torno de um pivô arbitrário (px, py),
        combinando:
        T(px, py) * R(angulo) * T(-px, -py)
        """

        px, py = pivo
        theta = math.radians(angulo_graus)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        t_para_origem = Transformacoes.matriz_translacao(-px, -py)
        rotacao = [
            [cos_t, -sin_t, 0],
            [sin_t, cos_t, 0],
            [0, 0, 1],
        ]
        t_de_volta = Transformacoes.matriz_translacao(px, py)

        return Transformacoes._multiplicar_matrizes(
            t_de_volta,
            Transformacoes._multiplicar_matrizes(rotacao, t_para_origem),
        )

    @staticmethod
    def rotacionar(vertices, angulo_graus, pivo):
        """
        Rotaciona o polígono por `angulo_graus` em torno de `pivo`.
        """

        matriz = Transformacoes.matriz_rotacao(angulo_graus, pivo)
        pontos = Transformacoes._aplicar_matriz(vertices, matriz)

        return [(round(x), round(y)) for x, y in pontos]