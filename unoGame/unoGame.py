import tkinter as tk
from PIL import Image, ImageTk
import os, random

def loadFolderImages(folderPath):
    """
    Carga todas las imágenes (PNG, JPG, JPEG) de la carpeta indicada.
    Devuelve una lista de tuplas (filename, PhotoImage).
    """
    images = []
    for filename in sorted(os.listdir(folderPath)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(folderPath, filename)
            img = Image.open(filepath)
            photo = ImageTk.PhotoImage(img)
            images.append((filename, photo))
    return images

# =============== CARD ================
class Card:
    def __init__(self, color, value, cardType):
        self.color = color
        self.value = value
        self.cardType = cardType
        self.image = None
        self.name = f"{value} {color}"  # Valor por defecto; se sobrescribirá

    def __repr__(self):
        return f"{self.value} ({self.cardType}) {self.color}"

# =============== DECK ================
class Deck:
    """
    Crea el mazo de cartas UNO.
    - Se agregan cartas numéricas y especiales según listas definidas.
    - Se agregan comodines con color "negro".
    Luego se asignan las imágenes a cada carta de forma cíclica usando las imágenes cargadas de la carpeta.
    """
    def __init__(self, folderImages):
        self.cards = []
        numerosYEspeciales = ["0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5",
                               "6", "6", "7", "7", "8", "8", "9", "9",
                               "+2", "+2", "salto", "salto", "reversa", "reversa"]
        colores = ["azul", "rojo", "amarillo", "verde"]
        comodines = ["+4", "comodin"]

        # Agregar cartas numéricas y de acción para cada color
        for value in numerosYEspeciales:
            for color in colores:
                cardType = "Número" if value.isdigit() else "Acción"
                self.cards.append(Card(color, value, cardType))
        # Agregar cartas comodín (color "negro")
        for wild in comodines:
            for _ in range(4):
                self.cards.append(Card("negro", wild, "Acción"))
        
        # Asignar imágenes a cada carta de forma cíclica usando las imágenes de la carpeta
        numImages = len(folderImages)
        for i, card in enumerate(self.cards):
            filename, photo = folderImages[i % numImages]
            card.image = photo
            card.name = filename

    def shuffleDeck(self):
        random.shuffle(self.cards)
    
    def popCard(self):
        if self.cards:
            return self.cards.pop()
        return None
    
    def isEmpty(self):
        return len(self.cards) == 0

    def __repr__(self):
        return f"Deck with {len(self.cards)} cards"

# =============== UNO GAME ================
class UNOGame:
    def __init__(self, root):
        self.root = root
        self.deck = None
        self.players = {"human": [], "ai": []}
        self.discardPile = []

# =============== MAIN ================
def game(root):
    # Ruta a la carpeta donde están las cartas separadas
    folderPath = r"C:\Users\Juan Jose Restrepo\Desktop\Juego-UNO-Hecho-en-Python\unoGame\assets\cards"
    folderImages = loadFolderImages(folderPath)
    
    # Creamos el mazo usando las imágenes cargadas de la carpeta
    deck = Deck(folderImages)
    deck.shuffleDeck()
    print("====== FULL DECK ======")
    print(deck)
    
    # Mostramos la primera carta en la ventana principal
    firstCard = deck.popCard()
    root.title("Uno Game")
    root.geometry("400x400")
    
    if firstCard.image:
        etiqueta = tk.Label(root, image=firstCard.image)
    else:
        etiqueta = tk.Label(root, text=str(firstCard), font=("Arial", 24))
    etiqueta.pack(pady=20, padx=20)
    
    # Al hacer clic sobre la imagen, se imprime el nombre de la carta en la terminal
    etiqueta.bind("<Button-1>", lambda event: print(f"Card clicked: {firstCard.name}"))
    
    # Asignamos el mazo al juego (por si se usa más adelante)
    game_instance = UNOGame(root)
    game_instance.deck = deck
    
    root.mainloop()
    
def main():
    root = tk.Tk()
    game(root)

if __name__ == "__main__":
    main()
