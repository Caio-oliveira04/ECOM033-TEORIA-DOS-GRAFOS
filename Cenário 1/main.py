import os
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

CAMINHO_GRAFO = os.path.join(os.path.dirname(__file__), 'graph1.txt')

def ler_grafo():
    with open(CAMINHO_GRAFO, 'r') as f:
        linhas = f.readlines()
        num_vertices, num_arestas = map(int, linhas[0].strip().split())
        return num_vertices, num_arestas, [list(map(int, linha.strip().split())) for linha in linhas[1:]]

def matriz_de_valores(grafo):
    num_vertices, num_arestas, arestas = grafo

    matriz = [[float('inf')] * (num_vertices + 1) for _ in range(num_vertices + 1)]

    for i in range(1, num_vertices + 1):
        matriz[i][i] = 0

    for v, w, custo in arestas:
        matriz[v][w] = custo
        matriz[w][v] = custo  

    return matriz

# def matriz_de_roteamento(D):
#     num_vertices = len(D) - 1
#     R = [[None] * (num_vertices + 1) for _ in range(num_vertices + 1)]

#     for i in range(1, num_vertices + 1):
#         for j in range(1, num_vertices + 1):
#             if D[i][j] != float('inf') and i != j:
#                 R[i][j] = j

#     return R

def visualizar_grafo(grafo):
    _, _, arestas = grafo
    G = nx.Graph()
    for v, w, custo in arestas:
        G.add_edge(v, w, weight=custo)

    pos = nx.circular_layout(G)  # super rápido

    nx.draw(G, pos, with_labels=True, node_size=700,
            node_color="skyblue", font_weight="bold", edge_color="gray")
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Visualização do Grafo")
    plt.show()

def visualizar_matriz(matriz):
    matriz = np.array(matriz)
    fig, ax = plt.subplots()
    im = ax.imshow(matriz[1:, 1:], cmap="Blues")  
    num_vertices = len(matriz) - 1
    for i in range(num_vertices):
        for j in range(num_vertices):
            valor = matriz[i+1][j+1]
            texto = "∞" if valor == float("inf") else str(valor)
            ax.text(j, i, texto, ha="center", va="center", color="black")

    ax.set_xticks(range(num_vertices))
    ax.set_yticks(range(num_vertices))
    ax.set_xticklabels(range(1, num_vertices+1))
    ax.set_yticklabels(range(1, num_vertices+1))
    ax.set_xlabel("Vértices")
    ax.set_ylabel("Vértices")
    plt.title("Matriz de Adjacência (Pesos)")
    plt.colorbar(im)
    plt.show()

if __name__ == "__main__":
    grafo = ler_grafo()
    D = matriz_de_valores(grafo)
    #R = matriz_de_roteamento(D) 
    visualizar_grafo(grafo)
    visualizar_matriz(D)
