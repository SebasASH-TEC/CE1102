import dearpygui.dearpygui as dpg
import numpy as np
from PIL import Image
import math
import os

# Constantes
WIDTH, HEIGHT = 50, 50 #Cantidad de celdas del grid
CELL_SIZE = 10 #Tamano de cada celda del grid
MIN_CELL_SIZE = 5 #Tamano minimo de cada celda (Para el ZoomOut)
MAX_CELL_SIZE = 20 #Tamano maximo de cada celda (Para el ZoomIn)

#CLase que modela los colores a utilizar, con su espectro RGBA, y asocia cada color con valores (0-255) y numeros (0-9)
class Colores: 
    def __init__(self, color, R, G, B, a, num):
        self.color = color #Nombre del color
        self.r = R #Valor de cada tonalidad (24 bits, RGB)
        self.g = G
        self.b = B
        self.a = a #Alpha, ergo, la opacidad
        self.num = num

    def ObtenerRGB(self):
        return (self.r, self.g, self.b, self.a) #Brinda los valores de cada color

    def ObtenerNum(self): #Brinda el numero asociado a cada colore
        return self.num

#Esta es una clase ASCII que ayuda como base para representar en ASCII la matriz, por medio de la funcion MostrarASCII
class ASCII:
    def __init__(self, numero, simbolo):
        self.numero = numero
        self.simbolo = simbolo

    def ObtenerSimbolo(self):
        return self.simbolo

#Esta es una clase que modela los botones interactuables por el usuario
class Boton:
    def __init__(self, label, callback, user_data=None, width=100, height=30):
        self.label = label
        self.callback = callback
        self.user_data = user_data
        self.width = width
        self.height = height

    def CrearBoton(self):
        dpg.add_button(label=self.label, callback=self.callback, user_data=self.user_data, width=self.width, height=self.height)
