from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 
from math import * 
from Ponto import Ponto
from Aresta import Aresta
from Edgetable import EdgeTable

TAMANHO_TELA = 800

def display():
    glClear(GL_COLOR_BUFFER_BIT)

def main():
    glutInit()
    glutInitWindowSize(TAMANHO_TELA, TAMANHO_TELA)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutCreateWindow(b"Partiu aprender")
    glutDisplayFunc(display)
    glutMainLoop()
    
    
    return 0 


# Passos do algoritmo:

# 1) Pegar pontos por cliques na tela


# 2) Transformar pontos em arestas


# 3) Inicializar ET e AET


# 4) Algoritmo para preenchimento do polígono


# 5) Interface: Mudança de cores + limpar tela


if __name__ == "__main__":
    main()