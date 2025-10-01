class EdgeTable:
    def __init__(self, n_arestas: int, TAMANHO_TELA):
        ''' Inicializa EdgeTables, que podem ser tanto ETs quanto AETs'''
        self.n_arestas = n_arestas
        self.linhas_de_varredura = []
        
        for i in range(TAMANHO_TELA):
            self.linhas_de_varredura.append([])
            
    def preencher_ET(self, arestas): 
        ''' Preenche uma ET a partir de uma lista de arestas '''
        
        # Ordena arestas em y_min crescente e x_min crescente caso empate
        arestas_ordenadas = sorted(arestas, key=lambda aresta: (aresta.y_min, aresta.x_min))
        
        # Itera por todas as linhas de varredura possíveis
        for i in range(len(self.linhas_de_varredura)):
            # Processa todas as arestas que começam na linha de varredura atual (i)
            while arestas_ordenadas and arestas_ordenadas[0].y_min == i:
                
                aresta = arestas_ordenadas.pop(0)
                
                # Adiciona a aresta à lista correspondente à linha de varredura 'i'
                self.linhas_de_varredura[i].append(aresta)
            
            # Se a lista de arestas a processar estiver vazia, podemos parar
            if not arestas_ordenadas:
                break  
            
            