#Clase principal        
class Matriz:
    def __init__(self, width, height, default_value=0):
        self.width = width
        self.height = height
        self.grid = [[default_value for c in range(width)] for c in range(height)]
        self.cell_size = CELL_SIZE

    @classmethod #Convierte una funcion a metodo de una clase
    def LeerTXT(cls, filepath, width=WIDTH, height=HEIGHT, default_value=0): #Funcion para leer el contenido del txt a importar
        try:
            print(f"Attempting to open file at: {filepath}")
            with open(filepath, 'r') as file:
                lines = file.readlines()
        except Exception as e: #Printea en caso de error
            print(f"Error opening file: {e}")
            return None

        matriz = cls(width, height, default_value) #Convierte a matriz el contenido del txt
        for y, line in enumerate(lines):            # Itera sobre las líneas leídas del archivo
            values = list(map(int, line.split()))  # Convierte cada línea en una lista de enteros
            for x, value in enumerate(values):      # Itera sobre los valores de cada línea
                if x < width and y < height:        # Asegura que los índices x e y están dentro de los límites de la matriz
                    matriz.grid[y][x] = value       # Asigna el valor a la posición correspondiente en la matriz
        return matriz

    def ConvertirAGrid(self, DiccionarioColores):
        return [[DiccionarioColores.get(val, DiccionarioColores[0]).ObtenerRGB() for val in fila] for fila in self.grid]

    def ImportarImagen(self, filepath): #Funcion que busca el txt llamado "matriz.txt", llama a LeerTXT, y utiliza la nueva matriz para importarla al grid
        if os.path.exists(filepath):
            MatrizImportada = Matriz.LeerTXT(filepath, width=self.width, height=self.height) # Si el archivo existe, lee su contenido usando la función LeerTXT y crea una nueva matriz
            if MatrizImportada:                                   # Verifica si la lectura y creación de la matriz fue exitosa
                self.grid = MatrizImportada.ConvertirAGrid(ValoresColores)  # Convierte la nueva matriz importada a un grid con colores utilizando el diccionario ValoresColores
                self.DibujaGrid()
            else:
                print(f"Failed to import matrix from {filepath}")
        else:
            print(f"No se encontró el archivo {filepath}")
    
    def ImportarImagenConNombre(self, sender, app_data, user_data): #Función para mostrar el popup y obtener el nombre del archivo
        dpg.show_item("PopupNombreArchivo")
            
    def DibujaGrid(self): #Dibuja la matriz sobre la que se hara el pixel art, con MxN = Altura*Ancho
        dpg.delete_item("Dibujo", children_only=True) #El children only se asegura de solo borrar ventanas secundarias, no la principal
        for y in range(self.height):
            for x in range(self.width): #For anidados para recorrer la matriz, dibujando las celdas
                dpg.draw_rectangle([x * self.cell_size, y * self.cell_size],
                                   [(x + 1) * self.cell_size, (y + 1) * self.cell_size], #Dibuja las celdas en del tamano del cell_size
                                   color=(0, 0, 0, 255), fill=self.grid[y][x], parent="Dibujo") #Color blanco por defecto, y la pone como ventana secundaria del Dibujo
        for x in range(self.width + 1):
            dpg.draw_line([x * self.cell_size, 0], [x * self.cell_size, self.height * self.cell_size], color=(0, 0, 0, 255), thickness=1, parent="Dibujo") #Dibuja las lineas de la matricula
        for y in range(self.height + 1):
            dpg.draw_line([0, y * self.cell_size], [self.width * self.cell_size, y * self.cell_size], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")

    def MouseDragHandler(self,sender, app_data): #Funcion que permite realizar dibujos fluidos, sin tener que clickear pixel por pixel
        self.ClickPosicion(sender, app_data, None)
        
    def ClickPosicion(self, sender, app_data, user_data): #Funcion que detecta el punto en que se esta clickeando
        mouse_pos = dpg.get_mouse_pos() #Función de dpg que regresa una tupla con la posición en "x" y "y" del mouse
        x = int(mouse_pos[0] // self.cell_size) #Posicion relativa al cell size
        y = int(mouse_pos[1] // self.cell_size)
        if 0 <= x < self.width and 0 <= y < self.height: #Verifica que este dentro de las dimensiones de la ventana 
            self.grid[y][x] = ColorActual.ObtenerRGB()
            self.DibujaGrid()

    def ValoresColorANumero(self, rgb): #Funcion de ayuda para el DibujaMatriz, convierte los colores a su numero asignado
        for num, color in ValoresColores.items():
            if color.ObtenerRGB() == rgb:
                return num
        return 0

    def DibujaMatriz(self):
        matriz = [[self.ValoresColorANumero(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)]
        
        if dpg.does_item_exist("MatrizWindow"): #Verifica si hay una ventana del mismo nombre, y la destruye
            dpg.delete_item("MatrizWindow")

        with dpg.window(label="Matriz", tag="MatrizWindow", width=700, height=600): #Crea la ventana secundaria para desplegar la matriz 
            for fila in matriz:
                dpg.add_text(" ".join(map(str, fila)))

    def DibujaASCII(self): #Identica a DibujaMatriz, pero con el diccionario ASCII
        matriz = [[self.ValoresColorANumero(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)] #convierte cada elemento del grid en un número asignado al color correspondiente
        if dpg.does_item_exist("ASCIIWindow"):
            dpg.delete_item("ASCIIWindow")
            
        with dpg.window(label="ASCII", tag="ASCIIWindow", width=700, height=600):
            for fila in matriz:
                dpg.add_text("".join(DiccionarioASCII[val] for val in fila))

    def ZoomIn(self):
        if self.cell_size < MAX_CELL_SIZE:
            self.cell_size += 1
            self.DibujaGrid()

    def ZoomOut(self):
        if self.cell_size > MIN_CELL_SIZE:
            self.cell_size -= 1
            self.DibujaGrid()

    def GuardaImagen(self):
        grid_expandido = [] #Lista vacia para guardar la matriz
        for fila in self.grid:
            nueva_fila = []
            for color in fila:
                nueva_fila.extend([color[:3], color[:3]])
            grid_expandido.extend([nueva_fila, nueva_fila]) #Duplica cada pixel, para aumentar la resolucion de la imagen resultante
        
        pixel_data = np.array(grid_expandido, dtype=np.uint8) #Convierte el grid en un array de numpy
        imagen = Image.fromarray(pixel_data) #Utiliza el modulo image para generar la imagen a traves del array
        folder = os.path.dirname(os.path.abspath(__file__)) #Direccion para guardarla
        DirectorioPath = os.path.join(folder, "PixelArt.png")
        TXTPath = os.path.join(folder, "PixelArt.txt")
        
        imagen.save(DirectorioPath)
        print(f"Imagen guardada en el directorio: {DirectorioPath}")

        matriz = [[self.ValoresColorANumero(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)] #Realiza un proceso similar a MostrarMatriz, pero lo escribe en un txt, en lugar de desplegarlo
        with open(TXTPath, 'w') as file:
            for fila in matriz:
                file.write(" ".join(map(str, fila)) + "\n")
        print(f"Matriz guardada en el directorio: TXTPath")

    def AltoContraste(self):
        for y in range(self.height):
            for x in range(self.width):
                valor = self.ValoresColorANumero(self.grid[y][x])
                if 0 <= valor <= 4: #Compara los valores actuales, si es igual o menor a 4, se vuelve color 1, si no, se vuelve 9
                    self.grid[y][x] = ValoresColores[1].ObtenerRGB()
                elif 5 <= valor <= 9:
                    self.grid[y][x] = ValoresColores[9].ObtenerRGB()
        self.DibujaGrid()

    def Negativo(self): #Convierte cada valor en su extremo opuesto
        for y in range(self.height):
            for x in range(self.width):
                valor = self.ValoresColorANumero(self.grid[y][x])
                self.grid[y][x] = ValoresColores[9 - valor].ObtenerRGB()
        self.DibujaGrid()

    def RotarDerecha(self):
        filas = len(self.grid)
        columnas = len(self.grid[0])
        NuevaGrid = [[None] * filas for _ in range(columnas)]
        for i in range(filas):
            for j in range(columnas):
                NuevaGrid[j][filas - 1 - i] = self.grid[i][j]  # toma el elemento en la posición [i][j] de la matriz original y lo coloca en la posición [j][filas - 1 - i] en la nueva matriz, rota la matriz 90 grados hacia la derecha.
        self.grid = NuevaGrid
        self.DibujaGrid()

    def RotarIzquierda(self):
        filas = len(self.grid)
        columnas = len(self.grid[0])
        NuevaGrid = [[None] * filas for _ in range(columnas)]
        for i in range(filas):
            for j in range(columnas):
                NuevaGrid[filas - 1 - j][i] = self.grid[i][j] #rota 90 grados la matriz hacia la izquierda
        self.grid = NuevaGrid
        self.DibujaGrid()

    def InvertirVertical(self):
        self.grid = self.grid[::-1] #Invierte la lista
        self.DibujaGrid()

    def InvertirHorizontal(self):
        self.grid = [fila[::-1] for fila in self.grid]
        self.DibujaGrid()

    def Limpiar(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = ValoresColores[0].ObtenerRGB() #Convierte todos los valores a 0
        self.DibujaGrid()
    
    def DibujaCirculo(self, X, Y, Radio):
        for y in range(self.height):
            for x in range(self.width): #Convierte los puntos de la matriz, especificados por el usuario, en el color actual seleccionado
                Distancia = math.sqrt((x - X)**2 + (y - Y)**2)
                if Radio - 0.5 <= Distancia <=Radio + 0.5:
                    self.grid[y][x] = ColorActual.ObtenerRGB()
        self.DibujaGrid()
    
    def DibujaRectangulo(self, X, Y, Ancho, Alto):
        for y in range(self.height):
            for x in range(self.width):
                if (x == X or x == X + Ancho - 1) and (Y <= y <= Y +Alto - 1):
                    self.grid[y][x] = ColorActual.ObtenerRGB()
                if (y == Y or y == Y + Alto - 1) and (X <= x <= X + Ancho - 1):
                    self.grid[y][x] = ColorActual.ObtenerRGB()
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
def DibujarCirculoCallback(sender, app_data, user_data):
    X = int(dpg.get_value("CirculoX"))
    Y = int(dpg.get_value("CirculoY"))
    Radio = int(dpg.get_value("CirculoRadio"))
    matriz.DibujaCirculo(X, Y, Radio)

def DibujarRectanguloCallback(sender, app_data, user_data):
    X = int(dpg.get_value("RectanguloX"))
    Y = int(dpg.get_value("RectanguloY"))
    Ancho = int(dpg.get_value("Ancho"))
    Alto = int(dpg.get_value("Alto"))
    matriz.DibujaRectangulo(X, Y, Ancho, Alto)

def ImportarImagenCallback(sender, app_data, user_data):
    path = dpg.get_value("NombreArchivo")
    matriz.ImportarImagen(path)
    dpg.hide_item("PopupNombreArchivo")
    
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

with dpg.font_registry():                                    #Función para establecer la fuente
    FuentePorDefecto = dpg.add_font("Roboto-Light.ttf", 20)    #Establece a Roboto-Light como fuente principal
    FuenteSecundaria = dpg.add_font("Roboto-Light.ttf", 10)

with dpg.window(label="Pixel Art Editor", tag="Primary Window"):   #Función de dpg la cual crea una ventana  a partir de un contexto
    with dpg.group(horizontal=True):                                # Establece que el grupo de los botones será horizontal
        with dpg.group():                                           
            with dpg.drawlist(width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, tag="Dibujo"):    #utiliza los valores predeterminados para las dimensiones del lienzo 
                dpg.set_item_callback("Dibujo", matriz.ClickPosicion)                               #establece cuando el mouse se posicione sobre el lienzo, llame la funcion clickposicion

        with dpg.group():                                                                   #se crea el grupo de botones de los colores
            for NombreDeColor in Colores:                                                   #llama a la instancia Colores para luego llamar a la instancia Botones, para crear los botones con el método CrearBoton
                Boton(label=NombreDeColor, callback=CambioAColorElegido, user_data=NombreDeColor).CrearBoton()

            Boton(label="Zoom In", callback=matriz.ZoomIn).CrearBoton()
            Boton(label="Zoom Out", callback=matriz.ZoomOut).CrearBoton()
            Boton(label="Mostrar Matriz", callback=matriz.DibujaMatriz, width=140).CrearBoton()
            Boton(label="Mostrar ASCII", callback=matriz.DibujaASCII, width=140).CrearBoton()
            
            Boton(label="Rotar a la derecha", callback=matriz.RotarDerecha, width=150).CrearBoton()
            Boton(label="Rotar a la izquierda", callback=matriz.RotarIzquierda, width=150).CrearBoton()
            Boton(label="Invertir vertical", callback=matriz.InvertirVertical, width=140).CrearBoton()
            Boton(label="Invertir horizontal", callback=matriz.InvertirHorizontal, width=140).CrearBoton()
            
            
            dpg.bind_font(FuentePorDefecto)
        with dpg.group():
            Boton(label="Limpiar canva", callback=matriz.Limpiar, width=140).CrearBoton()
            Boton(label="Círculo", callback=lambda: dpg.show_item("PopUpValoresCirculo"), width=140).CrearBoton()
            Boton(label="Rectángulo", callback=lambda: dpg.show_item("PopUpValoresRectangulo"), width=140).CrearBoton()
            Boton(label="Alto contraste", callback=matriz.AltoContraste, width=140).CrearBoton()
            Boton(label="Negativo", callback=matriz.Negativo, width=140).CrearBoton()
            Boton(label="Importar Imagen", callback=matriz.ImportarImagenConNombre, width=140).CrearBoton()
            Boton(label="Guardar Imagen", callback=matriz.GuardaImagen, width=140).CrearBoton()
        
        with dpg.window(label="Nombre del Archivo", modal=True, show=False, tag="PopupNombreArchivo"):
            dpg.add_input_text(label="Nombre del Archivo", tag="NombreArchivo", default_value="matriz.txt")
            dpg.add_button(label="Importar", callback=ImportarImagenCallback)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.hide_item("PopupNombreArchivo"))

        with dpg.window(label="Dimensiones", modal=True, show=False, tag="PopUpValoresCirculo"):
            dpg.add_input_int(label="X", tag="CirculoX", default_value=25)
            dpg.add_input_int(label="Y", tag="CirculoY", default_value=25)
            dpg.add_input_int(label="Radio", tag="CirculoRadio", default_value=10)
            dpg.add_button(label="Dibujar", callback=DibujarCirculoCallback)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.hide_item("PopUpValoresCirculo"))
        
        with dpg.window(label="Dimensiones", modal=True, show=False, tag="PopUpValoresRectangulo"):
            dpg.add_input_int(label="X de origen", tag="RectanguloX", default_value=10)
            dpg.add_input_int(label="Y de origen", tag="RectanguloY", default_value=10)
            dpg.add_input_int(label="Ancho", tag="Ancho", default_value=20)
            dpg.add_input_int(label="Alto", tag="Alto", default_value=15)
            dpg.add_button(label="Dibujar", callback=DibujarRectanguloCallback)
            dpg.add_button(label="Cancelar", callback=lambda: dpg.hide_item("PopUpValoresRectangulo"))

with dpg.handler_registry():
    dpg.add_mouse_drag_handler(callback=matriz.MouseDragHandler) #función de dpg que captura el click del mouse

matriz.DibujaGrid()
dpg.create_viewport(title='Pixel Art Editor', width=900, height=750)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True) #Establece la ventana secundaria que estará dentro de la ventana principal
dpg.start_dearpygui()
dpg.destroy_context() #Función de dpg que finaliza la ejecución de la interfaz gráfica
