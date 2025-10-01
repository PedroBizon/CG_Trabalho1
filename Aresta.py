from Ponto import Ponto

class Aresta:
    def __init__(self, ponto1: Ponto, ponto2: Ponto):
        self.y_max = max(ponto1.y, ponto2.y)
        
        if min(ponto1.y, ponto2.y) == ponto1.y:
            self.x_min = ponto1.x
        else:
            self.x_min = ponto2.x
            
        dx = ponto1.x - ponto2.x
        dy = ponto1.y - ponto2.y
        if dx == 0 or dy == 0:
            self.inverso_m = 0
        else:
            self.inverso_m = dx / dy
            