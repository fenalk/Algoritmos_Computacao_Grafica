"""
Módulo responsável pelo algoritmo de recorte de linhas (Cohen-Sutherland).
"""


class RecorteLinhas:
   

    # Códigos das regiões (outcodes)
    DENTRO = 0    # 0000
    ESQUERDA = 1  # 0001
    DIREITA = 2   # 0010
    BAIXO = 4     # 0100
    CIMA = 8      # 1000

    # ------------------------------------------------------------------

    @staticmethod
    def calcular_codigo(x, y, xmin, ymin, xmax, ymax):
        """
        Calcula o outcode de um ponto em relação à janela de recorte.
        """

        codigo = RecorteLinhas.DENTRO

        if x < xmin:
            codigo |= RecorteLinhas.ESQUERDA
        elif x > xmax:
            codigo |= RecorteLinhas.DIREITA

        if y < ymin:
            codigo |= RecorteLinhas.BAIXO
        elif y > ymax:
            codigo |= RecorteLinhas.CIMA

        return codigo

    # ------------------------------------------------------------------

    @staticmethod
    def recortar(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
        """
        Recorta o segmento de reta (x1, y1)-(x2, y2) pela janela de
        recorte [xmin, xmax] x [ymin, ymax].

        Retorna uma tupla (x1, y1, x2, y2) com as coordenadas (inteiras,
        já arredondadas) do segmento recortado, ou None caso a linha
        esteja totalmente fora da janela.
        """

        x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)

        codigo1 = RecorteLinhas.calcular_codigo(x1, y1, xmin, ymin, xmax, ymax)
        codigo2 = RecorteLinhas.calcular_codigo(x2, y2, xmin, ymin, xmax, ymax)

        aceito = False

        while True:

            if codigo1 == RecorteLinhas.DENTRO and codigo2 == RecorteLinhas.DENTRO:
                # Ambos os pontos estão dentro da janela: aceita direto
                aceito = True
                break

            elif codigo1 & codigo2 != 0:
                # Ambos compartilham uma região externa: totalmente fora
                break

            else:
                # Pelo menos um ponto está fora: calcula a interseção
                # com a borda correspondente
                x, y = 0.0, 0.0

                codigo_fora = codigo1 if codigo1 != RecorteLinhas.DENTRO else codigo2

                if codigo_fora & RecorteLinhas.CIMA:
                    x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                    y = ymax

                elif codigo_fora & RecorteLinhas.BAIXO:
                    x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                    y = ymin

                elif codigo_fora & RecorteLinhas.DIREITA:
                    y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                    x = xmax

                elif codigo_fora & RecorteLinhas.ESQUERDA:
                    y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                    x = xmin

                if codigo_fora == codigo1:
                    x1, y1 = x, y
                    codigo1 = RecorteLinhas.calcular_codigo(
                        x1, y1, xmin, ymin, xmax, ymax
                    )
                else:
                    x2, y2 = x, y
                    codigo2 = RecorteLinhas.calcular_codigo(
                        x2, y2, xmin, ymin, xmax, ymax
                    )

        if aceito:
            return (round(x1), round(y1), round(x2), round(y2))

        return None