# Preenchimento de Polígonos com Coerência de Arestas

## Descrição

Este projeto é uma implementação do algoritmo de preenchimento de polígonos utilizando a coerência de arestas, desenvolvido para a disciplina de Computação Gráfica. O sistema utiliza as estruturas de dados **Tabela de Arestas (ET)** e **Tabela de Arestas Ativas (AET)** para preencher de forma eficiente polígonos 2D, tanto simples quanto complexos.

A interface gráfica foi construída com Python e a biblioteca PyOpenGL, permitindo que o usuário desenhe polígonos de forma interativa através de cliques do mouse e personalize cores em tempo real.

## Funcionalidades

-   **Desenho Interativo**: Crie vértices de polígonos com cliques do botão esquerdo do mouse.
-   **Finalização de Polígono**: Feche e preencha o polígono com um clique do botão direito.
-   **Algoritmo Scan-Line**: Preenchimento eficiente baseado na coerência de arestas (ET/AET).
-   **Mudança de Cor de Preenchimento**: Alterne entre as cores de preenchimento predefinidas (Vermelho, Verde, Azul, Branco).
-   **Mudança de Cor de Fundo**: Alterne entre diferentes cores para o fundo da tela.
-   **Limpar Tela**: Apague o polígono atual e comece a desenhar um novo.
-   **Contorno Ajustável**: As bordas do polígono são renderizadas com espessura para melhor visualização.

## Tecnologias Utilizadas

-   **Python 3**
-   **PyOpenGL**: Binding da API gráfica OpenGL para Python.
-   **GLUT (OpenGL Utility Toolkit)**: Para gerenciamento de janelas e eventos de interface.

## Instalação e Setup

Siga os passos abaixo para configurar o ambiente e executar o projeto.

#### 1. Pré-requisitos
-   Python 3.8 ou superior
-   `pip` (gerenciador de pacotes do Python)

#### 2. Clone o Repositório
```bash
git clone https://[URL_DO_SEU_REPOSITORIO].git
cd [NOME_DO_DIRETORIO]
```

#### 3. Instale as Dependências
As bibliotecas necessárias podem ser instaladas via `pip`:
```bash
pip install PyOpenGL PyOpenGL-accelerate
```

#### 4. Configuração para WSL (Windows Subsystem for Linux)
Se você estiver executando o projeto em um ambiente WSL com interface gráfica, pode ser necessário especificar a plataforma gráfica a ser utilizada. Exporte as seguintes variáveis de ambiente no seu terminal antes de executar o programa:

```bash
export DISPLAY=:0
export PYOPENGL_PLATFORM=glx
```
**Dica**: Para tornar essa configuração permanente, adicione os comandos acima ao final do seu arquivo de configuração do shell (ex: `~/.bashrc` ou `~/.zshrc`) e reinicie o terminal.

## Como Executar

O projeto inclui um `Makefile` para simplificar a execução.

**Para executar usando o Makefile:**
```bash
make run
```

**Para executar diretamente com Python:**
```bash
python3 main.py
```

## Como Usar o Sistema

1.  **Desenhar o Polígono**: Clique com o **botão esquerdo** do mouse na tela para adicionar vértices. Você precisa de no mínimo 3 pontos.
2.  **Preencher o Polígono**: Clique com o **botão direito** do mouse em qualquer lugar para finalizar a criação de vértices. O polígono será fechado e preenchido automaticamente.
3.  **Botões de Ação**:
    -   **Limpar Tela**: Reseta a aplicação, permitindo o desenho de um novo polígono.
    -   **Mudar Cor**: Cicla entre as cores de preenchimento disponíveis para o polígono.
    -   **Mudar Fundo**: Cicla entre as cores de fundo da janela.

## Estrutura do Projeto
```
.
├── Aresta.py         # Define a classe Aresta e seus atributos (y_min, y_max, x_min, 1/m)
├── Edgetable.py      # Define a classe EdgeTable (ET)
├── Makefile          # Simplifica a execução do programa
├── Ponto.py          # Define a classe Ponto (coordenadas x, y)
├── main.py           # Arquivo principal com a lógica do programa, callbacks e renderização
└── Readme.md         # Este arquivo
```

## Autor
-   Pedro Bizon Dania
