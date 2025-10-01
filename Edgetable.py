# EdgeTable.py (CORRIGIDO)
from Aresta import Aresta

class EdgeTable:
    def __init__(self, n_arestas: int, TAMANHO_TELA):
        ''' Inicializa a Edge Table (ET).'''
        self.n_arestas = n_arestas
        # Cria uma lista de buckets, um para cada linha de varredura
        self.linhas_de_varredura = [[] for _ in range(TAMANHO_TELA)]
            
    def preencher_ET(self, arestas): 
        ''' Preenche a ET a partir de uma lista de arestas '''
        
        # Itera sobre cada aresta e a insere no cesto correto
        for aresta in arestas:
            # Pega o y_min da aresta, arredonda e converte para inteiro para usá-lo como índice do bucket
            indice_y = int(round(aresta.y_min))
            
            # Garante que o índice está dentro dos limites da tela
            if 0 <= indice_y < len(self.linhas_de_varredura):
                self.linhas_de_varredura[indice_y].append(aresta)
        
        # Ordena as arestas dentro de cada cesto pelo x_min
        for i in range(len(self.linhas_de_varredura)):
            if self.linhas_de_varredura[i]:
                self.linhas_de_varredura[i].sort(key=lambda a: (a.x_min, a.inverso_m))