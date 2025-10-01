# Arquivo puramente para testes
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
    glutCreateWindow(b"Preenchimento de Poligonos")
    glutDisplayFunc(display)
    glutMainLoop()
    return 0 


def teste():
    entrada1 = input().split()
    entrada2 = input().split()
    
    x1 = int(entrada1[0])
    y1 = int(entrada1[1])
    ponto1 = Ponto(x1, y1)
    
    x2 = int(entrada2[0])
    y2 = int(entrada2[1])
    ponto2 = Ponto(x2, y2)
    
    print(f'\nPonto 1: ({ponto1.x}, {ponto1.y})')
    print(f'Ponto 2: ({ponto2.x}, {ponto2.y})')
    
    
    aresta = Aresta(ponto1, ponto2)
    print(f'\nAresta:\n\ty_max = {aresta.y_max};\n\tx_min = {aresta.x_min};\n\tinverso_m = {aresta.inverso_m};')
    
    return 0



if __name__ == "__main__":
    teste()