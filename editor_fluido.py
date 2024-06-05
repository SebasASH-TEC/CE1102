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
        return [[colores_dict.get(val, colores_dict[0]).ObtenerRGB() for val in fila] for fila in self.grid]
    
class Boton:
    def __init__(self, label, callback, user_data=None, width=100, height=30):
        self.label = label
        self.callback = callback
        self.user_data = user_data
        self.width = width
        self.height = height

    def CrearBoton(self):
        dpg.add_button(label=self.label, callback=self.callback, user_data=self.user_data, width=self.width, height=self.height)


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
    dpg.delete_item("Dibujo", children_only=True) #el children_only elimina solo las "subventanas", no la principal
    for y in range(HEIGHT):
        for x in range(WIDTH): #For anidados para dibujar la matriz
            dpg.draw_rectangle([x * CELL_SIZE, y * CELL_SIZE],
                               [(x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE],
                               color=(0, 0, 0, 255), fill=grid[y][x], parent="Dibujo") #Dibuja la matriz, utiliza el CELL_SIZE para saber de que tamano representar cada pixel
    for x in range(WIDTH + 1):
        dpg.draw_line([x * CELL_SIZE, 0], [x * CELL_SIZE, HEIGHT * CELL_SIZE], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")
    for y in range(HEIGHT + 1):
        dpg.draw_line([0, y * CELL_SIZE], [WIDTH * CELL_SIZE, y * CELL_SIZE], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")

def ClickPosicion(sender, app_data, user_data): #Funcion para detectar donde se presiona, aunque tiene errores de colision, es temporal
    mouse_pos = dpg.get_mouse_pos() #mouse_pos es una funcion de DearPyGUI
    x = int(mouse_pos[0] // CELL_SIZE)
    y = int(mouse_pos[1] // CELL_SIZE)
    if 0 <= x < WIDTH and 0 <= y < HEIGHT: #Verifica si el mouse clickea dentro del grid
        grid[y][x] = ColorActual.ObtenerRGB()   
        DibujaGrid()

def MouseDragHandler(sender, app_data):
    ClickPosicion(sender, app_data, None)

def CambioAColorElegido(sender, app_data, user_data): #Funcion que cambia el color a colocar segun seleccion del usuario
    global ColorActual
    ColorActual = Colores[user_data]

def DibujaMatriz(): #Dibuja la matriz en consola (de momento), segun los pixeles que se encuentre y su numero asociado
    global Matriz
    Matriz = [[ValoresColorANumero(grid[y][x]) for x in range(WIDTH)] for y in range(HEIGHT)]
    for fila in Matriz:
        print(" ".join(map(str, fila)))

def DibujaASCII(): #Lo mismo, pero con ASCII
    Matriz = [[ValoresColorANumero(grid[y][x]) for x in range(WIDTH)] for y in range(HEIGHT)]
    for fila in Matriz:
        print("".join(DiccionarioASCII[val] for val in fila))

def ValoresColorANumero(rgb): 
    for num, color in ValoresColores.items():
        if color.ObtenerRGB() == rgb:
            return num
    return 0  # Retorna a borrador (BLanco) si no se encuentra

def ZoomIn(): #Aumenta el tamano de la celda en 1 unidad (Tamano maximo 20)
    global CELL_SIZE
    if CELL_SIZE < MAX_CELL_SIZE:
        CELL_SIZE += 1
        DibujaGrid()

def ZoomOut(): #Decrementa el tamano de la celda en 1 unidad (Tamano minimo 5)
    global CELL_SIZE
    if CELL_SIZE > MIN_CELL_SIZE:
        CELL_SIZE -= 1
        DibujaGrid()

def GuardaImagen():
    GridExpandido = [] # Crea un nuevo grid donde cada pixel se convierte en un 2x2 (Como el checkerboard de la paleta de colores)
    for fila in grid:
        for _ in range(CELL_SIZE):
            nueva_fila = []
            for color in fila:
                nueva_fila.extend([color] * CELL_SIZE)
            GridExpandido.append(nueva_fila)
    img = Image.new('RGBA', (len(GridExpandido[0]), len(GridExpandido)), (255, 255, 255, 255)) #El blanco como fondo
    pixels = img.load()
    for y in range(len(GridExpandido)):
        for x in range(len(GridExpandido[y])):
            pixels[x, y] = GridExpandido[y][x]
    img.save("DibujoGuardado.png")
    print("Imagen guardada como DibujoGuardado.png")

# Interfaz de DearPyGUI
dpg.create_context()

with dpg.handler_registry():
    dpg.add_mouse_drag_handler(callback=MouseDragHandler) #función de dpg que captura el click del mouse

with dpg.window(label="Pixel Art", width=800, height=600):
    with dpg.drawlist(width=WIDTH*CELL_SIZE, height=HEIGHT*CELL_SIZE, tag="Dibujo"):
        DibujaGrid()
    with dpg.group(horizontal=True):
        Boton("Dibujar en ASCII", DibujaASCII).CrearBoton()
        Boton("Dibujar Matriz", DibujaMatriz).CrearBoton()
        Boton("Zoom In", ZoomIn).CrearBoton()
        Boton("Zoom Out", ZoomOut).CrearBoton()
        Boton("Guardar Imagen", GuardaImagen).CrearBoton()

    for color_name, color in Colores.items():
        Boton(color_name, CambioAColorElegido, color_name).CrearBoton()

dpg.create_viewport(title='Pixel Art', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
