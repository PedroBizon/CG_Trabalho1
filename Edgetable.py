class EdgeTable:
    def __init__(self, n_arestas: int, TAMANHO_TELA):
        ''' Inicializa EdgeTables, que podem ser tanto ETs quanto AETs'''
        self.n_arestas = n_arestas
        self.linhas_de_varredura = []
        
        for i in range(TAMANHO_TELA):
            self.linhas_de_varredura.append([])
            
    def preencher_ET(self, arestas): 
        ''' Preenche uma ET a prtir de uma lista de arestas '''   
        
        # Ordena arestas em y crescente e x crescente caso empate
        arestas_ordenadas = sorted(arestas, key = lambda aresta : (aresta.y_min, aresta.x_min))
        
        
        # Sempre que o indice i for igual a y_min, aquele é o local da aresta
        i = 0
        while(arestas_ordenadas):
            
            if(arestas_ordenadas[0].y_min == i):
                self.linhas_de_varredura[i].append(arestas_ordenadas[0])
                arestas_ordenadas.pop(0)
                
            else:
                i += 1 
        print('Terminei de preencher a ET')
        print(self.linhas_de_varredura)
        
        for j in range(600):
            if self.linhas_de_varredura[j] != []:
                print(j)  
            
            