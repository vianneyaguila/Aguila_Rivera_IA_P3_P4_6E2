import tkinter as tk # Para crear la interfaz gráfica
from tkinter import messagebox # Para mostrar mensajes emergentes
import networkx as nx # Permite crear y trabajar con graficos 
import matplotlib.pyplot as plt # Para dibujar los gráficos como imágenes  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Permite integrarse a matpotlib dentro de la ventana de Tkin
import heapq #Para manejar una cola de prioridad (usada por Prim)

# Grafo de ejemplo
#Se define el grafo como un diccionario, donde cada clave es un nodo, y el valor es una lista de tuplas(vecino, peso).
grafo = {
    'A': [('B', 2), ('C', 3)],
    'B': [('A', 2), ('C', 1), ('D', 1)],
    'C': [('A', 3), ('B', 1), ('D', 4), ('E', 5)],
    'D': [('B', 1), ('C', 4), ('E', 1)],
    'E': [('C', 5), ('D', 1)],
}

class PrimApp: #Se crea una clase para organizar la aplicación y sus elementos
    def __init__(self, root): #Método que se ejecuta al crear la aplicación root es la ventana principal
        self.root = root
        self.root.title("Simulador Algoritmo de Prim") #Se guarda la ventana en self.root y se le pone el titulo
        self.graph = nx.Graph() # Se crea una grafo en networkx
        self.create_graph() #Se llama a un método (create_graph) para agrgar los nudos y aristas
        self.pos = nx.spring_layout(self.graph) # Calcula las posiciones visuales de los nodos (diseño automático)
        self.step = 0 # No se usa directamentepero puede servir para contar pasos
        self.mst_edges = [] # Lista de aristas agregadas al árbol
        self.visited = set() # Conjunto de nudos ya visitados
        self.edges_queue = [(0, None, 'A')]  # (peso, desde, hasta) # Cola de prioridad que guarda las posibles aristas a usar

        # Interfaz gráfica
        self.figure, self.ax = plt.subplots(figsize=(6, 4)) # Crea un gráfico (figure) con un eje (ax) donde se dibujara el gráfico
        self.canvas = FigureCanvasTkAgg(self.figure, master=root) #Incrusta el gráfico de matplotlib dentro de la ventana
        self.canvas.get_tk_widget().pack()

        self.label_step = tk.Label(root, text="Haz clic en 'Siguiente paso' para iniciar.", font=("Arial", 12))
        self.label_step.pack(pady=5) # Etiqueta que mostrará los mensajes descriptivos en la interfaz

        self.next_button = tk.Button(root, text="Siguiente paso", command=self.step_prim)
        self.next_button.pack(pady=10) # Botón que al hacer clic ejecuta el siguiente paso del algoritmo

        self.draw_graph("Esperando para iniciar...") # Dibuja el gráfico inicial sin ningún arista seleccionado

    def create_graph(self): 
        for nodo, vecinos in grafo.items():
            for vecino, peso in vecinos:
                self.graph.add_edge(nodo, vecino, weight=peso) #Lee el diccionario grafo y crea las aristas en networkx

    def draw_graph(self, descripcion=""):
        self.ax.clear()
        edge_colors = ['green' if (u, v) in self.mst_edges or (v, u) in self.mst_edges else 'black' for u, v in self.graph.edges()]
        weights = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, self.pos, with_labels=True, edge_color=edge_colors, node_color='skyblue', ax=self.ax)
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=weights, ax=self.ax)
        self.canvas.draw()
        self.label_step.config(text=descripcion)

    def step_prim(self):
        while self.edges_queue:
            peso, desde, hasta = heapq.heappop(self.edges_queue)
            if hasta in self.visited:
                continue
            self.visited.add(hasta)

            if desde:
                self.mst_edges.append((desde, hasta))
                descripcion = f"Se agrega la arista: {desde} --{peso}--> {hasta}"
                print(descripcion)
            else:
                descripcion = f"Iniciando desde el nodo: {hasta}"
                print(descripcion)

            for vecino, p in grafo[hasta]:
                if vecino not in self.visited:
                    heapq.heappush(self.edges_queue, (p, hasta, vecino))

            self.draw_graph(descripcion)
            return  # Salir para hacer paso a paso

        # Cuando ya se ha terminado el MST
        self.draw_graph("Árbol de expansión mínima completado.")
        print("Árbol de expansión mínima completado.")
        messagebox.showinfo("Finalizado", "El árbol ha sido generado completamente.")
        self.next_button.config(state="disabled")

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = PrimApp(root)
    root.mainloop()
