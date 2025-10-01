# Aresta.py (CORRIGIDO)

from Ponto import Ponto

class Aresta:
    def __init__(self, ponto1: Ponto, ponto2: Ponto):
        self.ponto1 = ponto1
        self.ponto2 = ponto2
        
        # GARANTIA DE FLOAT para todos os cálculos do Scanline
        if ponto1.y > ponto2.y:
            self.y_max = float(ponto1.y)
            self.y_min = float(ponto2.y)
            self.x_min = float(ponto2.x) # x correspondente a y_min
        else:
            self.y_max = float(ponto2.y)
            self.y_min = float(ponto1.y)
            self.x_min = float(ponto1.x) # x correspondente a y_min

        # Inicializa current_x com o x do ponto de y mínimo
        self.current_x = self.x_min
            
        dx = float(ponto2.x - ponto1.x)
        dy = float(ponto2.y - ponto1.y)
        
        # Ignora arestas horizontais, que não devem ir para a ET/AET
        if dy == 0:
            self.inverso_m = 0.0
        else:
            self.inverso_m = dx / dy