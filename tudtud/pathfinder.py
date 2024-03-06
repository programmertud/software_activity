import heapq
import tkinter as tk
from tkinter import ttk

# Define your places and their coordinates
places = {
    "Entrance Gate": (500, 630),
    "Mid Str-2nd Flr": (500, 600),
    
    # EAST
    "Str1": (410, 600),
    "Student Center": (280, 600),
    "Str1-2nd Flr": (100, 600),
    "ADMINISTRATION": (100, 550),
    "BOARD ROOM": (180, 550),
    "UNIVERSITY PRES": (260, 550),
    "VP ADMIN": (340, 550),
    "VP ACAD": (410, 550),
    "VP RDE": (455, 550),
    "HRMO": (500, 550),
    "REGISTRAR": (590, 550),    
    
    "2 ways": (100, 500),
    "ACCOUNTING": (100, 415),
    "CASHER": (100, 365),
    "BUDGET": (100, 315),
    "COLLEGE PRES": (100, 265),
    "Str2-down": (165, 265),
    "CANTEEN": (165, 150),
    "Str3-2nd Flr": (100, 150),
    "CATERING": (270, 150),
    "Str4-2nd Flr": (360, 150),
    "way(2)": (425, 150),
    "USC Office": (425, 100),
    
    "LIBRARY": (500, 150),
    
    "Str1-down": (200, 500),
    "SUPPLY": (200, 450),
    "COA": (200, 380),
    "way(1)": (270, 500),
    "COA BODEGA": (270, 380),
    "ICT Office": (270, 250),
    
    "PARKING LOT": (500, 315),
    
    # WEST
    "Str2": (590, 600),
    "REGISTRAR": (590, 550),
    "Str2-2nd Flr": (900, 600),
    "PLANNING": (900, 550),
    "BUILDING & ESTATES": (900, 450),
    "EXIT GATE": (900, 315),
    "NSTP Office": (900, 250),
    "DRRMO": (800, 250),
    "FITNESS STUDIO": (700, 250),
    "DANCE STUDIO": (600, 250),
    "way(3)": (500, 250),
    
    "Str5-2nd Flr": (640, 150),
    "CLINIC": (690, 150),
    "GUIDANCE": (740, 150),
    "PLACEMENT": (800, 150),
    "SAO": (845, 150),
    "Str6-2nd Flr": (900,150),   
}

# Define paths between locations
paths = [
    ("Entrance Gate", "Mid Str-2nd Flr"),
    ("Mid Str-2nd Flr", "Str1"),
    ("Mid Str-2nd Flr", "Str2"),
    
    # EAST
    ("Entrance Gate", "Str1"),
    ("Str1", "Student Center"),
    ("Str1", "VP ACAD"),
    ("Student Center", "Str1-2nd Flr"),
    ("Str1-2nd Flr", "ADMINISTRATION"),
    ("ADMINISTRATION", "2 ways"),
    ("ADMINISTRATION", "BOARD ROOM"),
    ("BOARD ROOM", "UNIVERSITY PRES"),
    ("UNIVERSITY PRES", "VP ADMIN"),
    ("VP ADMIN", "VP ACAD"),
    ("VP ACAD", "VP RDE"),
    ("VP RDE", "HRMO"),
    ("HRMO", "REGISTRAR"),
    
    ("2 ways", "ACCOUNTING"),
    ("ACCOUNTING", "CASHER"),
    ("CASHER", "BUDGET"),
    ("BUDGET", "COLLEGE PRES"),
    ("COLLEGE PRES","Str2-down"),
    ("Str2-down", "CANTEEN"),   
    ("CANTEEN", "CATERING"),
    ("CANTEEN", "Str3-2nd Flr"),
    ("CATERING", "Str4-2nd Flr"),
    ("Str4-2nd Flr", "way(2)"),
    ("way(2)", "USC Office"),
    
    ("way(2)","LIBRARY"),
    
    ("2 ways", "Str1-down"),
    ("Str1-down", "SUPPLY"),
    ("SUPPLY", "COA"),
    ("Str1-down", "way(1)"),
    ("way(1)", "COA BODEGA"),
    ("COA BODEGA", "ICT Office"),
    ("COA BODEGA", "PARKING LOT"),
    ("ICT Office", "PARKING LOT"),
    ("PARKING LOT", "way(3)"),
    
    ("way(3)", "LIBRARY"),
    
    # WEST
    ("Entrance Gate", "Str2"),
    ("Str2", "Str2-2nd Flr"),
    ("Str2", "REGISTRAR"),
    ("REGISTRAR", "PLANNING"),
    ("Str2-2nd Flr", "PLANNING"),
    ("PLANNING", "BUILDING & ESTATES"),
    ("BUILDING & ESTATES", "EXIT GATE"),
    ("EXIT GATE", "NSTP Office"),  
    ("NSTP Office", "DRRMO"),
    ("DRRMO", "FITNESS STUDIO"),
    ("FITNESS STUDIO", "DANCE STUDIO"),
    
    ("DANCE STUDIO", "way(3)"),
    ("way(3)", "PARKING LOT"),
    
    ("LIBRARY", "Str5-2nd Flr"),
    ("Str5-2nd Flr", "CLINIC"),
    ("CLINIC", "GUIDANCE"),
    ("GUIDANCE", "PLACEMENT"),
    ("PLACEMENT", "SAO"),
    ("SAO", "Str6-2nd Flr"),
]


