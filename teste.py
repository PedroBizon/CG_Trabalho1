# main.py (Recomentado para clareza)

# Importações necessárias da biblioteca PyOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GLUT as GLUT 
from math import * # Importação das classes auxiliares que definem as estruturas de dados
from Ponto import Ponto
from Aresta import Aresta
from Edgetable import EdgeTable

# --- Bloco de Constantes ---
# Define valores fixos para facilitar a manutenção do código.

# Dimensões da janela
TAMANHO_TELA = 600

# Paleta de cores em formato RGB (normalizado entre 0.0 e 1.0)
BRANCO = (1.0, 1.0, 1.0)
PRETO = (0.0, 0.0, 0.0) 
VERMELHO = (1.0, 0.0, 0.0)
VERDE = (0.0, 1.0, 0.0)
AZUL = (0.0, 0.0, 1.0)
CORES_POLIGONO = [VERMELHO, VERDE, AZUL, BRANCO]
CORES_FUNDO = [BRANCO, (0.5, 0.5, 0.5), (0.1, 0.1, 0.3)]

# Dimensões e posicionamento para os botões da interface
LARGURA_BOTAO = 120
ALTURA_BOTAO = 30
MARGEM_SUPERIOR = 20
MARGEM_ESQUERDA = 20

# --- Bloco de Variáveis Globais de Estado ---
# Armazenam o estado atual da aplicação.

pontos = []  # Lista para guardar os objetos Ponto clicados pelo usuário.
n_pontos = 0 # Contador de pontos.
coletando_pontos = True # Flag que controla se o programa está em modo de desenho ou finalizado.

arestas = [] # Lista que armazenará as arestas do polígono após a finalização dos cliques.
n_arestas = 0 # Contador de arestas.

# Índices para controlar a cor selecionada nas listas de cores.
indice_cor_poligono = 0
indice_cor_fundo = 0

# Flag de controle principal para o ciclo de renderização.
# Quando True, a função display() sabe que deve executar o algoritmo de preenchimento.
poligono_pronto_para_preencher = False

# --- Funções Auxiliares de Desenho ---

def desenhar_texto(texto, x, y):
    """Desenha uma string de texto na tela na posição (x, y)."""
    glWindowPos2f(x, y) # Define a posição do raster (texto) na janela.
    for char in texto:
        # Renderiza cada caractere usando uma fonte bitmap padrão do GLUT.
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord(char))

def criar_arestas():
    """Processa a lista de 'pontos' e a converte para uma lista de 'arestas'."""
    global pontos, n_pontos, arestas, n_arestas
    arestas.clear() # Limpa a lista de arestas anterior.
    if n_pontos < 3: return # Um polígono precisa de no mínimo 3 vértices.
    
    for i in range(n_pontos):
        p1 = pontos[i]
        # O operador '%' garante que o último ponto se conecte ao primeiro para fechar o polígono.
        p2 = pontos[(i + 1) % n_pontos]
        nova_aresta = Aresta(p1, p2)
        # CONDIÇÃO CRÍTICA: Arestas horizontais (dy=0) são ignoradas pelo algoritmo de scan-line.
        if nova_aresta.inverso_m != 0.0: 
            arestas.append(nova_aresta)
    n_arestas = len(arestas)

def desenhar_arestas(espessura: float):
    """Desenha as bordas (contorno) do polígono."""
    global pontos, indice_cor_poligono, CORES_POLIGONO
    if len(pontos) < 2: return
    
    # Define uma cor de borda que contraste com a cor de preenchimento.
    cor_borda = PRETO if CORES_POLIGONO[indice_cor_poligono] != PRETO else BRANCO
    glColor3f(*cor_borda) 
    glLineWidth(espessura) # Define a espessura da linha.
    
    # Inicia o modo de desenho de linhas.
    glBegin(GL_LINES)
    for i in range(len(pontos)):
        p1 = pontos[i]
        p2 = pontos[(i + 1) % len(pontos)] 
        glVertex2f(p1.x, p1.y)
        glVertex2f(p2.x, p2.y)
    glEnd() # Finaliza o modo de desenho.

