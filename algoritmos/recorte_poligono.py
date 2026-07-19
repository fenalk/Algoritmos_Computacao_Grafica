"""
Módulo responsável pelo algoritmo de recorte de polígonos (Sutherland-Hodgman).
"""


class RecortePoligonos:
    """
    Implementação do algoritmo de recorte de polígonos de Sutherland-Hodgman.

    O polígono de entrada é recortado sucessivamente contra as quatro
    bordas de uma janela retangular (esquerda, direita, baixo, cima).
    A cada etapa, o polígono resultante é recalculado a partir do
    polígono da etapa anterior, produzindo ao final o polígono
    inteiramente contido na janela de recorte.
    """

    ESQUERDA = "esquerda"
    DIREITA = "direita"
    BAIXO = "baixo"
    CIMA = "cima"

    # ------------------------------------------------------------------

    @staticmethod
    def _dentro(ponto, borda, limite):
        """
        Verifica se um ponto está do lado "interno" de uma borda da
        janela de recorte.
        """

        x, y = ponto

        if borda == RecortePoligonos.ESQUERDA:
            return x >= limite
        if borda == RecortePoligonos.DIREITA:
            return x <= limite
        if borda == RecortePoligonos.BAIXO:
            return y >= limite
        if borda == RecortePoligonos.CIMA:
            return y <= limite

        return False

    # ------------------------------------------------------------------

    @staticmethod
    def _intersecao(p1, p2, borda, limite):
        """
        Calcula o ponto de interseção do segmento p1-p2 com a reta que
        define a borda de recorte (vertical para esquerda/direita,
        horizontal para baixo/cima).
        """

        x1, y1 = p1
        x2, y2 = p2

        if borda in (RecortePoligonos.ESQUERDA, RecortePoligonos.DIREITA):
            if x2 == x1:
                return (limite, y1)
            t = (limite - x1) / (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (limite, y)

        # BAIXO ou CIMA
        if y2 == y1:
            return (x1, limite)
        t = (limite - y1) / (y2 - y1)
        x = x1 + t * (x2 - x1)
        return (x, limite)

    # ------------------------------------------------------------------

    @staticmethod
    def _recortar_borda(pontos, borda, limite):
        """
        Recorta o polígono (lista de pontos) contra uma única borda da
        janela de recorte, seguindo o algoritmo de Sutherland-Hodgman.
        """

        saida = []
        n = len(pontos)

        if n == 0:
            return saida

        for i in range(n):
            atual = pontos[i]
            anterior = pontos[i - 1]

            atual_dentro = RecortePoligonos._dentro(atual, borda, limite)
            anterior_dentro = RecortePoligonos._dentro(anterior, borda, limite)

            if atual_dentro:
                if not anterior_dentro:
                    # Entrando na região válida: guarda a interseção
                    saida.append(
                        RecortePoligonos._intersecao(anterior, atual, borda, limite)
                    )
                saida.append(atual)

            elif anterior_dentro:
                # Saindo da região válida: guarda só a interseção
                saida.append(
                    RecortePoligonos._intersecao(anterior, atual, borda, limite)
                )

        return saida

    # ------------------------------------------------------------------

    @staticmethod
    def recortar(vertices, xmin, ymin, xmax, ymax):
        """
        Recorta o polígono definido por `vertices` (lista de tuplas
        (x, y)) pela janela retangular [xmin, xmax] x [ymin, ymax].

        Retorna a lista de vértices (inteiros, arredondados) do
        polígono recortado, ou None caso o polígono fique totalmente
        fora da janela (ou degenere para menos de 3 vértices).
        """

        pontos = [(float(x), float(y)) for x, y in vertices]

        pontos = RecortePoligonos._recortar_borda(
            pontos, RecortePoligonos.ESQUERDA, xmin
        )
        pontos = RecortePoligonos._recortar_borda(
            pontos, RecortePoligonos.DIREITA, xmax
        )
        pontos = RecortePoligonos._recortar_borda(
            pontos, RecortePoligonos.BAIXO, ymin
        )
        pontos = RecortePoligonos._recortar_borda(
            pontos, RecortePoligonos.CIMA, ymax
        )

        if len(pontos) < 3:
            return None

        return [(round(x), round(y)) for x, y in pontos]