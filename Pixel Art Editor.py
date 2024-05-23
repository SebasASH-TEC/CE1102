import dearpygui.dearpygui as dpg
import numpy as np
from PIL import Image
import os

# Constantes
WIDTH, HEIGHT = 50, 50
CELL_SIZE = 10
MIN_CELL_SIZE = 5
MAX_CELL_SIZE = 20

Colores = {
    "Blanco": (255, 255, 255, 255),
    "Plata": (192, 192, 192, 255),
    "Amarillo": (250, 250, 0, 255),
    "Rojo": (250, 20, 10, 255),
    "Azul": (10, 10, 245, 255),
    "Verde": (30, 154, 94, 255),
    "Siena": (166, 66, 46, 255),
    "Púrpura": (177, 156, 217, 255),
    "Gris": (64, 64, 79, 255),
    "Negro": (0, 0, 0, 255)
}

# Valores en la matriz de cada color
ValoresColores = {
    (255, 255, 255, 255): 0,
    (192, 192, 192, 255): 1,
    (250, 250, 0, 255): 2,
    (250, 20, 10, 255): 3,
    (10, 10, 245, 255): 4,
    (30, 154, 94, 255): 5,
    (166, 66, 46, 255): 6,
    (177, 156, 217, 255): 7,
    (64, 64, 79, 255): 8,
    (0, 0, 0, 255): 9
}

# Valores iniciales
ColorActual = Colores["Negro"]
grid = [[Colores["Blanco"] for _ in range(WIDTH)] for _ in range(HEIGHT)]

def DibujaGrid():
    dpg.delete_item("Dibujo", children_only=True)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dpg.draw_rectangle([x * CELL_SIZE, y * CELL_SIZE],
                               [(x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE],
                               color=(0, 0, 0, 255), fill=grid[y][x], parent="Dibujo")
    for x in range(WIDTH + 1):
        dpg.draw_line([x * CELL_SIZE, 0], [x * CELL_SIZE, HEIGHT * CELL_SIZE], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")
    for y in range(HEIGHT + 1):
        dpg.draw_line([0, y * CELL_SIZE], [WIDTH * CELL_SIZE, y * CELL_SIZE], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")

def ClickPosicion(sender, app_data, user_data): #Callbacks de DPG
    mouse_pos = dpg.get_mouse_pos(local=True)
    x = int(mouse_pos[0] // CELL_SIZE)
    y = int(mouse_pos[1] // CELL_SIZE)
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        grid[y][x] = ColorActual
        DibujaGrid()
        
def CambioAColorElegido(sender, app_data, user_data):
    global ColorActual
    ColorActual = Colores[user_data]

def DibujaMatriz():
    matrix = [[ValoresColores[grid[y][x]] for x in range(WIDTH)] for y in range(HEIGHT)]
    for row in matrix:
        print(" ".join(map(str, row)))

def DibujaASCII():
    DiccionarioASCII = {0: ' ', 1: '.', 2: ':', 3: '-', 4: '%', 5: "¡", 6: "&", 7: "$", 8: "%", 9: "@"}
    matrix = [[ValoresColores[grid[y][x]] for x in range(WIDTH)] for y in range(HEIGHT)]
    for row in matrix:
        print("".join(DiccionarioASCII[val] for val in row))

def ZoomIn():
    global CELL_SIZE
    if CELL_SIZE < MAX_CELL_SIZE:
        CELL_SIZE += 1
        DibujaGrid()

def ZoomOut():
    global CELL_SIZE
    if CELL_SIZE > MIN_CELL_SIZE:
        CELL_SIZE -= 1
        DibujaGrid()

def GuardaImagen():
    pixel_data = [] #Lista vacia para almacenar los metadatos
    for row in grid:
        for color in row:
            pixel_data.extend(color[:3])  # Toma solo los valores RGB
    pixel_data = np.array(pixel_data, dtype=np.uint8)
    pixel_data = np.reshape(pixel_data, (HEIGHT, WIDTH, 3))
    image = Image.fromarray(pixel_data)
    
    
    Folder = os.path.dirname(os.path.abspath(__file__)) #Folder para guardar la imagen
    Path = os.path.join(Folder, "PixelArt.png")
    
    image.save(Path) #Guarda la imagen
    print(f"Image saved at {Path}")

dpg.create_context()

with dpg.window(label="Pixel Art Editor"):
    with dpg.group(horizontal=True):
        for color_name in Colores:
            dpg.add_button(label=color_name, callback=CambioAColorElegido, user_data=color_name)
    
    with dpg.group(horizontal=True):
        dpg.add_button(label="Zoom In", callback=ZoomIn)
        dpg.add_button(label="Zoom Out", callback=ZoomOut)
    
    with dpg.drawlist(width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, tag="Dibujo"):
        dpg.set_item_callback("Dibujo", ClickPosicion)

    dpg.add_button(label="Mostrar Matrix", callback=DibujaMatriz)
    dpg.add_button(label="Mostrar ASCII", callback=DibujaASCII)
    dpg.add_button(label="Guardar Imagen", callback=GuardaImagen)

DibujaGrid()

dpg.create_viewport(title='Pixel Art Editor', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
