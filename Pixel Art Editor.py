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

class Boton:
    def __init__(self, label, callback, user_data=None, width=100, height=30):
        self.label = label
        self.callback = callback
        self.user_data = user_data
        self.width = width
        self.height = height

    def CrearBoton(self):
        dpg.add_button(label=self.label, callback=self.callback, user_data=self.user_data, width=self.width, height=self.height)
        
class Matriz:
    def __init__(self, width, height, default_value=0):
        self.width = width
        self.height = height
        self.grid = [[default_value for c in range(width)] for c in range(height)]
        self.cell_size = CELL_SIZE

    @classmethod
    def LeerTXT(cls, filepath, width=WIDTH, height=HEIGHT, default_value=0):
        try:
            print(f"Attempting to open file at: {filepath}")
            with open(filepath, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            print(f"Error opening file: {e}")
            return None

        matriz = cls(width, height, default_value)
        for y, line in enumerate(lines):
            values = list(map(int, line.split()))
            for x, value in enumerate(values):
                if x < width and y < height:
                    matriz.grid[y][x] = value
        return matriz

    def ConvertirAGrid(self, colores_dict):
        return [[colores_dict.get(val, colores_dict[0]).ObtenerRGB() for val in fila] for fila in self.grid]

    def ImportarImagen(self, sender, app_data, user_data):
        DirectorioPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'matriz.txt')
        if os.path.exists(DirectorioPath):
            MatrizImportada = Matriz.LeerTXT(DirectorioPath, width=self.width, height=self.height)
            if MatrizImportada:
                self.grid = MatrizImportada.ConvertirAGrid(ValoresColores)
                self.DibujaGrid()
            else:
                print(f"Failed to import matrix from {DirectorioPath}")
        else:
            print(f"No se encontró el archivo {DirectorioPath}")
            
    def DibujaGrid(self):
        dpg.delete_item("Dibujo", children_only=True)
        for y in range(self.height):
            for x in range(self.width):
                dpg.draw_rectangle([x * self.cell_size, y * self.cell_size],
                                   [(x + 1) * self.cell_size, (y + 1) * self.cell_size],
                                   color=(0, 0, 0, 255), fill=self.grid[y][x], parent="Dibujo")
        for x in range(self.width + 1):
            dpg.draw_line([x * self.cell_size, 0], [x * self.cell_size, self.height * self.cell_size], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")
        for y in range(self.height + 1):
            dpg.draw_line([0, y * self.cell_size], [self.width * self.cell_size, y * self.cell_size], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")

    def MouseDragHandler(self,sender, app_data):
        self.ClickPosicion(sender, app_data, None)
        
    def ClickPosicion(self, sender, app_data, user_data):
        mouse_pos = dpg.get_mouse_pos()
        x = int(mouse_pos[0] // self.cell_size)
        y = int(mouse_pos[1] // self.cell_size)
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = ColorActual.ObtenerRGB()
            self.DibujaGrid()

    def ValoresColorANumero(self, rgb): 
        for num, color in ValoresColores.items():
            if color.ObtenerRGB() == rgb:
                return num
        return 0

    def DibujaMatriz(self):
        matriz = [[self.ValoresColorANumero(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)]
        for fila in matriz:
            print(" ".join(map(str, fila)))

    def DibujaASCII(self):
        matriz = [[self.ValoresColorANumero(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)]
        for fila in matriz:
            print("".join(DiccionarioASCII[val] for val in fila))

    def ZoomIn(self):
        if self.cell_size < MAX_CELL_SIZE:
            self.cell_size += 1
            self.DibujaGrid()

    def ZoomOut(self):
        if self.cell_size > MIN_CELL_SIZE:
            self.cell_size -= 1
            self.DibujaGrid()

    def GuardaImagen(self):
        grid_expandido = []
        for fila in self.grid:
            nueva_fila = []
            for color in fila:
                nueva_fila.extend([color[:3], color[:3]])
            grid_expandido.extend([nueva_fila, nueva_fila])
        
        pixel_data = np.array(grid_expandido, dtype=np.uint8)
        imagen = Image.fromarray(pixel_data)
        folder = os.path.dirname(os.path.abspath(__file__))
        DirectorioPath = os.path.join(folder, "PixelArt.png")
        TXTPath = os.path.join(folder, "PixelArt.txt")
        
        imagen.save(DirectorioPath)
        print(f"Imagen guardada en el directorio: {DirectorioPath}")

        matriz = [[self.ValoresColorANumero(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)]
        with open(TXTPath, 'w') as file:
            for fila in matriz:
                file.write(" ".join(map(str, fila)) + "\n")
        print(f"Matriz guardada en el directorio: TXTPath")

    def Altocontraste(self):
        for y in range(self.height):
            for x in range(self.width):
                valor = self.ValoresColorANumero(self.grid[y][x])
                if 0 <= valor <= 4:
                    self.grid[y][x] = ValoresColores[1].ObtenerRGB()
                elif 5 <= valor <= 9:
                    self.grid[y][x] = ValoresColores[9].ObtenerRGB()
        self.DibujaGrid()

    def Negativo(self):
        for y in range(self.height):
            for x in range(self.width):
                valor = self.ValoresColorANumero(self.grid[y][x])
                self.grid[y][x] = ValoresColores[9 - valor].ObtenerRGB()
        self.DibujaGrid()

    def Rotarderecha(self):
        filas = len(self.grid)
        columnas = len(self.grid[0])
        nueva_grid = [[None] * filas for _ in range(columnas)]
        for i in range(filas):
            for j in range(columnas):
                nueva_grid[j][filas - 1 - i] = self.grid[i][j]
        self.grid = nueva_grid
        self.DibujaGrid()

    def Rotarizquierda(self):
        filas = len(self.grid)
        columnas = len(self.grid[0])
        nueva_grid = [[None] * filas for _ in range(columnas)]
        for i in range(filas):
            for j in range(columnas):
                nueva_grid[filas - 1 - j][i] = self.grid[i][j]
        self.grid = nueva_grid
        self.DibujaGrid()

    def InvertirVertical(self):
        self.grid = self.grid[::-1]
        self.DibujaGrid()

    def InvertirHorizontal(self):
        self.grid = [fila[::-1] for fila in self.grid]
        self.DibujaGrid()

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

# Inicialización de la matriz
grid = [[Colores["Borrador"].ObtenerRGB() for r in range(WIDTH)] for r in range(HEIGHT)]
matriz = Matriz(WIDTH, HEIGHT, default_value=Colores["Borrador"].ObtenerRGB())
matriz.grid = grid

def CambioAColorElegido(sender, app_data, user_data):
    global ColorActual
    ColorActual = Colores[user_data]

# Dibuja la interfaz
dpg.create_context()

with dpg.font_registry():
    FuentePorDefecto = dpg.add_font("Roboto-Light.ttf", 20)
    FuenteSecundaria = dpg.add_font("Roboto-Light.ttf", 10)

with dpg.window(label="Pixel Art Editor", tag="Primary Window"):
    with dpg.group(horizontal=True):
        with dpg.group():
            with dpg.drawlist(width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, tag="Dibujo"):
                dpg.set_item_callback("Dibujo", matriz.ClickPosicion)

        with dpg.group():
            for NombreDeColor in Colores:
                Boton(label=NombreDeColor, callback=CambioAColorElegido, user_data=NombreDeColor).CrearBoton()

            Boton(label="Zoom In", callback=matriz.ZoomIn).CrearBoton()
            Boton(label="Zoom Out", callback=matriz.ZoomOut).CrearBoton()
            Boton(label="Mostrar Matriz", callback=matriz.DibujaMatriz, width=140).CrearBoton()
            Boton(label="Mostrar ASCII", callback=matriz.DibujaASCII, width=140).CrearBoton()
            Boton(label="Guardar Imagen", callback=matriz.GuardaImagen, width=140).CrearBoton()
            Boton(label="Alto contraste", callback=matriz.Altocontraste, width=140).CrearBoton()
            Boton(label="Negativo", callback=matriz.Negativo, width=140).CrearBoton()
            Boton(label="Rotar a la derecha", callback=matriz.Rotarderecha, width=140).CrearBoton()
            Boton(label="Rotar a la izquierda", callback=matriz.Rotarizquierda, width=140).CrearBoton()
            Boton(label="Invertir vertical", callback=matriz.InvertirVertical, width=140).CrearBoton()
            Boton(label="Invertir horizontal", callback=matriz.InvertirHorizontal, width=140).CrearBoton()
            Boton(label="Importar Imagen", callback=matriz.ImportarImagen).CrearBoton()
            dpg.bind_font(FuentePorDefecto)

matriz.DibujaGrid()
with dpg.handler_registry():
    dpg.add_mouse_drag_handler(callback=matriz.MouseDragHandler) #función de dpg que captura el click del mouse

dpg.create_viewport(title='Pixel Art Editor', width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
