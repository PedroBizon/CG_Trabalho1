from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GLUT as GLUT 
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
CORES_POLIGONO = [VERMELHO, VERDE, AZUL, BRANCO, PRETO]
CORES_FUNDO = [BRANCO, PRETO, (0.5, 0.5, 0.5), (0.1, 0.1, 0.3)]

# Botões
LARGURA_BOTAO = 120
ALTURA_BOTAO = 30
MARGEM_SUPERIOR = 20
MARGEM_ESQUERDA = 20

# Variáveis Globais de Estado
pontos = []
n_pontos = 0
coletando_pontos = True

arestas = []
n_arestas = 0

indice_cor_poligono = 0
indice_cor_fundo = 0

### ADICIONADO: Variáveis de controle para o ciclo de renderização
poligono_pronto_para_preencher = False

def desenhar_texto(texto, x, y):
    glWindowPos2f(x, y)
    for char in texto:
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord(char))

def criar_arestas():
    global pontos, n_pontos, arestas, n_arestas
    arestas.clear()
    if n_pontos < 3: return
    
    for i in range(n_pontos):
        p1 = pontos[i]
        p2 = pontos[(i + 1) % n_pontos]
        nova_aresta = Aresta(p1, p2)
        if nova_aresta.inverso_m != 0.0: 
            arestas.append(nova_aresta)
    n_arestas = len(arestas)

def desenhar_arestas(espessura: float):
    global pontos, indice_cor_poligono, CORES_POLIGONO
    if len(pontos) < 2: return
    
    cor_borda = PRETO if CORES_POLIGONO[indice_cor_poligono] != PRETO else BRANCO
    glColor3f(*cor_borda) 
    glLineWidth(espessura)
    glBegin(GL_LINES)
    for i in range(len(pontos)):
        p1 = pontos[i]
        p2 = pontos[(i + 1) % len(pontos)] 
        glVertex2f(p1.x, p1.y)
        glVertex2f(p2.x, p2.y)
    glEnd()

def desenhar_botoes():
    # --- Botão Limpar ---
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
    # --- Botão Cor Polígono ---
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
    # --- Botão Cor Fundo ---
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

def preencher_poligono_scanline(et: EdgeTable):
    AET = []
    y_start = 0
    for i, linha in enumerate(et.linhas_de_varredura):
        if linha:
            y_start = i 
            break
    
    y = y_start
    cor_preenchimento = CORES_POLIGONO[indice_cor_poligono]
    
    # O laço só precisa continuar enquanto houver arestas na ET ou AET
    while AET or any(et.linhas_de_varredura[y:] if y < TAMANHO_TELA else []):
        if y >= TAMANHO_TELA: break # Segurança

        # 1. Mover da ET para a AET
        if y < len(et.linhas_de_varredura) and et.linhas_de_varredura[y]:
            for aresta in et.linhas_de_varredura[y]:
                # IMPORTANTE: Reseta o current_x para o valor inicial da aresta
                aresta.current_x = aresta.x_min
                AET.append(aresta)
        
        AET.sort(key=lambda a: a.current_x)

        # 2. Desenhar os spans da scanline atual
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

        # 3. Remover arestas que terminam na linha atual
        AET = [aresta for aresta in AET if int(round(aresta.y_max)) > y]

        # 4. Incrementar y e atualizar x para a PRÓXIMA linha
        y += 1
        for aresta in AET:
            aresta.current_x += aresta.inverso_m
    
    # Não precisa de glutPostRedisplay aqui, pois já está no loop de display

def display():
    global coletando_pontos, poligono_pronto_para_preencher, arestas
    
    glClear(GL_COLOR_BUFFER_BIT)
    
    desenhar_botoes()
    
    ### ALTERADO: Lógica de desenho
    # 1. Se o polígono estiver pronto, PREENCHE PRIMEIRO
    if poligono_pronto_para_preencher:
        # Recria a ET a cada frame para garantir que o estado (current_x) está limpo
        et_para_desenho = EdgeTable(len(arestas), TAMANHO_TELA)
        et_para_desenho.preencher_ET(arestas)
        preencher_poligono_scanline(et_para_desenho)
    
    # 2. Desenha os pontos (para feedback visual durante a coleta)
    cor_ponto = BRANCO if CORES_FUNDO[indice_cor_fundo] == PRETO else PRETO
    glColor3f(*cor_ponto) 
    glPointSize(5.0) 
    glBegin(GL_POINTS)
    for p in pontos:
        glVertex2f(p.x, p.y) 
    glEnd()
    
    # 3. Desenha a borda do polígono POR CIMA do preenchimento
    if not coletando_pontos:
        desenhar_arestas(3.0)
    
    glFlush()
    
