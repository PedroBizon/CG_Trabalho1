from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from math import * 
from Ponto import Ponto
from Aresta import Aresta
from Edgetable import EdgeTable

# Constantes
TAMANHO_TELA = 800

# Variáveis Globais - mal necessário para usar as funções do OpenGL 
pontos = []
n_pontos = 0
arestas = []
n_arestas = 0

def display():
    glClear(GL_COLOR_BUFFER_BIT)
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
        
    
def main():    
    # Inicialização da tela
    glutInit()
    glutInitWindowSize(TAMANHO_TELA, TAMANHO_TELA)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutCreateWindow(b"Preenchimento de Poligonos")
    
    # Funções de Callback
    glutDisplayFunc(display)
    glutReshapeFunc(reshape(TAMANHO_TELA, TAMANHO_TELA))
    glutMouseFunc(mouse_click)
    
    # Loop de eventos
    glutMainLoop()
    
    
    return 0 


if __name__ == "__main__":
    main()