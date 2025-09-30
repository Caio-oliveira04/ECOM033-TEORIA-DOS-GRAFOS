class Edge:
    def __init__(self, source, destination, weight):
        self.source = source
        self.destination = destination
        self.weight = weight

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.edges = []    # List to store graph edges

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_edges_from_list(self, edge_list):
        for edge in edge_list:
            self.add_edge(edge)

def bellman_ford(vertices, edges, source):
    # Inicializa as distâncias de todos os vértices como infinito
    distance = [float("Inf")] * vertices
    distance[source] = 0  # A distância do vértice de origem para ele mesmo é 0

    # Relaxa todas as arestas |V| - 1 vezes
    for _ in range(vertices - 1):
        for edge in edges:
            if distance[edge.source] != float("Inf") and distance[edge.source] + edge.weight < distance[edge.destination]:
                distance[edge.destination] = distance[edge.source] + edge.weight

    # Verifica se há ciclos de peso negativo
    for edge in edges:
        if distance[edge.source] != float("Inf") and distance[edge.source] + edge.weight < distance[edge.destination]:
            print("O grafo contém um ciclo de peso negativo")
            return None

    return distance

def read_file(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def min_path(distance, source, destination):
    if distance[destination] == float("Inf"):
        return f"Não há caminho do vértice {source} ao vértice {destination}"
    else:
        return f"O menor caminho do vértice {source} ao vértice {destination} é {distance[destination]}"

def sum_of_cost_path(distance, path):
    total_cost = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if distance[v] == float("Inf"):
            return float("Inf")
        total_cost += distance[v] - distance[u]
    return total_cost

def build_graph(lines):
    edges = []
    verticesNumber = 0
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            verticesNumber = int(parts[0])
            continue
        if len(parts) == 3:
            source = int(parts[0])
            destination = int(parts[1])
            weight = int(parts[2])
            edges.append(Edge(source, destination, weight))
    graph = Graph(verticesNumber)
    graph.add_edges_from_list(edges)
    return graph

if __name__ == "__main__":

    # Construir grafo a partir do arquivo
    lines = read_file('graph2.txt')
    graph = build_graph(lines)
    distance = bellman_ford(graph.V, graph.edges, 0)
    print(min_path(distance, 0, 6))
    print(sum_of_cost_path(distance, [0, 1, 3, 5, 6]))
    print(f"Número de vértices: {graph.V}")