def reshape(largura: int, altura: int):
    glViewport(0, 0, largura, altura)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, largura, 0, altura)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def mouse_click(botao, estado, x, y):
    global pontos, n_pontos, coletando_pontos, arestas, n_arestas, indice_cor_poligono, indice_cor_fundo
    ### ADICIONADO: Acesso à nova flag
    global poligono_pronto_para_preencher
    
    y_real = TAMANHO_TELA - y
    
    if botao == GLUT.GLUT_LEFT_BUTTON and estado == GLUT.GLUT_DOWN:
        # --- LÓGICA DE BOTÕES ---
        x_limpar = MARGEM_ESQUERDA; y_limpar = TAMANHO_TELA - MARGEM_SUPERIOR - ALTURA_BOTAO
        x_cor = MARGEM_ESQUERDA + LARGURA_BOTAO + 20; y_cor = y_limpar
        x_fundo = x_cor + LARGURA_BOTAO + 20; y_fundo = y_limpar
        
        # Botão LIMPAR
        if (x_limpar <= x <= x_limpar + LARGURA_BOTAO and y_limpar <= y_real <= y_limpar + ALTURA_BOTAO):
            pontos.clear(); arestas.clear()
            n_pontos = 0; n_arestas = 0
            coletando_pontos = True
            poligono_pronto_para_preencher = False ### ADICIONADO: Reseta a flag
            print("--- Tela Limpa. Coleta Reiniciada. ---")
            GLUT.glutPostRedisplay()
            return
        
        # Botão MUDAR COR
        if (x_cor <= x <= x_cor + LARGURA_BOTAO and y_cor <= y_real <= y_cor + ALTURA_BOTAO):
            indice_cor_poligono = (indice_cor_poligono + 1) % len(CORES_POLIGONO)
            print(f"--- Cor do Polígono Alterada para: {CORES_POLIGONO[indice_cor_poligono]} ---")
            # Apenas solicita um redesenho, o display loop fará o resto com a nova cor
            GLUT.glutPostRedisplay()
            return
        
        # Botão MUDAR FUNDO
        if (x_fundo <= x <= x_fundo + LARGURA_BOTAO and y_fundo <= y_real <= y_fundo + ALTURA_BOTAO):
            indice_cor_fundo = (indice_cor_fundo + 1) % len(CORES_FUNDO)
            cor = CORES_FUNDO[indice_cor_fundo]
            glClearColor(cor[0], cor[1], cor[2], 1.0)
            print(f"--- Cor de Fundo Alterada para: {cor} ---")
            GLUT.glutPostRedisplay()
            return
            
        # --- LÓGICA DE COLETA DE PONTOS ---
        if coletando_pontos:
            pontos.append(Ponto(x, y_real))
            n_pontos += 1
            print(f'Ponto {n_pontos}: ({x}, {y_real})')
            GLUT.glutPostRedisplay()
    
    if botao == GLUT.GLUT_RIGHT_BUTTON and estado == GLUT.GLUT_DOWN:
        if coletando_pontos and n_pontos >= 3:
            coletando_pontos = False
            print("Fim da coleta de pontos. Polígono pronto para preenchimento.")
            
            ### ALTERADO: Lógica de finalização do polígono
            # Apenas prepara os dados. Não desenha nada diretamente.
            criar_arestas()
            poligono_pronto_para_preencher = True # SINALIZA para o display() desenhar
            
            GLUT.glutPostRedisplay() # Solicita o redesenho que fará o preenchimento

        elif n_pontos < 3:
            print("ERRO: Mínimo de 3 pontos necessários.")
        else:
            print("Polígono já finalizado. Limpe a tela para criar um novo.")

def main():
    GLUT.glutInit()
    GLUT.glutInitWindowSize(TAMANHO_TELA, TAMANHO_TELA)
    GLUT.glutInitDisplayMode(GLUT.GLUT_SINGLE | GLUT.GLUT_RGBA)
    GLUT.glutCreateWindow(b"Preenchimento de Poligonos - Scan-Line (Corrigido)")
    
    cor_inicial = CORES_FUNDO[indice_cor_fundo]
    glClearColor(cor_inicial[0], cor_inicial[1], cor_inicial[2], 1.0)
    
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutMouseFunc(mouse_click)
    
    GLUT.glutMainLoop()

if __name__ == "__main__":
    main()