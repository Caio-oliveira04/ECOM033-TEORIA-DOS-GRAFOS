import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import heapq
from matplotlib.animation import FuncAnimation

CAMINHO_GRAFO = os.path.join(os.path.dirname(__file__), '..', 'Descrição da atividade', 'grid_example.txt')


def ler_grid(arquivo):
    with open(arquivo, 'r') as f:
        linhas, cols = map(int, f.readline().split())
        grid = [list(f.readline().strip()) for _ in range(linhas)]
    return grid, linhas, cols


def encontrar_inicio_e_fim(grid):
    inicio = None
    fim = None
    for i, linha in enumerate(grid):
        for j, char in enumerate(linha):
            if char == 'S':
                inicio = (i, j)
            elif char == 'G':
                fim = (i, j)
    return inicio, fim


def custo(celula):
    if celula == '=':
        return 1
    if celula == '~':
        return 3
    if celula in ['S', 'G']:
        return 1
    return None  # obstáculo 


def vizinhos(pos, grid, linhas, cols):
    i, j = pos
    movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, O, L
    resultado = []

    for di, dj in movimentos:
        ni, nj = i + di, j + dj
        if 0 <= ni < linhas and 0 <= nj < cols:
            c = custo(grid[ni][nj])
            if c is not None:  # não é obstáculo
                resultado.append(((ni, nj), c))
    return resultado


def dijkstra(grid, inicio, fim, linhas, cols):
    
    V = [(i, j) for i in range(linhas) for j in range(cols) if custo(grid[i][j]) is not None]
    dist = {v: float('inf') for v in V}
    anterior = {v: None for v in V}
    dist[inicio] = 0

    A = set(V)   
    F = set()    

    while A:
        r = min(A, key=lambda x: dist[x])

        if r == fim:  
            break

        F.add(r)
        A.remove(r)

        for (viz, custo_viz) in vizinhos(r, grid, linhas, cols):
            if viz in A:  
                p = min(dist[viz], dist[r] + custo_viz)
                if p < dist[viz]:
                    dist[viz] = p
                    anterior[viz] = r

    return dist, anterior



def reconstruir_caminho(prev, inicio, fim):
    caminho = []
    atual = fim
    while atual != inicio:
        caminho.append(atual)
        atual = prev.get(atual)
        if atual is None:
            return []  # não há caminho
    caminho.append(inicio)
    caminho.reverse()
    return caminho


# def visualizar_grid(grid, inicio, fim):
#     char_map = {'.': 0, '~': 1, '#': 2, '=': 3, 'S': 4, 'G': 5}
#     cmap = ListedColormap(['#D2B48C', '#1f77b4', "#737373",
#                            '#808080', '#2ca02c', '#d62728'])

#     numeric_grid = np.array([[char_map.get(char, 0) for char in row] for row in grid])

#     fig, ax = plt.subplots(figsize=(10, 10))
#     ax.imshow(numeric_grid, cmap=cmap, interpolation='nearest')

#     if inicio:
#         ax.annotate('S', xy=(inicio[1], inicio[0]), ha='center',
#                     va='center', color='white', fontsize=12, weight='bold')
#     if fim:
#         ax.annotate('G', xy=(fim[1], fim[0]), ha='center',
#                     va='center', color='white', fontsize=12, weight='bold')

#     ax.set_xticks(np.arange(numeric_grid.shape[1]))
#     ax.set_yticks(np.arange(numeric_grid.shape[0]))
#     ax.set_xticklabels([])
#     ax.set_yticklabels([])
#     ax.tick_params(length=0)

#     ax.set_xticks(np.arange(-.5, numeric_grid.shape[1], 1), minor=True)
#     ax.set_yticks(np.arange(-.5, numeric_grid.shape[0], 1), minor=True)
#     ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)

#     plt.title("Visualização do Grid")
#     plt.show()


# def animar_caminho(grid, caminho, inicio, fim):
#     char_map = {'.': 0, '~': 1, '#': 2, '=': 3, 'S': 4, 'G': 5}
#     cmap = ListedColormap(['#D2B48C', '#1f77b4',
#                            "#737373", '#808080', '#2ca02c', '#d62728'])

#     numeric_grid = np.array([[char_map.get(char, 0) for char in row] for row in grid])

#     fig, ax = plt.subplots(figsize=(8, 8))
#     ax.imshow(numeric_grid, cmap=cmap, interpolation='nearest')

#     ax.set_xticks(np.arange(numeric_grid.shape[1]))
#     ax.set_yticks(np.arange(numeric_grid.shape[0]))
#     ax.set_xticklabels([])
#     ax.set_yticklabels([])
#     ax.tick_params(length=0)
#     ax.set_xticks(np.arange(-.5, numeric_grid.shape[1], 1), minor=True)
#     ax.set_yticks(np.arange(-.5, numeric_grid.shape[0], 1), minor=True)
#     ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)

#     # marcador da partícula
#     part, = ax.plot([], [], "o", color="yellow", markersize=12)

#     def init():
#         part.set_data([], [])
#         return part,

#     def update(frame):
#         i, j = caminho[frame]
#         part.set_data([j], [i])  # corrigido: agora passa listas
#         return part,

#     ani = FuncAnimation(fig, update, frames=len(caminho),
#                         init_func=init, blit=True, interval=500, repeat=False)
#     plt.show()


if __name__ == "__main__":
    grid, linhas, cols = ler_grid(CAMINHO_GRAFO)
    inicio, fim = encontrar_inicio_e_fim(grid)

    dist, prev = dijkstra(grid, inicio, fim, linhas, cols)
    caminho = reconstruir_caminho(prev, inicio, fim)

    if caminho:
        caminho = [(i + 1, j + 1) for i, j in caminho]
        print("Custo total:", dist[fim])
        print("Caminho:", caminho)
    else:
        print("Não existe caminho do início ao objetivo.")


    # visualizar_grid(grid, inicio, fim)

    # if caminho:
    #     animar_caminho(grid, caminho, inicio, fim)
    # else:
    #     print("Nenhum caminho encontrado para animar.")
