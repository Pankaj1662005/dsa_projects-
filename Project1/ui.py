import tkinter as tk
from collections import deque

# Updated Graph
graph = {
    "Delhi": ["Jaipur", "Agra", "Mumbai"],
    "Jaipur": ["Delhi", "Udaipur", "Agra"],
    "Agra": ["Delhi", "Kanpur", "Udaipur", "Jaipur"],
    "Udaipur": ["Jaipur", "Agra", "Kanpur"],
    "Mumbai": ["Delhi"],
    "Kanpur": ["Agra", "Udaipur"],
    "London": ["Paris", "Rome"],
    "Paris": ["London", "Rome"],
    "Rome": ["London", "Paris"]
}

# Node positions for Tkinter display
positions = {
    "Delhi": (100, 100),
    "Jaipur": (200, 50),
    "Agra": (200, 150),
    "Udaipur": (300, 100),
    "Mumbai": (100, 200),
    "Kanpur": (300, 200),
    "London": (500, 100),
    "Paris": (600, 50),
    "Rome": (600, 150)
}

# BFS to find path
def find_path(graph, start, end):
    visited = {}
    parent = {}
    q = deque([start])
    visited[start] = True

    while q:
        current = q.popleft()
        if current == end:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited[neighbor] = True
                parent[neighbor] = current
                q.append(neighbor)
    return None


# Draw the graph
def draw_graph(canvas, path=None):
    canvas.delete("all")

    # Draw edges
    drawn_edges = set()
    for node, neighbors in graph.items():
        x1, y1 = positions[node]
        for neighbor in neighbors:
            edge = tuple(sorted((node, neighbor)))
            if edge in drawn_edges:
                continue  # Avoid drawing duplicate edges
            drawn_edges.add(edge)

            x2, y2 = positions[neighbor]
            if path and node in path and neighbor in path:
                idx1 = path.index(node)
                idx2 = path.index(neighbor)
                if abs(idx1 - idx2) == 1:  # part of path
                    canvas.create_line(x1, y1, x2, y2, fill="red", width=3)
                    continue
            canvas.create_line(x1, y1, x2, y2)

    # Draw nodes
    for node, (x, y) in positions.items():
        canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue")
        canvas.create_text(x, y, text=node)


# Tkinter UI
def run():
    def on_find_path():
        start = start_entry.get()
        end = end_entry.get()
        if start not in graph or end not in graph:
            result_label.config(text="Invalid node names")
            return
        path = find_path(graph, start, end)
        if path:
            result_label.config(text=" -> ".join(path))
        else:
            result_label.config(text="No path found")
        draw_graph(canvas, path)

    root = tk.Tk()
    root.title("Graph Visualization with Path Highlight")

    canvas = tk.Canvas(root, width=800, height=400, bg="white")
    canvas.pack()

    control_frame = tk.Frame(root)
    control_frame.pack()

    tk.Label(control_frame, text="Start:").pack(side=tk.LEFT)
    start_entry = tk.Entry(control_frame)
    start_entry.pack(side=tk.LEFT)

    tk.Label(control_frame, text="End:").pack(side=tk.LEFT)
    end_entry = tk.Entry(control_frame)
    end_entry.pack(side=tk.LEFT)

    find_button = tk.Button(control_frame, text="Find Path", command=on_find_path)
    find_button.pack(side=tk.LEFT)

    result_label = tk.Label(root, text="")
    result_label.pack()

    draw_graph(canvas)
    root.mainloop()


if __name__ == "__main__":
    run()
