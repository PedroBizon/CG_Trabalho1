from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from math import * 
from Ponto import Ponto
from Aresta import Aresta
from Edgetable import EdgeTable

# Constantes
    # Cores
TAMANHO_TELA = 600
BRANCO = (1.0, 1.0, 1.0)
PRETO = (0.0, 0.0, 0.0) 
VERMELHO = (1.0, 0.0, 0.0)
VERDE = (0.0, 1.0, 0.0)
AZUL = (0.0, 0.0, 1.0)
CORES_POLIGONO = [BRANCO, VERMELHO, VERDE, AZUL, PRETO]


    # Botões
LARGURA_BOTAO = 120
ALTURA_BOTAO = 30
MARGEM_SUPERIOR = 20
MARGEM_ESQUERDA = 20

# Variáveis Globais - mal necessário para usar as funções do OpenGL 
pontos = []
n_pontos = 0
coletando_pontos = True

arestas = []
n_arestas = 0

indice_cor_atual = 0

# Funções:
# ... (após mouse_click ou onde preferir) ...

def desenhar_arestas(espessura):
    ''' Desenha as arestas do polígono usando GL_LINES. '''
    global pontos
    
    if len(pontos) < 2:
        return
    
    glColor3f(*CORES_POLIGONO[indice_cor_atual]) 
    glLineWidth(espessura)
    
    glBegin(GL_LINES)
    # Itera sobre os pontos, conectando cada um ao seu sucessor
    for i in range(len(pontos)):
        p1 = pontos[i]
        # Ponto 2 é o próximo, usando o operador % para fechar o polígono (conecta o último ao primeiro)
        p2 = pontos[(i + 1) % len(pontos)] 
        
        # Desenha a aresta (linha) entre p1 e p2
        glVertex2f(p1.x, p1.y)
        glVertex2f(p2.x, p2.y)
        
    glEnd()


