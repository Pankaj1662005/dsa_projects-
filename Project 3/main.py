import tkinter as tk
from math import sqrt
import heapq
from PIL import Image, ImageTk  # Importing Image and ImageTk from PIL

# Positions of cities (x, y)
positions = {
    "Delhi": (200, 200),
    "Udaipur": (100, 280),
    "Mumbai": (130, 400),
    "Kolkata":(400,325),
    "Coimbatore":(200,550),
    "Manipur":(500,280)
}

# Function to calculate Euclidean distance
def euclidean_dist(pos1, pos2):
    return round(sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2), 2)

# Auto-generate graph with distances as weights
graph = {}
for node in positions:
    graph[node] = []
    for neighbor in positions:
        if neighbor != node:
            dist = euclidean_dist(positions[node], positions[neighbor])
            graph[node].append((neighbor, dist))

# Dijkstra algorithm to find min cost
def find_min_cost_path(graph, start, end):
    if start not in graph or end not in graph:
        return None, float('inf')

    costs = {node: float('inf') for node in graph}
    costs[start] = 0
    visited = set()
    heap = [(0, start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            return cost

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                new_cost = cost + weight
                if new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
    return None

# Draw the graph in Tkinter
# Draw the graph in Tkinter
def draw_graph(canvas, path=None):
    canvas.delete("all")
    drawn_edges = set()

    # Draw the map image as background
    try:
        map_image = Image.open("india_map.png")  # Replace with your map image path
        map_image = map_image.resize((600, 700))  # Resize to fit canvas
        map_photo = ImageTk.PhotoImage(map_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=map_photo)
        canvas.image = map_photo  # Keep a reference to prevent garbage collection
    except Exception as e:
        print(f"Error loading map image: {e}")

    # Draw grid lines every 100 pixels
    for x in range(0, 601, 100):  # X-axis lines
        canvas.create_line(x, 0, x, 700, fill="lightgray", dash=(2, 4))
        canvas.create_text(x + 5, 10, text=str(x), fill="black", font=("Arial", 8))

    for y in range(0, 701, 100):  # Y-axis lines
        canvas.create_line(0, y, 600, y, fill="lightgray", dash=(2, 4))
        canvas.create_text(10, y - 5, text=str(y), fill="black", font=("Arial", 8))

    # Draw edges
    for node, neighbors in graph.items():
        x1, y1 = positions[node]
        for neighbor, cost in neighbors:
            edge = tuple(sorted((node, neighbor)))
            if edge in drawn_edges:
                continue
            drawn_edges.add(edge)
            x2, y2 = positions[neighbor]

            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            canvas.create_text(mid_x, mid_y, text=str(cost), fill="gray", font=("Arial", 8))

    # Draw nodes
    for node, (x, y) in positions.items():
        canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue")
        canvas.create_text(x, y, text=node)

# Tkinter UI
def run():
    def on_find_path():
        start = start_entry.get()
        end = end_entry.get()

        cost = find_min_cost_path(graph, start, end)
        if cost is None:
            result_label.config(text="No path found")
        else:
            result_label.config(text=f"Minimum cost from {start} to {end} = {cost}")
        draw_graph(canvas)

    root = tk.Tk()
    root.title("Min Cost Path Finder")

    canvas = tk.Canvas(root, width=600, height=700, bg="white")
    canvas.pack()

    control_frame = tk.Frame(root)
    control_frame.pack()

    tk.Label(control_frame, text="Start:").pack(side=tk.LEFT)
    start_entry = tk.Entry(control_frame)
    start_entry.pack(side=tk.LEFT)

    tk.Label(control_frame, text="End:").pack(side=tk.LEFT)
    end_entry = tk.Entry(control_frame)
    end_entry.pack(side=tk.LEFT)

    find_button = tk.Button(control_frame, text="Find Min Cost", command=on_find_path)
    find_button.pack(side=tk.LEFT)

    result_label = tk.Label(root, text="")
    result_label.pack()

    draw_graph(canvas)
    root.mainloop()

if __name__ == "__main__":
    run()
