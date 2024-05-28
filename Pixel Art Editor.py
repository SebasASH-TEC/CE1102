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

class Matriz:
    def __init__(self, width, height, default_value=0):
        self.width = width
        self.height = height
        self.grid = [[default_value for _ in range(width)] for _ in range(height)]

    @classmethod
    def LeerTXT(cls, filepath, width=WIDTH, height=HEIGHT, default_value=0):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        matriz = cls(width, height, default_value)
        for y, line in enumerate(lines):
            values = list(map(int, line.split()))
            for x, value in enumerate(values):
                if x < width and y < height:
                    matriz.grid[y][x] = value
        return matriz

    def ConvertirAGrid(self, colores_dict):
        return [[colores_dict.get(val, colores_dict[0]).ObtenerRGB() for val in row] for row in self.grid]

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
    0: Borrador,
    1: Plata,
    2: Amarillo,
    3: Rojo,
    4: Azul,
    5: Verde,
    6: Siena,
    7: Purpura,
    8: Gris,
    9: Negro
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
    global matrix
    matrix = [[ValoresColorANumero(grid[y][x]) for x in range(WIDTH)] for y in range(HEIGHT)]
    for row in matrix:
        print(" ".join(map(str, row)))

def DibujaASCII():
    matrix = [[ValoresColorANumero(grid[y][x]) for x in range(WIDTH)] for y in range(HEIGHT)]
    for row in matrix:
        print("".join(DiccionarioASCII[val] for val in row))

def ValoresColorANumero(rgb):
    for num, color in ValoresColores.items():
        if color.ObtenerRGB() == rgb:
            return num
    return 0  # Retorna a borrador (BLanco) si no se encuentra

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
    GridExpandido = [] # Crea un nuevo grid donde cada pixel se convierte en un 2x2 (Como el checkboarding de la playstation)
    for row in grid:
        NuevoRow = []
        for color in row:
            NuevoRow.extend([color[:3], color[:3]])  # Duplica cada pixel horizontalmente
        GridExpandido.extend([NuevoRow, NuevoRow])  # Verticalmente
    
    pixel_data = np.array(GridExpandido, dtype=np.uint8) #Convierte el grid expandido en un array de numpy 
    image = Image.fromarray(pixel_data)
    folder = os.path.dirname(os.path.abspath(__file__)) 
    path = os.path.join(folder, "PixelArt.png")
    TXTPath = os.path.join(folder, "PixelArt.txt")
    
    image.save(path)
    print(f"Image saved at {path}")

    Matriz = [[ValoresColorANumero(grid[y][x]) for x in range(WIDTH)] for y in range(HEIGHT)]
    with open(TXTPath, 'w') as file:
        for row in Matriz:
            file.write(" ".join(map(str, row)) + "\n")
    print(f"Matrix saved at {TXTPath}")
    
def ImportarImagen(sender, app_data, user_data):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'matriz.txt')
    if os.path.exists(filepath):
        MatrizImportada = Matriz.LeerTXT(filepath)
        global grid
        grid = MatrizImportada.ConvertirAGrid(ValoresColores)
        DibujaGrid()
    else:
        print(f"No se encontró el archivo {filepath}")

def BorraImagen():
    global grid
    grid = [[Colores["Borrador"].ObtenerRGB() for _ in range(WIDTH)] for _ in range(HEIGHT)]
    DibujaGrid()

def Altocontraste():
    global grid
    for y in range(HEIGHT):
        for x in range(WIDTH):
            valor = ValoresColorANumero(grid[y][x])
            if 0 <= valor <= 4:
                grid[y][x] = ValoresColores[1].ObtenerRGB()  # Cambiar a color Plata
            elif 5 <= valor <= 9:
                grid[y][x] = ValoresColores[9].ObtenerRGB()  # Cambiar a color Negro
    DibujaGrid()


def Negativo():
    global grid
    for y in range(HEIGHT):
        for x in range(WIDTH):
            valor = ValoresColorANumero(grid[y][x])
            if valor == 9:
                grid[y][x] = ValoresColores[0].ObtenerRGB()
            elif valor == 8:
                grid[y][x] = ValoresColores[1].ObtenerRGB()
            elif valor == 7:
                grid[y][x] = ValoresColores[2].ObtenerRGB()
            elif valor == 6:
                grid[y][x] = ValoresColores[3].ObtenerRGB()
            elif valor == 5:
                grid[y][x] = ValoresColores[4].ObtenerRGB()
            elif valor == 4:
                grid[y][x] = ValoresColores[5].ObtenerRGB()
            elif valor == 3:
                grid[y][x] = ValoresColores[6].ObtenerRGB()
            elif valor == 2:
                grid[y][x] = ValoresColores[7].ObtenerRGB()
            elif valor == 1:
                grid[y][x] = ValoresColores[8].ObtenerRGB()
            elif valor == 0:
                grid[y][x] = ValoresColores[9].ObtenerRGB()

    DibujaGrid()
    
def Rotarderecha():
    global grid
    filas = len(grid)
    columnas = len(grid[0])
    nueva_grid = [[None] * filas for _ in range(columnas)]
    for i in range(filas):
        for j in range(columnas):
            nueva_grid[j][filas - 1 - i] = grid[i][j]
    filas, columnas = columnas, filas
    grid = nueva_grid
    DibujaGrid()

def Rotarizquierda():
    global grid
    filas = len(grid)
    columnas = len(grid[0])
    nueva_grid = [[None] * filas for _ in range(columnas)]
    for i in range(filas):
        for j in range(columnas):
            nueva_grid[filas - 1 - j][i] = grid[i][j]
    filas, columnas = columnas, filas
    grid = nueva_grid
    DibujaGrid()

dpg.create_context()

with dpg.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = dpg.add_font("Roboto-Light.ttf", 20)
    second_font = dpg.add_font("Roboto-Light.ttf", 10)

with dpg.window(label="Pixel Art Editor", tag="Primary Window"):
    with dpg.group(horizontal=True):
        with dpg.group():
            with dpg.drawlist(width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, tag="Dibujo"):
                dpg.set_item_callback("Dibujo", ClickPosicion)

        with dpg.group():
            for color_name in Colores:
                dpg.add_button(label=color_name, callback=CambioAColorElegido, user_data=color_name, width=100, height=30)
            
            dpg.add_button(label="Zoom In", callback=ZoomIn, width=100, height=30)
            dpg.add_button(label="Zoom Out", callback=ZoomOut, width=100, height=30)
            dpg.add_button(label="Mostrar Matrix", callback=DibujaMatriz, width=140, height=30)
            dpg.add_button(label="Mostrar ASCII", callback=DibujaASCII, width=140, height=30)
            dpg.add_button(label="Importar imagen", callback=ImportarImagen, width=140, height=30)
            dpg.add_button(label="Guardar Imagen", callback=GuardaImagen, width=140, height=30)
            dpg.add_button(label="Alto contraste", callback=Altocontraste, width=140, height=30)
            dpg.add_button(label="Negativo", callback=Negativo, width=140, height=30)
            dpg.add_button(label="X", callback=BorraImagen, width=100, height=30)
            dpg.add_button(label="Rotar a la derecha", callback=Rotarderecha, width=140, height=30)
            dpg.add_button(label="Rotar a la izquierda", callback=Rotarizquierda, width=140, height=30)
            dpg.bind_font(default_font)
            
DibujaGrid()

dpg.create_viewport(title='Pixel Art Editor', width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
