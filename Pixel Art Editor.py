import dearpygui.dearpygui as dpg

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
 #Colores a representar, en RGB
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
 #Valores en la matriz de cada color 
ColorActual = Colores["Negro"]
grid = [[Colores["Blanco"] for _ in range(WIDTH)] for _ in range(HEIGHT)]

def DibujaGrid():
    dpg.delete_item("Dibujo", children_only=True)  # Elimina los dibujos anteriores, children_only=True determina que solo el dibujo se borra, no el area de dibujo
    for y in range(HEIGHT):
        for x in range(WIDTH): #Los loops enlazados iteran sobre si mismos en el grid
            dpg.draw_rectangle([x * CELL_SIZE, y * CELL_SIZE],
                               [(x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE],
                               color=(0, 0, 0, 255), fill=grid[y][x], parent="Dibujo")
    # Dibuja verticales de arriba a abajo
    for x in range(WIDTH + 1):
        dpg.draw_line([x * CELL_SIZE, 0], [x * CELL_SIZE, HEIGHT * CELL_SIZE], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")
    for y in range(HEIGHT + 1): # Dsibuja horizontales de izquierda a derecha
        dpg.draw_line([0, y * CELL_SIZE], [WIDTH * CELL_SIZE, y * CELL_SIZE], color=(0, 0, 0, 255), thickness=1, parent="Dibujo")

def ClickPosicion(sender, app_data, user_data): #dpg.get_mouse_pos(local=True) Verifica la posicion actual del mouse, retorna tupla con x,y
    mouse_pos = dpg.get_mouse_pos(local=True)
    x = int(mouse_pos[0] // CELL_SIZE) #La posicion del mouse relativa con el grid
    y = int(mouse_pos[1] // CELL_SIZE)
    if 0 <= x < WIDTH and 0 <= y < HEIGHT: #Chequea si esta en el grid
        grid[y][x] = ColorActual
        DibujaGrid()

def CambioAColorElegido(sender, app_data, user_data): #Actualiza el color actual por el seleccionado por el usuario
    global ColorActual
    ColorActual = Colores[user_data]

def DibujaMatriz(): #Funcion que muestra (DE MOMENTO) en consola la matriz
    matrix = [[ValoresColores[grid[y][x]] for x in range(WIDTH)] for y in range(HEIGHT)]
    for row in matrix:
        print(" ".join(map(str, row)))

def DibujaASCII(): #Funcion que muestra (DE MOMENTO) en consola el ascii
    ascii_map = {0: ' ', 1: '.', 2: ':', 3: '-', 4: '%', 5: "¡", 6: "&", 7: "$", 8: "%", 9: "@"}
    matrix = [[ValoresColores[grid[y][x]] for x in range(WIDTH)] for y in range(HEIGHT)]
    for row in matrix:
        print("".join(ascii_map[val] for val in row))

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

DibujaGrid()

dpg.create_viewport(title='Pixel Art Editor', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

#SEBAS WAPO
#ARRIBA EL SAPRISSA