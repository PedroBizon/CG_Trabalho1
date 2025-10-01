class EdgeTable:
    def __init__(self, n_arestas: int, TAMANHO_TELA):
        ''' Inicializa EdgeTables, que podem ser tanto ETs quanto AETs'''
        self.n_arestas = n_arestas
        self.linhas_de_varredura = []
        
        for i in range(TAMANHO_TELA):
            self.linhas_de_varredura = []
            
    def criar_ET(self, arestas): 
        ''' Preenche uma ET a prtir de uma lista de arestas '''   
        for aresta in arestas:
            self.linhas_de_varredura        