def desenhar_botoes():
    """Desenha a interface gráfica com os botões."""
    # Desenho do botão "Limpar Tela"
    x_limpar = MARGEM_ESQUERDA
    y_limpar = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
    glColor3f(0.7, 0.7, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(x_limpar, y_limpar)
    glVertex2f(x_limpar + LARGURA_BOTAO, y_limpar)
    glVertex2f(x_limpar + LARGURA_BOTAO, y_limpar + ALTURA_BOTAO)
    glVertex2f(x_limpar, y_limpar + ALTURA_BOTAO)
    glEnd()
    glColor3f(*PRETO)
    desenhar_texto("Limpar Tela", x_limpar + 10, y_limpar + 10)

    # Desenho do botão "Mudar Cor"
    x_cor_poligono = MARGEM_ESQUERDA + LARGURA_BOTAO + 20 
    y_cor_poligono = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(x_cor_poligono, y_cor_poligono)
    glVertex2f(x_cor_poligono + LARGURA_BOTAO, y_cor_poligono)
    glVertex2f(x_cor_poligono + LARGURA_BOTAO, y_cor_poligono + ALTURA_BOTAO)
    glVertex2f(x_cor_poligono, y_cor_poligono + ALTURA_BOTAO)
    glEnd()
    glColor3f(*PRETO)
    desenhar_texto("Mudar Cor", x_cor_poligono + 10, y_cor_poligono + 10)

    # Desenho do botão "Mudar Fundo"
    x_fundo = x_cor_poligono + LARGURA_BOTAO + 20 
    y_fundo = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
    glColor3f(0.6, 0.9, 0.6) 
    glBegin(GL_QUADS)
    glVertex2f(x_fundo, y_fundo)
    glVertex2f(x_fundo + LARGURA_BOTAO, y_fundo)
    glVertex2f(x_fundo + LARGURA_BOTAO, y_fundo + ALTURA_BOTAO)
    glVertex2f(x_fundo, y_fundo + ALTURA_BOTAO)
    glEnd()
    glColor3f(*PRETO)
    desenhar_texto("Mudar Fundo", x_fundo + 10, y_fundo + 10)

# --- Implementação do Algoritmo de Preenchimento ---

def preencher_poligono_scanline(et: EdgeTable):
    """Executa o algoritmo de preenchimento por Scan-Line com ordem de operação corrigida."""
    AET = []
    
    y_start = 0
    for i, linha in enumerate(et.linhas_de_varredura):
        if linha:
            y_start = i 
            break
    
    y = y_start
    cor_preenchimento = CORES_POLIGONO[indice_cor_poligono]
    
    while AET or any(et.linhas_de_varredura[y:] if y < TAMANHO_TELA else []):
        if y >= TAMANHO_TELA: break

        # --- ORDEM DE OPERAÇÃO CORRIGIDA ---

        # PASSO 1 (Antigo Passo 4): Remover arestas que terminam na linha ATUAL.
        # Esta operação agora acontece ANTES de adicionar novas arestas.
        AET = [aresta for aresta in AET if int(round(aresta.y_max)) > y]

        # PASSO 2 (Antigo Passo 1): Adicionar arestas da ET que começam na linha ATUAL.
        if y < len(et.linhas_de_varredura) and et.linhas_de_varredura[y]:
            for aresta in et.linhas_de_varredura[y]:
                aresta.current_x = aresta.x_min
                AET.append(aresta)
        
        # PASSO 3: Ordenar a AET.
        AET.sort(key=lambda a: (a.current_x, a.inverso_m))

        # PASSO 4: Desenhar os spans da scanline atual.
        if len(AET) >= 2:
            glColor3f(*cor_preenchimento)
            glBegin(GL_LINES) 
            for i in range(0, len(AET) - 1, 2):
                x_inicio = int(round(AET[i].current_x))
                x_fim = int(round(AET[i+1].current_x))
                if x_inicio < x_fim:
                    glVertex2f(x_inicio, y)
                    glVertex2f(x_fim, y)
            glEnd()

        # PASSO 5: Atualizar para a próxima scanline.
        y += 1
        for aresta in AET:
            aresta.current_x += aresta.inverso_m


def display():
    """Função principal de desenho, chamada repetidamente pelo GLUT."""
    global coletando_pontos, poligono_pronto_para_preencher, arestas
    
    # 1. Limpa a tela a cada quadro para redesenhar a cena.
    glClear(GL_COLOR_BUFFER_BIT)
    
    # 2. Desenha os elementos estáticos da interface.
    desenhar_botoes()
    
    # 3. Lógica de renderização condicional do polígono.
    # Se o polígono foi finalizado, ele deve ser preenchido.
    if poligono_pronto_para_preencher:
        # A ET é recriada a cada quadro. Isso é crucial porque o algoritmo
        # altera o estado das arestas (current_x) e precisa de um estado "limpo" a cada vez.
        et_para_desenho = EdgeTable(len(arestas), TAMANHO_TELA)
        et_para_desenho.preencher_ET(arestas)
        # Chama o preenchimento, que será desenhado PRIMEIRO.
        preencher_poligono_scanline(et_para_desenho)
    
    # 4. Desenha os pontos clicados pelo usuário para dar feedback visual.
    cor_ponto = BRANCO if CORES_FUNDO[indice_cor_fundo] == PRETO else PRETO
    glColor3f(*cor_ponto) 
    glPointSize(5.0) 
    glBegin(GL_POINTS)
    for p in pontos:
        glVertex2f(p.x, p.y) 
    glEnd()
    
    # 5. Desenha a borda do polígono por último, para que apareça sobre o preenchimento.
    if not coletando_pontos:
        desenhar_arestas(3.0)
    
    # 6. Força a execução de todos os comandos OpenGL pendentes.
    glFlush()
    
def reshape(largura: int, altura: int):
    """Função chamada quando a janela é redimensionada."""
    glViewport(0, 0, largura, altura) # Define a área de desenho para a janela inteira.
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Define um sistema de coordenadas 2D que mapeia pixels para coordenadas.
    gluOrtho2D(0, largura, 0, altura)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def mouse_click(botao, estado, x, y):
    """Função chamada quando um botão do mouse é pressionado ou solto."""
    global pontos, n_pontos, coletando_pontos, arestas, n_arestas, indice_cor_poligono, indice_cor_fundo
    global poligono_pronto_para_preencher
    
    # Converte a coordenada y do mouse (origem no topo) para a do OpenGL (origem na base).
    y_real = TAMANHO_TELA - y
    
    # Lógica para o clique do botão esquerdo.
    if botao == GLUT.GLUT_LEFT_BUTTON and estado == GLUT.GLUT_DOWN:
        x_limpar = MARGEM_ESQUERDA; y_limpar = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
        x_cor = MARGEM_ESQUERDA + LARGURA_BOTAO + 20; y_cor = y_limpar
        x_fundo = x_cor + LARGURA_BOTAO + 20; y_fundo = y_limpar
        
        # Verifica se o clique foi no botão "Limpar".
        if (x_limpar <= x <= x_limpar + LARGURA_BOTAO and y_limpar <= y_real <= y_limpar + ALTURA_BOTAO):
            # Reseta todas as variáveis de estado para o valor inicial.
            pontos.clear(); arestas.clear()
            n_pontos = 0; n_arestas = 0
            coletando_pontos = True
            poligono_pronto_para_preencher = False
            print("--- Tela Limpa. Coleta Reiniciada. ---")
            GLUT.glutPostRedisplay() 
            return
        
        # Verifica se o clique foi no botão "Mudar Cor".
        if (x_cor <= x <= x_cor + LARGURA_BOTAO and y_cor <= y_real <= y_cor + ALTURA_BOTAO):
            indice_cor_poligono = (indice_cor_poligono + 1) % len(CORES_POLIGONO)
            print(f"--- Cor do Polígono Alterada para: {CORES_POLIGONO[indice_cor_poligono]} ---")
            GLUT.glutPostRedisplay()
            return
        
        # Verifica se o clique foi no botão "Mudar Fundo".
        if (x_fundo <= x <= x_fundo + LARGURA_BOTAO and y_fundo <= y_real <= y_fundo + ALTURA_BOTAO):
            indice_cor_fundo = (indice_cor_fundo + 1) % len(CORES_FUNDO)
            cor = CORES_FUNDO[indice_cor_fundo]
            glClearColor(cor[0], cor[1], cor[2], 1.0) # Altera a cor de fundo.
            print(f"--- Cor de Fundo Alterada para: {cor} ---")
            GLUT.glutPostRedisplay()
            return
            
        # Se não clicou em nenhum botão, e está em modo de coleta, adiciona um ponto.
        if coletando_pontos:
            pontos.append(Ponto(x, y_real))
            n_pontos += 1
            print(f'Ponto {n_pontos}: ({x}, {y_real})')
            GLUT.glutPostRedisplay()
    
    # Lógica para o clique do botão direito.
    if botao == GLUT.GLUT_RIGHT_BUTTON and estado == GLUT.GLUT_DOWN:
        if coletando_pontos and n_pontos >= 3:
            # Finaliza a coleta de pontos.
            coletando_pontos = False
            print("Fim da coleta de pontos. Polígono pronto para preenchimento.")
            
            # Prepara os dados do polígono.
            criar_arestas()
            # Ativa a flag para que a função display() comece a preencher o polígono.
            poligono_pronto_para_preencher = True
            
            GLUT.glutPostRedisplay()

        elif n_pontos < 3:
            print("ERRO: Mínimo de 3 pontos necessários.")
        else:
            print("Polígono já finalizado. Limpe a tela para criar um novo.")


# --- Função Principal ---
def main():
    """Função que inicializa o GLUT e inicia o loop principal."""
    # Inicialização básica do GLUT.
    GLUT.glutInit()
    GLUT.glutInitWindowSize(TAMANHO_TELA, TAMANHO_TELA)
    GLUT.glutInitDisplayMode(GLUT.GLUT_SINGLE | GLUT.GLUT_RGBA)
    GLUT.glutCreateWindow(b"Preenchimento de Poligonos - Scan-Line (Corrigido)")
    
    # Define a cor de fundo inicial.
    cor_inicial = CORES_FUNDO[indice_cor_fundo]
    glClearColor(cor_inicial[0], cor_inicial[1], cor_inicial[2], 1.0)
    
    # Registra as funções de callback.
    GLUT.glutDisplayFunc(display)       
    GLUT.glutReshapeFunc(reshape)       
    GLUT.glutMouseFunc(mouse_click)     
    
    # Inicia o loop de eventos do GLUT.
    GLUT.glutMainLoop()

if __name__ == "__main__":
    main()