def desenhar_botoes():
    ''' Desenha a aparência visual dos botões na tela '''
    
    # --- Botão Limpar ---
    x_limpar = MARGEM_ESQUERDA
    y_limpar = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
    
    # Desenha o retângulo do botão (ex: cor cinza claro)
    glColor3f(0.7, 0.7, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(x_limpar, y_limpar)
    glVertex2f(x_limpar + LARGURA_BOTAO, y_limpar)
    glVertex2f(x_limpar + LARGURA_BOTAO, y_limpar + ALTURA_BOTAO)
    glVertex2f(x_limpar, y_limpar + ALTURA_BOTAO)
    glEnd()
    
    # Adiciona a cor do texto (Preto)
    glColor3f(*PRETO)
    # Desenha o texto "Limpar" (Necessita de uma função auxiliar para texto)
    desenhar_texto("Limpar Tela", x_limpar + 10, y_limpar + 10)


    # --- Botão Cor ---
    x_cor = MARGEM_ESQUERDA + LARGURA_BOTAO + 20 # 20px de espaço
    y_cor = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
    
    # Desenha o retângulo do botão (ex: cor ligeiramente diferente)
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(x_cor, y_cor)
    glVertex2f(x_cor + LARGURA_BOTAO, y_cor)
    glVertex2f(x_cor + LARGURA_BOTAO, y_cor + ALTURA_BOTAO)
    glVertex2f(x_cor, y_cor + ALTURA_BOTAO)
    glEnd()

    # Adiciona a cor do texto (Preto)
    glColor3f(*PRETO)
    # Desenha o texto "Mudar Cor"
    desenhar_texto("Mudar Cor", x_cor + 10, y_cor + 10)
    
    # Restaura a cor de desenho (opcional)
    glColor3f(*PRETO) 

def desenhar_texto(texto, x, y):
    ''' Função auxiliar para desenhar texto 2D com GLUT '''
    glWindowPos2f(x, y)
    for char in texto:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

def criar_arestas():
    ''' Pega todos os pontos coletados da lista pontos e faz arestas com eles, na ordem em que estiverem.
        Além disso, une o último ponto ao primeiro. A criação das arestas é simplesmente a criação dos objetos
        Aresta que contém as informações relevantes para as Edge Tables'''
    global pontos
    global n_pontos
    global arestas
    global n_arestas
     
    for i in range(n_pontos - 1):
        nova_aresta = Aresta(pontos[i], pontos[i+1])
        arestas.append(nova_aresta)
        
    nova_aresta = Aresta(pontos[0], pontos[-1])
    arestas.append(nova_aresta)
    n_arestas = n_pontos

        
# main.py
def display():
    ''' Função principal de desenho '''
    global coletando_pontos
    
    glClear(GL_COLOR_BUFFER_BIT)
    
    desenhar_botoes()
    
    # 1. Desenha os pontos (para feedback visual)
    glColor3f(*PRETO) # Use PRETO para visualizar os pontos no fundo BRANCO
    glPointSize(5.0) 
    glBegin(GL_POINTS)
    for p in pontos:
        glVertex2f(p.x, p.y) 
    glEnd()
    
    # 2. Desenha o polígono APENAS se a coleta terminou
    if not coletando_pontos:
        desenhar_arestas(4.0) # Espessura de 4.0
    
    glFlush()
    
def reshape(largura: int, altura: int):
    ''' Função para alterar as coordenadas do OpenGL e deixar como nós estamos acostumados
        em Geometria Analítica e afins'''
        
    glViewport(0, 0, largura, altura)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluOrtho2D(0, largura, 0, altura)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    

def mouse_click(botao, estado, x, y):
    ''' Função de callback para eventos de clique de mouse e botões '''
    global pontos, n_pontos, coletando_pontos, arestas, n_arestas, indice_cor_atual
    
    y_real = TAMANHO_TELA - y
    
    if botao == GLUT_LEFT_BUTTON and estado == GLUT_DOWN:
        
        # ------------------------------------
        # 1. LÓGICA DE CLIQUE NOS BOTÕES
        # ------------------------------------
        x_limpar = MARGEM_ESQUERDA
        y_limpar = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
        x_cor = MARGEM_ESQUERDA + LARGURA_BOTAO + 20
        y_cor = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
        
        # Verifica clique no botão LIMPAR
        if (x >= x_limpar and x <= x_limpar + LARGURA_BOTAO and 
            y_real >= y_limpar and y_real <= y_limpar + ALTURA_BOTAO):
            
            # Executa a ação do botão Limpar
            pontos.clear()
            arestas.clear()
            n_pontos = 0
            n_arestas = 0
            coletando_pontos = True # Volta ao estado de coleta
            print("--- Tela Limpa. Coleta Reiniciada. ---")
            glutPostRedisplay()
            return # Sai da função para não processar como clique normal
        
        # Verifica clique no botão MUDAR COR
        if (x >= x_cor and x <= x_cor + LARGURA_BOTAO and 
            y_real >= y_cor and y_real <= y_cor + ALTURA_BOTAO):
            
            # Executa a ação do botão Mudar Cor
            indice_cor_atual = (indice_cor_atual + 1) % len(CORES_POLIGONO)
            print(f"--- Cor do Polígono Alterada para: {CORES_POLIGONO[indice_cor_atual]} ---")
            glutPostRedisplay()
            return # Sai da função para não processar como clique normal
            
        # ------------------------------------
        # 2. LÓGICA DE COLETA DE PONTOS
        # ------------------------------------
        if coletando_pontos:
            ponto = Ponto(x, y_real)
            pontos.append(ponto)
            n_pontos += 1
            
            print(f'Ponto {len(pontos)}: ({pontos[-1].x}, {pontos[-1].y})')
            glutPostRedisplay()
        
    
    # ... (o resto da lógica de botão direito e if not coletando_pontos é mantida) ...
    if botao == GLUT_RIGHT_BUTTON and estado == GLUT_DOWN:
        # Sua lógica de fim de coleta aqui:
        if coletando_pontos:
             # ... (cria arestas, inicializa ET, etc.) ...
             coletando_pontos = False
             glutPostRedisplay()
             
    elif not coletando_pontos:
        print("Não estou coletando pontos no momento (Polígono Finalizado).")
        pass
        
    
def main():    
    global coletando_pontos
    
    # Inicialização da tela
    glutInit()
    glutInitWindowSize(TAMANHO_TELA, TAMANHO_TELA)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutCreateWindow(b"Preenchimento de Poligonos")
    
    # Funções de Callback
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse_click)
    
        
    # Loop de eventos
    glutMainLoop()
    
    
    return 0 


if __name__ == "__main__":
    main()