"""
Algoritmo de recorte de linhas utilizando Cohen-Sutherland.
"""


class Recorte:
    """Implementação do algoritmo de recorte de linhas Cohen-Sutherland."""

    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    @classmethod
    def codigo(cls, x, y, xmin, ymin, xmax, ymax):
        """
        Calcula o código da região de um ponto.
        """

        codigo = cls.INSIDE

        if x < xmin:
            codigo |= cls.LEFT
        elif x > xmax:
            codigo |= cls.RIGHT

        if y < ymin:
            codigo |= cls.BOTTOM
        elif y > ymax:
            codigo |= cls.TOP

        return codigo

    @staticmethod
    def _intersecao(
        codigo,
        x1,
        y1,
        x2,
        y2,
        xmin,
        ymin,
        xmax,
        ymax,
    ):
        """
        Calcula a interseção da reta com um dos limites da janela.
        """

        if codigo & Recorte.TOP:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax

        elif codigo & Recorte.BOTTOM:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin

        elif codigo & Recorte.RIGHT:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax

        else:  # esquerda
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin

        return x, y

    @classmethod
    def recortar(
        cls,
        x1,
        y1,
        x2,
        y2,
        xmin,
        ymin,
        xmax,
        ymax,
    ):
        """
        Recorta uma linha pela janela retangular.

        Retorna:
            (x1, y1, x2, y2) se a linha permanecer visível.
            None caso esteja totalmente fora.
        """

        codigo1 = cls.codigo(x1, y1, xmin, ymin, xmax, ymax)
        codigo2 = cls.codigo(x2, y2, xmin, ymin, xmax, ymax)

        while True:

            # Linha completamente dentro
            if codigo1 == cls.INSIDE and codigo2 == cls.INSIDE:
                return (
                    round(x1),
                    round(y1),
                    round(x2),
                    round(y2),
                )

            # Linha completamente fora
            if codigo1 & codigo2:
                return None

            codigo = codigo1 if codigo1 != cls.INSIDE else codigo2

            x, y = cls._intersecao(
                codigo,
                x1,
                y1,
                x2,
                y2,
                xmin,
                ymin,
                xmax,
                ymax,
            )

            if codigo == codigo1:
                x1, y1 = x, y
                codigo1 = cls.codigo(
                    x1,
                    y1,
                    xmin,
                    ymin,
                    xmax,
                    ymax,
                )
            else:
                x2, y2 = x, y
                codigo2 = cls.codigo(
                    x2,
                    y2,
                    xmin,
                    ymin,
                    xmax,
                    ymax,
                )