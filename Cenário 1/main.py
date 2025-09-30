import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import networkx as nx
import numpy as np

CAMINHO_GRAFO = os.path.join(os.path.dirname(__file__), 'graph1.txt')


class Grafo:

    def __init__(self, caminho_arquivo):
        self.num_vertices = 0
        self.num_arestas = 0
        self.arestas = []
        self.matriz = []

        self._ler_grafo(caminho_arquivo)
        self._gerar_matriz_de_valores()

    def _ler_grafo(self, caminho):
        """Lê os dados do grafo a partir de um arquivo."""
        with open(caminho, 'r') as f:
            linhas = f.readlines()
            self.num_vertices, self.num_arestas = map(int, linhas[0].strip().split())
            self.arestas = [list(map(int, linha.strip().split())) for linha in linhas[1:]]

    def _gerar_matriz_de_valores(self):
        """Gera a matriz de adjacência com pesos."""
        n = self.num_vertices
        self.matriz = [[float('inf')] * (n + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            self.matriz[i][i] = 0

        for v, w, peso in self.arestas:
            self.matriz[v][w] = peso
            self.matriz[w][v] = peso  

    def gerar_matriz_de_roteamento(self):
        """Cria e retorna a matriz de roteamento inicial para o algoritmo de Floyd-Warshall."""
        n = self.num_vertices
        M = [[0] * (n + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            M[i][i] = i

        for v, w, _ in self.arestas:
            M[v][w] = w
            M[w][v] = v

        return M

    def floyd_warshall(self, D=None, M=None):
        """Executa o algoritmo de Floyd-Warshall."""
        if D is None:
            D = self._copiar_matriz(self.matriz)
        if M is None:
            M = self.gerar_matriz_de_roteamento()

        n = self.num_vertices
        for k in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if D[i][k] + D[k][j] < D[i][j]:
                        D[i][j] = D[i][k] + D[k][j]
                        M[i][j] = M[i][k]

        return D, M

    def _copiar_matriz(self, matriz):
        """Retorna uma cópia profunda de uma matriz."""
        return [linha[:] for linha in matriz]

    def encontrar_vertice_central(self):
        """Encontra o vértice central do grafo (menor soma das distâncias mínimas)."""
        D, _ = self.floyd_warshall()
        n = self.num_vertices

        menor_soma = float('inf')
        vertice_central = -1

        for i in range(1, n + 1):
            soma = sum(D[i][j] for j in range(1, n + 1) if i != j and D[i][j] != float('inf'))
            if soma < menor_soma:
                menor_soma = soma
                vertice_central = i

        return vertice_central, menor_soma

    def obter_distancias_do_central(self, vertice_central):
        """Retorna o vetor de distâncias do vértice central para os demais."""
        D, _ = self.floyd_warshall()
        return D[vertice_central][1:] 

    def obter_vertice_mais_distante(self, vertice_central):
        """Retorna o vértice mais distante do central e a distância."""
        D, _ = self.floyd_warshall()
        n = self.num_vertices
        max_dist = -1
        vertice_distante = -1

        for j in range(1, n + 1):
            if j != vertice_central and D[vertice_central][j] < float("inf"):
                if D[vertice_central][j] > max_dist:
                    max_dist = D[vertice_central][j]
                    vertice_distante = j

        return vertice_distante, max_dist

    def obter_matriz_todos(self):
        """Retorna a matriz de distâncias mínimas (todos os pares)."""
        D, _ = self.floyd_warshall()
        return D


class Visualizador:
    """Classe para visualização de grafos e matrizes."""

    def __init__(self, arestas=None, matriz=None):
        self.arestas = arestas
        self.matriz = matriz

    def exibir_grafo(self, direcionado=False):
        """Exibe o grafo com as arestas e seus pesos."""
        if not self.arestas:
            print("Nenhuma aresta fornecida para visualização do grafo.")
            return

        G = nx.DiGraph() if direcionado else nx.Graph()

        for v, w, peso in self.arestas:
            G.add_edge(v, w, weight=peso)

        pos = nx.circular_layout(G)

        nx.draw(G, pos, with_labels=True, node_size=700,
                node_color="skyblue", font_weight="bold", edge_color="gray", arrows=direcionado)

        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        titulo = "Grafo Direcionado" if direcionado else "Grafo Não Direcionado"
        plt.title(titulo)
        plt.show()

    def exibir_matriz(self):
        """Exibe a matriz de adjacência com coloração e pesos."""
        if not self.matriz:
            print("Nenhuma matriz fornecida para visualização.")
            return

        matriz = np.array(self.matriz)
        n = len(matriz) - 1

        color_matrix = np.ones((n, n))
        for i in range(n):
            if matriz[i + 1][i + 1] == 0:
                color_matrix[i, i] = 0

        fig, ax = plt.subplots()
        cmap = ListedColormap(["#1976d2", "#ffffff"])
        ax.imshow(color_matrix, cmap=cmap, vmin=0, vmax=1)

        for i in range(n):
            for j in range(n):
                valor = matriz[i + 1][j + 1]
                texto = "∞" if valor == float("inf") else str(int(valor))
                ax.text(j, i, texto, ha="center", va="center", color="black", fontsize=8)

        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(range(1, n + 1))
        ax.set_yticklabels(range(1, n + 1))

        plt.title("Matriz de Adjacência (Pesos)")
        plt.xlabel("Destino")
        plt.ylabel("Origem")
        plt.show()


if __name__ == "__main__":
    grafo = Grafo(CAMINHO_GRAFO)
    # visualizador = Visualizador(arestas=grafo.arestas, matriz=grafo.matriz)

    # visualizador.exibir_grafo()
    # visualizador.exibir_matriz()

    vertice, soma = grafo.encontrar_vertice_central()
    print(f"\n Vértice central escolhido: {vertice} (Soma das distâncias: {soma})")

    distancias = grafo.obter_distancias_do_central(vertice)
    print(f" Vetor de distâncias do vértice central {vertice}: {distancias}")

    v_dist, dist_max = grafo.obter_vertice_mais_distante(vertice)
    print(f" Vértice mais distante do central: {v_dist} (Distância = {dist_max})")

    matriz = grafo.obter_matriz_todos()
    print("\n Matriz de distâncias mínimas entre todos os pares:")
    for i in range(1, grafo.num_vertices + 1):
        linha = [("∞" if matriz[i][j] == float("inf") else int(matriz[i][j]))
                 for j in range(1, grafo.num_vertices + 1)]
        print(f"{i}: {linha}")
