import dearpygui.dearpygui as dpg
import numpy as np
from PIL import Image
import os

# Constantes
WIDTH, HEIGHT = 50, 50
CELL_SIZE = 10
MIN_CELL_SIZE = 5
MAX_CELL_SIZE = 20

class Colores:
    def __init__(self, color, R, G, B, a, num):
        self.color = color
        self.r = R
        self.g = G
        self.b = B
        self.a = a
        self.num = num

    def ObtenerRGB(self):
        return (self.r, self.g, self.b, self.a)

    def ObtenerNum(self):
        return self.num

class ASCII:
    def __init__(self, numero, simbolo):
        self.numero = numero
        self.simbolo = simbolo

    def ObtenerSimbolo(self):
        return self.simbolo

# Instanciación de colores
Borrador = Colores("Borrador", 255, 255, 255, 255, 0)
Plata = Colores("Plata", 192, 192, 192, 255, 1)
Amarillo = Colores("Amarillo", 250, 250, 0, 255, 2)
Rojo = Colores("Rojo", 250, 20, 10, 255, 3)
Azul = Colores("Azul", 10, 10, 245, 255, 4)
Verde = Colores("Verde", 30, 154, 94, 255, 5)
Siena = Colores("Siena", 166, 66, 46, 255, 6)
Purpura = Colores("Purpura", 177, 156, 217, 255, 7)
Gris = Colores("Gris", 64, 64, 79, 255, 8)
Negro = Colores("Negro", 0, 0, 0, 255, 9)

# Diccionarios para acceso rápido
Colores = {
    "Borrador": Borrador,
    "Plata": Plata,
    "Amarillo": Amarillo,
    "Rojo": Rojo,
    "Azul": Azul,
    "Verde": Verde,
    "Siena": Siena,
    "Purpura": Purpura,
    "Gris": Gris,
    "Negro": Negro
}

ValoresColores = {
    Borrador.ObtenerRGB(): Borrador.ObtenerNum(),
    Plata.ObtenerRGB(): Plata.ObtenerNum(),
    Amarillo.ObtenerRGB(): Amarillo.ObtenerNum(),
    Rojo.ObtenerRGB(): Rojo.ObtenerNum(),
    Azul.ObtenerRGB(): Azul.ObtenerNum(),
    Verde.ObtenerRGB(): Verde.ObtenerNum(),
    Siena.ObtenerRGB(): Siena.ObtenerNum(),
    Purpura.ObtenerRGB(): Purpura.ObtenerNum(),
    Gris.ObtenerRGB(): Gris.ObtenerNum(),
    Negro.ObtenerRGB(): Negro.ObtenerNum()
}

# Instanciación de símbolos ASCII
Espacio = ASCII(0, ' ')
Punto = ASCII(1, '.')
DosPuntos = ASCII(2, ':')
Guion = ASCII(3, '-')
Porcentaje = ASCII(4, '%')
Exclamacion = ASCII(5, '¡')
Ampersand = ASCII(6, '&')
Dolar = ASCII(7, '$')
Porcentaje = ASCII(8, '%')
Arroba = ASCII(9, '@')

DiccionarioASCII = {
    0: Espacio.ObtenerSimbolo(),
    1: Punto.ObtenerSimbolo(),
    2: DosPuntos.ObtenerSimbolo(),
    3: Guion.ObtenerSimbolo(),
    4: Porcentaje.ObtenerSimbolo(),
    5: Exclamacion.ObtenerSimbolo(),
    6: Ampersand.ObtenerSimbolo(),
    7: Dolar.ObtenerSimbolo(),
    8: Porcentaje.ObtenerSimbolo(),
    9: Arroba.ObtenerSimbolo()
}

# Valores iniciales
ColorActual = Colores["Negro"]
grid = [[Colores["Borrador"].ObtenerRGB() for _ in range(WIDTH)] for _ in range(HEIGHT)]

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

def ClickPosicion(sender, app_data, user_data):
    mouse_pos = dpg.get_mouse_pos()
    x = int(mouse_pos[0] // CELL_SIZE)
    y = int(mouse_pos[1] // CELL_SIZE)
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        grid[y][x] = ColorActual.ObtenerRGB()
        DibujaGrid()
        
def CambioAColorElegido(sender, app_data, user_data):
    global ColorActual
    ColorActual = Colores[user_data]

def DibujaMatriz():
    matrix = [[ValoresColores[grid[y][x]] for x in range(WIDTH)] for y in range(HEIGHT)]
    for row in matrix:
        print(" ".join(map(str, row)))

def DibujaASCII():
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
    pixel_data = []
    for row in grid:
        for color in row:
            pixel_data.extend(color[:3])  # Toma solo los valores RGB
    pixel_data = np.array(pixel_data, dtype=np.uint8)
    pixel_data = np.reshape(pixel_data, (HEIGHT, WIDTH, 3))
    image = Image.fromarray(pixel_data)
    
    folder = os.path.dirname(os.path.abspath(__file__))  # Folder para guardar la imagen
    path = os.path.join(folder, "PixelArt.png")
    
    image.save(path)  # Guarda la imagen
    print(f"Image saved at {path}")

def Importar():
    return

dpg.create_context()

with dpg.window(label="Pixel Art Editor", tag="Primary Window"):
    with dpg.group(horizontal=True):
        with dpg.group():
            with dpg.drawlist(width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, tag="Dibujo"):
                dpg.set_item_callback("Dibujo", ClickPosicion)

        with dpg.group():
            for color_name in Colores:
                dpg.add_button(label=color_name, callback=CambioAColorElegido, user_data=color_name)
            
            dpg.add_button(label="Zoom In", callback=ZoomIn)
            dpg.add_button(label="Zoom Out", callback=ZoomOut)
            dpg.add_button(label="Mostrar Matrix", callback=DibujaMatriz)
            dpg.add_button(label="Mostrar ASCII", callback=DibujaASCII)
            dpg.add_button(label="Importar imagen", callback=Importar)
            dpg.add_button(label="Guardar Imagen", callback=GuardaImagen)

DibujaGrid()

dpg.create_viewport(title='Pixel Art Editor', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()