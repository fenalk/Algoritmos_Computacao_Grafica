"""
Módulo responsável pelas projeções de sólidos 3D em 2D: ortográfica,
oblíqua (cavalier/cabinet) e perspectiva de um ponto.

Cada função recebe uma lista de vértices 3D (x, y, z) e devolve a
lista correspondente de pontos 2D (x, y) já projetados e arredondados
para coordenadas inteiras de pixel, prontos para serem rasterizados
(por exemplo, aresta a aresta, usando o algoritmo de Bresenham).
"""

import math


class Projecoes:


    @staticmethod
    def projetar_ortografica(vertices, vista="frontal"):
        """
        Projeção ortográfica (paralela): descarta um dos três eixos,
        conforme a vista escolhida.

        - "frontal": plano XY (descarta Z)  -> vista de frente
        - "superior": plano XZ (descarta Y) -> vista de cima
        - "lateral": plano ZY (descarta X)  -> vista lateral
        """

        projetados = []

        for x, y, z in vertices:
            if vista == "superior":
                projetados.append((x, z))
            elif vista == "lateral":
                projetados.append((z, y))
            else:  # frontal
                projetados.append((x, y))

        return [(round(px), round(py)) for px, py in projetados]

    # ------------------------------------------------------------------
    # Projeção Oblíqua (cavalier / cabinet)
    # ------------------------------------------------------------------

    @staticmethod
    def projetar_obliqua(vertices, angulo_graus, fator_l):
        """
        Projeção oblíqua: X e Y permanecem inalterados; a
        profundidade (Z) é somada a X e Y na direção de um ângulo
        alpha, multiplicada por um fator de redução L:

            x' = x + L * z * cos(alpha)
            y' = y + L * z * sin(alpha)

        L = 1.0   -> projeção Cavalier (profundidade em escala real)
        L = 0.5   -> projeção Cabinet (profundidade "encolhida" pela
                     metade, resultado visualmente mais realista)
        """

        theta = math.radians(angulo_graus)
        cos_a = math.cos(theta)
        sin_a = math.sin(theta)

        projetados = []

        for x, y, z in vertices:
            xp = x + fator_l * z * cos_a
            yp = y + fator_l * z * sin_a
            projetados.append((xp, yp))

        return [(round(px), round(py)) for px, py in projetados]

    # ------------------------------------------------------------------
    # Projeção Perspectiva (um ponto de fuga, ao longo do eixo Z)
    # ------------------------------------------------------------------

    @staticmethod
    def projetar_perspectiva(vertices, distancia):
        """
        Projeção em perspectiva de um ponto: o observador (centro de
        projeção) está em (0, 0, -distancia), olhando na direção +Z; o
        plano de projeção é o plano z = 0.

            x' = x * d / (z + d)
            y' = y * d / (z + d)

        Quanto maior a distância `d`, mais "achatada" (próxima da
        ortográfica) fica a projeção; quanto menor, mais acentuado o
        efeito de perspectiva (objetos mais distantes ficam bem
        menores que os mais próximos).
        """

        projetados = []

        for x, y, z in vertices:
            denominador = z + distancia

            if denominador == 0:
                # Evita divisão por zero quando o vértice coincide
                # exatamente com o centro de projeção
                denominador = 1e-6

            xp = x * distancia / denominador
            yp = y * distancia / denominador
            projetados.append((xp, yp))

        return [(round(px), round(py)) for px, py in projetados]

    # ------------------------------------------------------------------
    # Utilitário: sólido de exemplo (cubo canônico)
    # ------------------------------------------------------------------

    @staticmethod
    def cubo_exemplo(lado=4):
        """
        Retorna (vertices, arestas) de um cubo canônico centrado na
        origem, com o comprimento de lado indicado.

        Vértices 0-3 formam a face de trás (Z negativo) e 4-7 a face
        da frente (Z positivo), cada um alinhado com o correspondente
        na outra face (vértice i está "atrás" do vértice i+4).
        """

        meio = lado / 2

        vertices = [
            (-meio, -meio, -meio),  # 0 - trás, inferior, esquerda
            (meio, -meio, -meio),   # 1 - trás, inferior, direita
            (meio, meio, -meio),    # 2 - trás, superior, direita
            (-meio, meio, -meio),   # 3 - trás, superior, esquerda
            (-meio, -meio, meio),   # 4 - frente, inferior, esquerda
            (meio, -meio, meio),    # 5 - frente, inferior, direita
            (meio, meio, meio),     # 6 - frente, superior, direita
            (-meio, meio, meio),    # 7 - frente, superior, esquerda
        ]

        arestas = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # face de trás
            (4, 5), (5, 6), (6, 7), (7, 4),  # face da frente
            (0, 4), (1, 5), (2, 6), (3, 7),  # arestas de profundidade
        ]

        return vertices, arestas