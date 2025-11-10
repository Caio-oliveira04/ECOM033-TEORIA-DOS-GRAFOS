import heapq
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon
from math import dist

class Grafo:
    def __init__(self, grafo):
        self.grafo = grafo

    @staticmethod
    def ler_mapa(caminho):
        """Lê o arquivo de mapa e retorna as posições e obstáculos"""
        with open(caminho, 'r') as f:
            linhas = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        q_start = tuple(map(float, linhas[0].split(',')))
        q_goal = tuple(map(float, linhas[1].split(',')))

        num_obs = int(linhas[2])
        idx = 3
        obstaculos = []

        for _ in range(num_obs):
            n_quinas = int(linhas[idx])
            idx += 1
            quinas = []
            for _ in range(n_quinas):
                x, y = map(float, linhas[idx].split(','))
                quinas.append((x, y))
                idx += 1
            obstaculos.append(quinas)

        return q_start, q_goal, obstaculos

    @staticmethod
    def desenhar_mapa(q_start, q_goal, obstaculos, arestas=None):
        """Desenha o mapa com obstáculos, ponto inicial e final"""
        fig, ax = plt.subplots(figsize=(7, 7))

        # Obstáculos
        for obs in obstaculos:
            x, y = zip(*obs)
            x += (x[0],)
            y += (y[0],)
            ax.fill(x, y, color="black", edgecolor="black", linewidth=1.2)
            ax.plot(x, y, 'bo', markersize=5)

        # Arestas 
        for aresta in arestas or []:
            p1, p2 = aresta
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'Orange', linewidth=2, alpha=0.6)

        # Ponto inicial e final
        ax.plot(q_start[0], q_start[1], 'go', markersize=10)
        ax.text(q_start[0] + 0.2, q_start[1], 'Start', color='green', fontsize=9)

        ax.plot(q_goal[0], q_goal[1], 'ro', markersize=10)
        ax.text(q_goal[0] + 0.2, q_goal[1], 'Goal', color='red', fontsize=9)

        ax.set_aspect('equal', adjustable='box')

        # Remover bordas e eixos
        for side in ['top', 'right', 'bottom', 'left']:
            ax.spines[side].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)

        plt.show()


class Prim:
    def __init__(self, grafo, num_vertices, start_vertex=0):
        self.grafo = grafo
        self.num_vertices = num_vertices
        self.mst = []
        self.start_vertex = start_vertex
        self.chave = [float('inf')] * num_vertices
        self.pai = [None] * num_vertices
        self.fila = []

    def prim(self):
        self.chave[self.start_vertex] = 0
        for v in range(self.num_vertices):
            heapq.heappush(self.fila, (self.chave[v], v))

        while self.fila:
            chave_u, u = heapq.heappop(self.fila)
            for p1, p2, peso in self.grafo:
                if p1 == u or p2 == u:
                    v = p2 if p1 == u else p1
                    if v in [item[1] for item in self.fila] and peso < self.chave[v]:
                        self.chave[v] = peso
                        self.pai[v] = u
                        # Atualiza a fila de prioridade
                        for index, (chave, vertice) in enumerate(self.fila):
                            if vertice == v:
                                self.fila[index] = (peso, v)
                                heapq.heapify(self.fila)

        for v in range(self.num_vertices):
            if self.pai[v] is not None:
                self.mst.append((self.pai[v], v))
        return self.mst


class BFS:
    def __init__(self, arvore, num_vertices):
        self.arvore = arvore
        self.visitado = [False] * num_vertices
        self.fila = []
        self.ordem_visita = []

    def bfs(self, start_vertex):
        self.fila.append(start_vertex)
        self.visitado[start_vertex] = True

        while self.fila:
            u = self.fila.pop(0)
            self.ordem_visita.append(u)

            for p1, p2 in self.arvore:
                if p1 == u or p2 == u:
                    v = p2 if p1 == u else p1
                    if not self.visitado[v]:
                        self.fila.append(v)
                        self.visitado[v] = True

        return self.ordem_visita


class GrafoDeVisibilidade:
    def __init__(self, q_start, q_goal, obstaculos):
        self.q_start = q_start
        self.q_goal = q_goal
        self.obstaculos = obstaculos
        self.vertices = []
        self.arestas = []
        self.mapa_indices = {}

    def gerar_vertices(self):
        """Adiciona quinas dos obstáculos + start + goal"""
        self.vertices = [self.q_start, self.q_goal]
        for obs in self.obstaculos:
            self.vertices.extend(obs)
        self.mapa_indices = {v: i for i, v in enumerate(self.vertices)}

    def eh_visivel(self, p1, p2):
        """Verifica se há linha de visada entre dois pontos"""
        linha = LineString([p1, p2])
        for obs in self.obstaculos:
            poligono = Polygon(obs)
            if linha.crosses(poligono) or linha.within(poligono):
                return False
        return True

    def gerar_grafo(self):
        """Gera arestas visíveis com pesos e índices"""
        self.gerar_vertices()
        self.arestas = []

        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                p1, p2 = self.vertices[i], self.vertices[j]
                if self.eh_visivel(p1, p2):
                    peso = dist(p1, p2)
                    self.arestas.append((i, j, peso))

        return self.arestas


if __name__ == "__main__":
    caminho = "Pratica 2/mapas/mapa.txt"
    q_start, q_goal, obstaculos = Grafo.ler_mapa(caminho)

    g_vis = GrafoDeVisibilidade(q_start, q_goal, obstaculos)
    grafo_indexado = g_vis.gerar_grafo()

    prim = Prim(grafo_indexado, num_vertices=len(g_vis.vertices), start_vertex=0)
    mst = prim.prim()

    caminho = BFS(mst, num_vertices=len(g_vis.vertices))
    ordem = caminho.bfs(start_vertex=0)

    print("Ordem de visita BFS (índices):", ordem)

    # Desenhar o mapa com a MST
    arestas_mst = [(g_vis.vertices[u], g_vis.vertices[v]) for u, v in mst]
    Grafo.desenhar_mapa(q_start, q_goal, obstaculos, arestas=arestas_mst)