# Create a grid to represent the map
grid = [[0] * 900 for _ in range(700)]  # Initialize grid with zeros

# Determine maximum x and y values
max_x = max(x for x, _ in places.values())
max_y = max(y for _, y in places.values())

# Create a grid to represent the map
grid = [[0] * (max_x + 1) for _ in range(max_y + 1)]  # Initialize grid with zeros

# Update grid to mark blocked locations
for place, (x, y) in places.items():
    grid[y][x] = 1


# Function to move an object along the path
def move_along_path(object_id, path):
    for i in range(len(path) - 1):
        (x1, y1), (x2, y2) = places[path[i]], places[path[i + 1]]
        dx = x2 - x1
        dy = y2 - y1
        distance = max(abs(dx), abs(dy))
        steps = distance // 5  # Adjust speed here
        for s in range(steps):
            x = x1 + dx * s / steps
            y = y1 + dy * s / steps
            canvas.coords(object_id, x - 5, y - 5, x + 5, y + 5)  # Move the object to the new coordinates
            root.update()
            canvas.after(50)  # Adjust speed here

# Function to find the shortest path between two points
def shortest_path(start, goal):
    # Initialize the queue and visited set
    queue = [(0, start, [])]  # Include a list to store the path
    visited = set()

    # While the queue is not empty
    while queue:
        # Dequeue the current node, distance, and path
        dist, current, path = heapq.heappop(queue)

        # If this node has not been visited yet
        if current not in visited:
            # Mark this node as visited
            visited.add(current)

            # If this is the goal node, we are done
            if current == goal:
                return dist, path + [current]  # Return the path as well

            # Otherwise, enqueue all neighbors
            for neighbor in paths:
                if current == neighbor[0] and neighbor[1] not in visited:
                    heapq.heappush(queue, (dist + 1, neighbor[1], path + [current]))
                elif current == neighbor[1] and neighbor[0] not in visited:
                    heapq.heappush(queue, (dist + 1, neighbor[0], path + [current]))

    # If we get here, there is no path between the start and goal
    print(f"No path found between {start} and {goal}")  # Add debugging statement
    return None

    

# Define the main GUI window
root = tk.Tk()
root.title("SNSU MAIN - GROUND FLOOR")
start_var = tk.StringVar(value="Entrance Gate")

# Create a canvas to draw the map
canvas = tk.Canvas(root, width=1000, height=715)
canvas.pack()

# Draw paths
for start, end in paths:
    (x1, y1), (x2, y2) = places[start], places[end]
    canvas.create_line(x1, y1, x2, y2, fill="blue")

# Draw places
for place, (x, y) in places.items():
    circle = canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")
    label = canvas.create_text(x, y + 20, text=place, anchor="w", font=("Arial", 7))

# Function to move an object along the path
# Function to move an object along the path
def move_along_path(object_id, path):
    for i in range(len(path) - 1):
        (x1, y1), (x2, y2) = places[path[i]], places[path[i + 1]]
        dx = x2 - x1
        dy = y2 - y1
        distance = max(abs(dx), abs(dy))
        steps = distance // 5  # Adjust speed here
        for s in range(steps):
            canvas.move(object_id, dx / steps, dy / steps)
            root.update()
            canvas.after(50)  # Adjust speed here


# Function to handle mouse clicks
# Function to handle mouse clicks
def on_click(event):
    x, y = event.x, event.y
    start_point = "Entrance Gate"  # Set the starting point to Entrance Gate
    for place, (px, py) in places.items():
        if abs(x - px) < 8 and abs(y - py) < 8:
            result = shortest_path(start_point, place)
            if result is not None:
                path = result[1]
                object_id = canvas.create_oval(places[start_point][0] - 8, places[start_point][1] - 8, places[start_point][0] + 8, places[start_point][1] + 8, fill="green")  # Create a moving object at Entrance Gate
                move_along_path(object_id, path)  # Move the object along the path
                canvas.delete(object_id)  # Delete the object after moving along the path

# Bind mouse click event to canvas
canvas.bind("<Button-1>", on_click)


# Start the GUI main loop
root.mainloop()
