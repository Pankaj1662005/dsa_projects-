import tkinter as tk
from tkinter import messagebox, ttk
import subprocess

# City positions (for drawing)
positions = {
    "Delhi": (100, 100),
    "Jaipur": (300, 160),
    "Agra": (220, 230),
    "Udaipur": (420, 230),
    "Ahmedabad": (540, 260),
    "Kanpur": (300, 320),
    "Lucknow": (400, 370),
    "Varanasi": (520, 420),
    "Mumbai": (680, 300)
}

cities = list(positions.keys())

# Edges between cities
edges = [
    ("Delhi", "Jaipur", 280), ("Delhi", "Agra", 210),
    ("Jaipur", "Udaipur", 390), ("Agra", "Kanpur", 270),
    ("Udaipur", "Ahmedabad", 260), ("Kanpur", "Lucknow", 90),
    ("Ahmedabad", "Mumbai", 530), ("Lucknow", "Varanasi", 320),
    ("Lucknow", "Mumbai", 1360), ("Mumbai", "Varanasi", 1420)
]

# Function to call C++ program
def run_cpp(start, end):
    try:
        result = subprocess.run(["./dijkstra"], input=f"{start} {end}\n",
                                text=True, capture_output=True)
        out = result.stdout.strip().split("\n")
        if not out or "NoPath" in out[0]:
            return None, []
        dist = int(out[0])
        path = out[1].split()
        return dist, path
    except Exception as e:
        messagebox.showerror("Error", e)
        return None, []

def draw_map(path=[]):
    canvas.delete("all")

    for c1, c2, w in edges:
        x1, y1 = positions[c1]
        x2, y2 = positions[c2]
        color = "gray"
        width = 2
        if path and c1 in path and c2 in path:
            i1, i2 = path.index(c1), path.index(c2)
            if abs(i1 - i2) == 1:
                color = "red"
                width = 3
        canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
        canvas.create_text((x1+x2)/2, (y1+y2)/2 - 10, text=f"{w} km", fill="black")

    for city, (x, y) in positions.items():
        canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue")
        canvas.create_text(x, y, text=city)

def find_path():
    s, e = start_var.get(), end_var.get()
    if not s or not e:
        messagebox.showwarning("Error", "Please select both cities.")
        return
    if s == e:
        messagebox.showinfo("Info", "Source and destination are same.")
        draw_map()
        label_result.config(text="Distance: 0 km")
        return

    d, p = run_cpp(s, e)
    if not d:
        label_result.config(text="No path found.")
        draw_map()
    else:
        label_result.config(text=f"Path: {' -> '.join(p)}\nDistance: {d} km")
        draw_map(p)

root = tk.Tk()
root.title("City Path Finder")
root.geometry("850x600")

frame = ttk.Frame(root)
frame.pack(pady=10)

start_var = tk.StringVar()
end_var = tk.StringVar()

ttk.Label(frame, text="Source:").grid(row=0, column=0)
ttk.Combobox(frame, textvariable=start_var, values=cities, width=12, state="readonly").grid(row=0, column=1)
ttk.Label(frame, text="Destination:").grid(row=0, column=2)
ttk.Combobox(frame, textvariable=end_var, values=cities, width=12, state="readonly").grid(row=0, column=3)
ttk.Button(frame, text="Find Path", command=find_path).grid(row=0, column=4, padx=10)

label_result = tk.Label(root, text="", font=("Arial", 11))
label_result.pack()

canvas = tk.Canvas(root, width=820, height=480, bg="white")
canvas.pack()

draw_map()
root.mainloop()
