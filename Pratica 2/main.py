import heapq
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon
from math import dist

class Grafo:
    def __init__(self, grafo):
        self.grafo = grafo

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

    def desenhar_mapa(q_start, q_goal, obstaculos, vertices, grafo=None, mst=None, caminho_final=None):
        """
        Desenha o mapa, o Grafo de Visibilidade (grafo), a MST e o caminho final.
        O parâmetro 'vertices' é necessário para converter índices (em grafo/mst) em coordenadas.
        """
        fig, ax = plt.subplots(figsize=(7, 7))

        # Obstáculos
        for obs in obstaculos:
            x, y = zip(*obs)
            x += (x[0],)
            y += (y[0],)
            ax.fill(x, y, color="black", edgecolor="black", linewidth=1.2, alpha=0.5)
            ax.plot(x, y, 'bo', markersize=3)
        
        # Grafo de Visibilidade
        for u, v, _ in grafo or []:
            p1_coord = vertices[u] 
            p2_coord = vertices[v]
            ax.plot([p1_coord[0], p2_coord[0]], [p1_coord[1], p2_coord[1]], 'gray', linewidth=1.0, alpha=0.2, linestyle='-')

        # MST
        for aresta in mst or []:
            p1, p2 = aresta
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'orange', linewidth=2, alpha=0.7, linestyle='--')

        # Caminho Final
        if caminho_final:
            x_path, y_path = zip(*caminho_final)
            ax.plot(x_path, y_path, 'r-', linewidth=3, alpha=0.9, marker='o', markerfacecolor='Green', markeredgecolor='white', markersize=6)
            
        # Pontos Iniciais/Finais
        ax.plot(q_start[0], q_start[1], 'go', markersize=10, label='Start')
        ax.text(q_start[0] + 0.2, q_start[1], 'Start', color='green', fontsize=9)

        ax.plot(q_goal[0], q_goal[1], 'ro', markersize=10, label='Goal')
        ax.text(q_goal[0] + 0.2, q_goal[1], 'Goal', color='red', fontsize=9)

        
        ax.set_aspect('equal', adjustable='box')
        
        for side in ['top', 'right', 'bottom', 'left']: # Remover bordas e eixos
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
        """Executa o algoritmo de Prim (Versão Corrigida/Eficiente)."""
        self.chave[self.start_vertex] = 0
        heapq.heappush(self.fila, (0, self.start_vertex))
        
        na_mst = [False] * self.num_vertices 

        while self.fila:
            chave_u, u = heapq.heappop(self.fila)

            if na_mst[u]:
                continue
            
            na_mst[u] = True

            if self.pai[u] is not None:
                 self.mst.append((self.pai[u], u))

            for p1, p2, peso in self.grafo:
                
                if p1 == u:
                    v = p2
                elif p2 == u:
                    v = p1
                else:
                    continue

                if not na_mst[v] and peso < self.chave[v]:
                    self.chave[v] = peso
                    self.pai[v] = u
                    heapq.heappush(self.fila, (peso, v)) 

        return self.mst


class BFS:
    def __init__(self, arvore, num_vertices):
        self.adj = [[] for _ in range(num_vertices)]
        for u, v in arvore:
            self.adj[u].append(v)
            self.adj[v].append(u)
        self.num_vertices = num_vertices

    def encontrar_caminho(self, start_v, goal_v):
        """Encontra o caminho único entre start_v e goal_v na MST."""
        fila = [start_v]
        visitado = [False] * self.num_vertices
        pai = [None] * self.num_vertices 
        visitado[start_v] = True
        
        caminho_encontrado = False

        while fila:
            u = fila.pop(0)
            
            if u == goal_v:
                caminho_encontrado = True
                break

            for v in self.adj[u]:
                if not visitado[v]:
                    visitado[v] = True
                    pai[v] = u
                    fila.append(v)

        if not caminho_encontrado:
            return []

        caminho_vertices = []
        curr = goal_v
        while curr is not None:
            caminho_vertices.append(curr)
            curr = pai[curr]
            
        return caminho_vertices[::-1]


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
    
    def verticeMaisProximo(self, ponto):
        """Retorna o vértice (coordenada) e o índice da lista de vértices mais próximo."""
        vertice_mais_prox = None
        min_dist = float('inf')
        
        for v_coord in self.vertices:
            d = dist(ponto, v_coord)
            if d < min_dist:
                min_dist = d
                vertice_mais_prox = v_coord
                
        return vertice_mais_prox, self.mapa_indices[vertice_mais_prox]


if __name__ == "__main__":
    caminho_mapa = "Pratica 2/mapas/mapa.txt" 
    
    q_start, q_goal, obstaculos = Grafo.ler_mapa(caminho_mapa)

    g_vis = GrafoDeVisibilidade(q_start, q_goal, obstaculos)
    grafo_indexado = g_vis.gerar_grafo() 
    num_vertices = len(g_vis.vertices)

    prim = Prim(grafo_indexado, num_vertices=num_vertices, start_vertex=0)
    mst_indices = prim.prim()
    
    v_start_coord, v_start_idx = g_vis.verticeMaisProximo(q_start)
    v_goal_coord, v_goal_idx = g_vis.verticeMaisProximo(q_goal)
    
    busca_caminho = BFS(mst_indices, num_vertices=num_vertices)
    caminho_indices = busca_caminho.encontrar_caminho(v_start_idx, v_goal_idx)

    caminho_final_coords = [g_vis.vertices[i] for i in caminho_indices]

    # Converte as arestas da MST para coordenadas para a plotagem
    arestas_mst_coords = [(g_vis.vertices[u], g_vis.vertices[v]) for u, v in mst_indices]

    Grafo.desenhar_mapa(q_start, q_goal, obstaculos, vertices=g_vis.vertices, 
                        grafo=grafo_indexado,mst=arestas_mst_coords, caminho_final=caminho_final_coords)       