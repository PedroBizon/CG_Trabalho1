from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from math import * 
from Ponto import Ponto
from Aresta import Aresta
from Edgetable import EdgeTable

# Constantes
TAMANHO_TELA = 600
BRANCO = (1.0, 1.0, 1.0)
PRETO = (0.0, 0.0, 0.0) 
VERMELHO = (1.0, 0.0, 0.0)
VERDE = (0.0, 1.0, 0.0)
AZUL = (0.0, 0.0, 1.0)
#AMARELO = 

# Variáveis Globais - mal necessário para usar as funções do OpenGL 
pontos = []
n_pontos = 0
coletando_pontos = True

arestas = []
n_arestas = 0


# Funções:
# ... (após mouse_click ou onde preferir) ...

def desenhar_arestas(espessura):
    ''' Desenha as arestas do polígono usando GL_LINES. '''
    global pontos
    
    if len(pontos) < 2:
        return
    
    glColor3f(*BRANCO) # Usa VERMELHO para destacar o polígono
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
    ''' Função de callback para eventos de clique de mouse '''
    global pontos
    global n_pontos
    global coletando_pontos
    global arestas
    global n_arestas
    
    if coletando_pontos:
        
        y_real = TAMANHO_TELA - y
        
        if botao == GLUT_LEFT_BUTTON and estado == GLUT_DOWN:
            ponto = Ponto(x, y_real)
            pontos.append(ponto)
            n_pontos += 1
            
            print(f'Ponto {len(pontos)}: ({pontos[-1].x}, {pontos[-1].y})')
        
        
        if botao == GLUT_RIGHT_BUTTON and estado == GLUT_DOWN:
            print("Fim da coleta de pontos")
            print("Lista dos pontos: ")
            for i in range(len(pontos)):
                print(f'Ponto {i+1}: ({pontos[i].x}, {pontos[i].y})')
                
            print(n_pontos) 
            coletando_pontos = False
            
            
            # Precisamos lembrar de verificar se temos pontos suficientes para desenhar, acho que em outro local seria melhor
            # Criar arestas
            criar_arestas()
            
            # Inicializar ET e AET
            et = EdgeTable(n_arestas, TAMANHO_TELA)
            aet = EdgeTable(n_arestas, TAMANHO_TELA)
            
            # Preencher ET
            et.preencher_ET(arestas)
            
            # Preenchimento do polígono em si
            
            glutPostRedisplay()
        
    else:
        print("Não estou coletando pontos no momento")
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