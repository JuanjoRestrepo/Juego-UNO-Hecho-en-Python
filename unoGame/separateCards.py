import os
from PIL import Image

def main():
    # Ruta del sprite sheet y carpeta destino
    spritePath = r"C:\Users\Juan Jose Restrepo\Desktop\Juego-UNO-Hecho-en-Python\unoGame\assets\cartas.jpg"
    saveFolder = r"C:\Users\Juan Jose Restrepo\Desktop\Juego-UNO-Hecho-en-Python\unoGame\assets\cards"
    
    # Abrir el sprite sheet
    sheet = Image.open(spritePath)
    sheetWidth, sheetHeight = sheet.size
    
    # Cada carta: 10 columnas; altura fija de 125 píxeles
    cardSizeX = sheetWidth // 10
    cardSizeY = 125
    
    # Crear la carpeta destino si no existe
    os.makedirs(saveFolder, exist_ok=True)
    
    # ---------------------------------
    # Fila 1 (índice 0): rojas, valores "1,2,3,4,5,6,7,8,9,0"
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    row = 0
    for i, val in enumerate(values):
        col = i
        x1 = col * cardSizeX
        y1 = row * cardSizeY
        x2 = x1 + cardSizeX
        y2 = y1 + cardSizeY
        
        cardImage = sheet.crop((x1, y1, x2, y2))
        filename = f"{val} rojo.png"
        filepath = os.path.join(saveFolder, filename)
        cardImage.save(filepath)
        print(f"Guardada: {filename}")
    
    # ---------------------------------
    # Fila 2 (índice 1): amarillas
    row = 1
    for i, val in enumerate(values):
        col = i
        x1 = col * cardSizeX
        y1 = row * cardSizeY
        x2 = x1 + cardSizeX
        y2 = y1 + cardSizeY
        
        cardImage = sheet.crop((x1, y1, x2, y2))
        filename = f"{val} amarillo.png"
        filepath = os.path.join(saveFolder, filename)
        cardImage.save(filepath)
        print(f"Guardada: {filename}")
    
    # ---------------------------------
    # Fila 3 (índice 2): verdes
    row = 2
    for i, val in enumerate(values):
        col = i
        x1 = col * cardSizeX
        y1 = row * cardSizeY
        x2 = x1 + cardSizeX
        y2 = y1 + cardSizeY
        
        cardImage = sheet.crop((x1, y1, x2, y2))
        filename = f"{val} verde.png"
        filepath = os.path.join(saveFolder, filename)
        cardImage.save(filepath)
        print(f"Guardada: {filename}")
    
    # ---------------------------------
    # Fila 4 (índice 3): azules
    row = 3
    for i, val in enumerate(values):
        col = i
        x1 = col * cardSizeX
        y1 = row * cardSizeY
        x2 = x1 + cardSizeX
        y2 = y1 + cardSizeY
        
        cardImage = sheet.crop((x1, y1, x2, y2))
        filename = f"{val} azul.png"
        filepath = os.path.join(saveFolder, filename)
        cardImage.save(filepath)
        print(f"Guardada: {filename}")
    
    # ---------------------------------
    # Fila 5 (índice 4): Acciones para cada color
    # Suponemos que la fila 5 tiene 10 cartas y definimos manualmente los nombres
    row5 = 4
    row5Values = [
        ("salto", "rojo"), ("reversa", "rojo"), ("+2", "rojo"),
        ("salto", "amarillo"), ("reversa", "amarillo"), ("+2", "amarillo"),
        ("salto", "verde"), ("reversa", "verde"), ("+2", "verde"),
        ("salto", "azul")
    ]
    for i, (val, color) in enumerate(row5Values):
        col = i  # Asumimos que ocupan las 10 columnas
        x1 = col * cardSizeX
        y1 = row5 * cardSizeY
        x2 = x1 + cardSizeX
        y2 = y1 + cardSizeY
        
        cardImage = sheet.crop((x1, y1, x2, y2))
        filename = f"{val} {color}.png"
        filepath = os.path.join(saveFolder, filename)
        cardImage.save(filepath)
        print(f"Guardada: {filename}")
    
    # ---------------------------------
    # Fila 6 (índice 5): Resto de acciones y comodines
    # Queremos: "reversa azul", "+2 azul", "comodin", "+4"
    # Suponemos que en esta fila el sprite sheet tiene duplicados y definimos explícitamente las columnas a usar.
    row6 = 5
    # Especificamos los índices de columna donde se encuentran las cartas deseadas:
    # Por ejemplo, columna 0: "reversa azul", columna 1: "+2 azul", columna 2: "comodin", columna 4: "+4"
    row6Indices = [0, 1, 2, 4]
    row6Values = [
        ("reversa", "azul"),
        ("+2", "azul"),
        ("comodin", "negro"),
        ("+4", "negro")
    ]
    for idx, (val, color) in zip(row6Indices, row6Values):
        col = idx
        x1 = col * cardSizeX
        y1 = row6 * cardSizeY
        x2 = x1 + cardSizeX
        y2 = y1 + cardSizeY
        
        cardImage = sheet.crop((x1, y1, x2, y2))
        filename = f"{val} {color}.png"
        filepath = os.path.join(saveFolder, filename)
        cardImage.save(filepath)
        print(f"Guardada: {filename}")
    
    print("\nProceso finalizado. Todas las cartas guardadas en:", saveFolder)

if __name__ == "__main__":
    main()
