import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import os, random

# =============== LOAD IMAGES ================
def loadImagesByName(folderPath):
    """
    Carga todas las imágenes (PNG, JPG, JPEG) de la carpeta dada.
    Devuelve un diccionario { "value color": PhotoImage, ... }
    y también la imagen para el reverso (back.png) si existe.
    """
    imageDict = {}
    backImage = None
    for filename in sorted(os.listdir(folderPath)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(folderPath, filename)
            base, _ = os.path.splitext(filename)  # p.ej. "2 amarillo"
            if base.lower() == "back":
                # Imagen del reverso
                backImg = Image.open(filepath)
                backImage = ImageTk.PhotoImage(backImg)
            else:
                # Imagen normal
                img = Image.open(filepath)
                photo = ImageTk.PhotoImage(img)
                imageDict[base] = photo
    return imageDict, backImage

# =============== CARD ================
class Card:
    def __init__(self, color, value):
        self.color = color  # p.ej. "rojo", "amarillo", "negro"
        self.value = value  # p.ej. "8", "+2", "salto", "reversa", "comodin", "+4"
        if value.isdigit():
            self.cardType = "Número"
        else:
            self.cardType = "Acción"
        self.image = None

    def __repr__(self):
        return f"{self.value} {self.color}"

# =============== DECK ================
class Deck:
    def __init__(self, imageDict):
        self.cards = []
        numerosYEspeciales = [
            "0","1","1","2","2","3","3","4","4","5","5",
            "6","6","7","7","8","8","9","9","+2","+2","salto","salto","reversa","reversa"
        ]
        colores = ["azul", "rojo", "amarillo", "verde"]
        comodines = ["+4", "comodin"]
        
        for val in numerosYEspeciales:
            for col in colores:
                self.cards.append(Card(col, val))
        for wild in comodines:
            for _ in range(4):
                self.cards.append(Card("negro", wild))
        
        # Asignar imagen a cada carta
        for card in self.cards:
            key = f"{card.value} {card.color}"
            if key in imageDict:
                card.image = imageDict[key]
            else:
                card.image = None

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
    def __init__(self, root, deck, numPlayers, backImage):
        self.root = root
        self.deck = deck
        self.players = {i: [] for i in range(numPlayers)}
        self.discardPile = []
        self.currentPlayer = 0
        self.numPlayers = numPlayers
        self.cardBackImage = backImage
        self.turnStep = 1
        self.accum = 0
        self.currentColor = None  # Color activo tras comodín
        # Para "UNO"
        self.unoButton = None
        self.unoLabel = None
        self.unoCountdown = 0
        self.unoTimerId = None
        self.unoCalled = False
        self.setupGame()

    def setupGame(self):
        for _ in range(7):
            for i in range(self.numPlayers):
                self.players[i].append(self.deck.popCard())
        firstCard = self.deck.popCard()
        self.discardPile.append(firstCard)
        # Definir color activo
        if firstCard.color != "negro":
            self.currentColor = firstCard.color
        else:
            # Si la primera carta es comodín, elegimos un color al azar
            self.currentColor = random.choice(["azul","rojo","amarillo","verde"])
        print("Initial Discard Pile:", firstCard)
        
        self.createWidgets()
        self.updateBoard()
        self.printCurrentCard()

    def evaluateStep(self, step, currentPlayer):
        if (step > 0) and (currentPlayer + step >= self.numPlayers):
            currentPlayer = currentPlayer - self.numPlayers
        if (step < 0) and (currentPlayer + step < 0):
            currentPlayer = self.numPlayers + currentPlayer
        currentPlayer += step
        if abs(step) >= 2:
            step = int(step / 2)
        print(f"After evaluating step => step={step}, currentPlayer={currentPlayer}")
        return step, currentPlayer

    def applyEffects(self, card, step):
        if card.value == "salto":
            step *= 2
        if card.value == "reversa":
            step = -step
        if card.value == "+2":
            self.accum += 2
        elif card.value == "+4":
            self.accum += 4
        print(f"After applying effects => step={step}, accum={self.accum}")
        return step

    def checkWinCondition(self):
        for p in range(self.numPlayers):
            if len(self.players[p]) == 0:
                if p == 0:
                    winnerText = "You have won!"
                else:
                    winnerText = f"Player {p} (AI) has won!"
                answer = messagebox.askyesno("Game Over", f"{winnerText}\nPlay again?")
                if answer:
                    self.root.destroy()
                    main()  # Reiniciar
                else:
                    self.root.destroy()
                return

    def startUnoCountdown(self):
        self.unoCalled = False
        self.unoCountdown = 5
        if self.unoLabel is None:
            self.unoLabel = tk.Label(self.root, text="Time to call UNO: 5", fg="red", font=("Arial", 14))
            self.unoLabel.pack(pady=5)
        else:
            self.unoLabel.config(text="Time to call UNO: 5")
            self.unoLabel.pack(pady=5)
        if self.unoButton is None:
            self.unoButton = tk.Button(self.root, text="Cantar UNO", bg="yellow", command=self.callUnoNow)
            self.unoButton.pack(pady=5)
        else:
            self.unoButton.config(state=tk.NORMAL)
            self.unoButton.pack(pady=5)
        self.unoCountdownTick()

    def unoCountdownTick(self):
        if self.unoCountdown > 0:
            self.unoCountdown -= 1
            self.unoLabel.config(text=f"Time to call UNO: {self.unoCountdown}")
            self.unoTimerId = self.root.after(1000, self.unoCountdownTick)
        else:
            if not self.unoCalled:
                # Penalizar con 1 carta
                if not self.deck.isEmpty():
                    c = self.deck.popCard()
                    self.players[0].append(c)
                    print("Penalty for not calling UNO:", c)
            self.hideUnoWidgets()

    def callUnoNow(self):
        self.unoCalled = True
        messagebox.showinfo("UNO!", "¡Has cantado UNO a tiempo!")
        self.hideUnoWidgets()

    def hideUnoWidgets(self):
        if self.unoLabel:
            self.unoLabel.pack_forget()
        if self.unoButton:
            self.unoButton.pack_forget()
        if self.unoTimerId:
            self.root.after_cancel(self.unoTimerId)
        self.unoTimerId = None
        self.unoCountdown = 0

    def createWidgets(self):
        self.root.title("UNO: +2/+4 Chain, Color Lock, UNO Countdown, Replay")
        self.infoFrame = tk.Frame(self.root)
        self.infoFrame.pack(pady=5)
        
        self.humanLabel = tk.Label(self.infoFrame, text="You: 0 cards")
        self.humanLabel.pack(side=tk.LEFT, padx=10)
        self.deckLabel = tk.Label(self.infoFrame, text=f"Draw Pile: {len(self.deck.cards)} cards")
        self.deckLabel.pack(side=tk.LEFT, padx=10)
        self.discardInfoLabel = tk.Label(self.infoFrame, text="Discard Pile:")
        self.discardInfoLabel.pack(side=tk.LEFT, padx=10)
        
        self.currentColorLabel = tk.Label(self.infoFrame, text=f"Current Color: {self.currentColor}")
        self.currentColorLabel.pack(side=tk.LEFT, padx=10)
        
        self.aiLabels = {}
        for i in range(1, self.numPlayers):
            lbl = tk.Label(self.infoFrame, text=f"AI {i}: {len(self.players[i])} cards")
            lbl.pack(side=tk.LEFT, padx=10)
            self.aiLabels[i] = lbl
        
        self.playArea = tk.Frame(self.root)
        self.playArea.pack(pady=10)
        
        self.deckButton = tk.Button(self.playArea, text="Draw", image=self.cardBackImage, command=self.drawCard)
        self.deckButton.grid(row=0, column=0, padx=30)
        
        self.discardCardLabel = tk.Label(self.playArea)
        self.discardCardLabel.grid(row=0, column=1, padx=10)
        
        self.handContainer = tk.Frame(self.root)
        self.handContainer.pack(pady=10, fill=tk.X)
        
        self.handCanvas = tk.Canvas(self.handContainer, width=600, height=180, bg="white")
        self.handCanvas.pack(side=tk.TOP, fill=tk.X, expand=True)
        
        self.handScrollbar = tk.Scrollbar(self.handContainer, orient="horizontal", command=self.handCanvas.xview)
        self.handScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.handCanvas.configure(xscrollcommand=self.handScrollbar.set)
        self.handInnerFrame = tk.Frame(self.handCanvas, bg="white")
        self.handInnerFrameWindow = self.handCanvas.create_window((0,0), window=self.handInnerFrame, anchor="nw")
        self.handInnerFrame.bind("<Configure>", self._onFrameConfigure)

    def _onFrameConfigure(self, event=None):
        self.handCanvas.configure(scrollregion=self.handCanvas.bbox("all"))
        self.root.update_idletasks()
        canvasWidth = self.handCanvas.winfo_width()
        frameWidth = self.handInnerFrame.winfo_reqwidth()
        xOffset = (canvasWidth - frameWidth) // 2 if frameWidth < canvasWidth else 0
        self.handCanvas.coords(self.handInnerFrameWindow, xOffset, 0)

    def updateBoard(self):
        topCard = self.discardPile[-1]
        if topCard.image:
            self.discardCardLabel.config(image=topCard.image)
            self.discardCardLabel.image = topCard.image
        else:
            self.discardCardLabel.config(text=str(topCard))
        self.printCurrentCard()
        
        for widget in self.handInnerFrame.winfo_children():
            widget.destroy()
        for idx, card in enumerate(self.players[0]):
            btn = tk.Button(self.handInnerFrame, image=card.image, command=lambda i=idx: self.humanPlay(i))
            btn.image = card.image
            btn.pack(side=tk.LEFT, padx=5)
        
        self.humanLabel.config(text=f"You: {len(self.players[0])} cards")
        self.deckLabel.config(text=f"Draw Pile: {len(self.deck.cards)} cards")
        
        # Actualizamos la IA
        for i in range(1, self.numPlayers):
            self.aiLabels[i].config(text=f"AI {i}: {len(self.players[i])} cards")
        
        # Actualizamos currentColor
        self.currentColorLabel.config(text=f"Current Color: {self.currentColor}")
        
        self._onFrameConfigure()
        self.checkWinCondition()
        
        # Lógica UNO
        if len(self.players[0]) == 1:
            if not self.unoTimerId:
                self.startUnoCountdown()
        else:
            self.hideUnoWidgets()

    def printCurrentCard(self):
        topCard = self.discardPile[-1]
        if topCard.color == "negro":
            print("Current card in play:", f"{topCard.value} {self.currentColor}")
        else:
            print("Current card in play:", topCard)

    def chooseColorDialog(self):
        colorWindow = tk.Toplevel(self.root)
        colorWindow.title("Choose a Color")
        chosen = [None]
        def selectColor(col):
            chosen[0] = col
            colorWindow.destroy()
        tk.Label(colorWindow, text="Choose a color for the Wild Card:").pack(pady=10)
        for c in ["azul", "rojo", "amarillo", "verde"]:
            btn = tk.Button(colorWindow, text=c, width=10, command=lambda col=c: selectColor(col))
            btn.pack(pady=5)
        colorWindow.transient(self.root)
        colorWindow.grab_set()
        self.root.wait_window(colorWindow)
        return chosen[0]

    def humanPlay(self, cardIndex):
        card = self.players[0][cardIndex]
        topCard = self.discardPile[-1]
        # Determinamos el color activo
        activeColor = self.currentColor if topCard.color == "negro" else topCard.color
        
        print(f"Human selected: {card}")
        
        # 1) Si accum>0 => SOLO se puede jugar +2/+4
        #    * si es +4, color no importa
        #    * si es +2, color debe coincidir con activeColor
        if self.accum > 0:
            if card.value == "+4":
                pass  # siempre válido
            elif card.value == "+2" and card.color == activeColor:
                pass  # válido
            else:
                messagebox.showinfo("Invalid Move", f"You must respond with +2 of color {activeColor} or +4.")
                return
        else:
            # accum == 0 => validación normal:
            #  comodín => siempre válido (elegir color)
            #  o coincide color con activeColor
            #  o coincide valor con topCard.value
            if card.color == "negro":
                valid = True
            elif card.color == activeColor or card.value == topCard.value:
                valid = True
            else:
                valid = False
            if not valid:
                messagebox.showinfo("Invalid Move", "You cannot play that card.")
                return
        
        # Si es comodín, pedir color
        if card.color == "negro":
            chosenColor = self.chooseColorDialog()
            if not chosenColor:
                return
            card.color = chosenColor
            self.currentColor = chosenColor
            print(f"Human changed wild color to {chosenColor}")
        else:
            # Si se juega +2 con accum>0, ya verificamos que color == activeColor
            # o si accum==0 y color coincide, actualizamos currentColor
            self.currentColor = card.color
        
        print(f"Human plays: {card}")
        self.discardPile.append(card)
        self.players[0].pop(cardIndex)
        
        self.turnStep = self.applyEffects(card, self.turnStep)
        self.turnStep, self.currentPlayer = self.evaluateStep(self.turnStep, self.currentPlayer)
        self.updateBoard()
        self.root.after(1000, self.aiTurn)

    def drawCard(self):
        if self.accum > 0:
            # come accum
            if self.deck.isEmpty():
                messagebox.showinfo("Deck Empty", "No more cards to draw.")
                return
            print(f"Human cannot respond => draws {self.accum} cards.")
            for _ in range(self.accum):
                if not self.deck.isEmpty():
                    self.players[0].append(self.deck.popCard())
            self.accum = 0
            # reset discard
            if not self.deck.isEmpty():
                newTop = self.deck.popCard()
                self.discardPile[-1] = newTop
                print("Discard pile reset to:", newTop)
                if newTop.color != "negro":
                    self.currentColor = newTop.color
                else:
                    self.currentColor = random.choice(["azul","rojo","amarillo","verde"])
            else:
                print("Deck empty, cannot reset discard pile.")
            self.turnStep, self.currentPlayer = self.evaluateStep(self.turnStep, self.currentPlayer)
            self.updateBoard()
            self.root.after(1000, self.aiTurn)
        else:
            if self.deck.isEmpty():
                messagebox.showinfo("Empty Deck", "No more cards to draw.")
                return
            newCard = self.deck.popCard()
            self.players[0].append(newCard)
            print("Human draws:", newCard)
            topCard = self.discardPile[-1]
            activeColor = self.currentColor if topCard.color == "negro" else topCard.color
            
            # Chequear si la carta es jugable
            if newCard.color == "negro":
                canPlay = True
            elif newCard.color == activeColor or newCard.value == topCard.value:
                canPlay = True
            else:
                canPlay = False
            
            if canPlay:
                messagebox.showinfo("Draw + Play", f"You drew a playable card ({newCard}). It will be played now.")
                if newCard.color == "negro":
                    chosenColor = self.chooseColorDialog()
                    if not chosenColor:
                        return
                    newCard.color = chosenColor
                    self.currentColor = chosenColor
                    print(f"Human changed wild color to {chosenColor}")
                print(f"Human plays after draw: {newCard}")
                self.players[0].remove(newCard)
                self.discardPile.append(newCard)
                self.turnStep = self.applyEffects(newCard, self.turnStep)
                self.turnStep, self.currentPlayer = self.evaluateStep(self.turnStep, self.currentPlayer)
                self.updateBoard()
                self.root.after(1000, self.aiTurn)
            else:
                messagebox.showinfo("Draw", "You cannot play that card. Turn lost.")
                print("Human cannot play the drawn card => turn lost.")
                self.turnStep, self.currentPlayer = self.evaluateStep(self.turnStep, self.currentPlayer)
                self.updateBoard()
                self.root.after(1000, self.aiTurn)

    def aiTurn(self):
        if self.numPlayers < 2:
            return
        if self.currentPlayer >= self.numPlayers:
            self.currentPlayer %= self.numPlayers
        if self.currentPlayer == 0:
            return
        
        print(f"AI Turn => Player {self.currentPlayer}, accum={self.accum}")
        
        topCard = self.discardPile[-1]
        activeColor = self.currentColor if topCard.color == "negro" else topCard.color
        
        if self.accum > 0:
            # Buscar +2 / +4
            foundChain = None
            for i, card in enumerate(self.players[self.currentPlayer]):
                # +4 siempre válido, +2 solo si color == activeColor
                if card.value == "+4":
                    foundChain = (i, card)
                    break
                elif card.value == "+2" and card.color == activeColor:
                    foundChain = (i, card)
                    break
            if foundChain:
                i, chainCard = foundChain
                print(f"AI chains with {chainCard}, accum={self.accum}")
                self.players[self.currentPlayer].pop(i)
                # Si es comodín, IA elige color
                if chainCard.value == "+4":
                    chainCard.color = random.choice(["azul","rojo","amarillo","verde"])
                    self.currentColor = chainCard.color
                    print(f"AI chooses color {chainCard.color} for +4")
                else:
                    # +2 => color ya está en la carta
                    self.currentColor = chainCard.color
                self.discardPile.append(chainCard)
                self.turnStep = self.applyEffects(chainCard, self.turnStep)
                self.turnStep, self.currentPlayer = self.evaluateStep(self.turnStep, self.currentPlayer)
                self.updateBoard()
                self.root.after(1000, self.aiTurn)
                return
            else:
                # No puede encadenar => come accum
                print(f"AI cannot chain => draws {self.accum} cards.")
                for _ in range(self.accum):
                    if not self.deck.isEmpty():
                        self.players[self.currentPlayer].append(self.deck.popCard())
                self.accum = 0
                # reset discard
                if not self.deck.isEmpty():
                    newTop = self.deck.popCard()
                    self.discardPile[-1] = newTop
                    print("Discard pile reset to:", newTop)
                    if newTop.color != "negro":
                        self.currentColor = newTop.color
                    else:
                        self.currentColor = random.choice(["azul","rojo","amarillo","verde"])
                else:
                    print("Deck empty, cannot reset discard pile.")
                self.turnStep, self.currentPlayer = self.evaluateStep(self.turnStep, self.currentPlayer)
                self.updateBoard()
                self.root.after(1000, self.aiTurn)
        else:
            # Jugada normal
            validIndex = None
            for i, card in enumerate(self.players[self.currentPlayer]):
                if card.color == "negro":
                    validIndex = i
                    break
                elif (card.color == activeColor) or (card.value == self.discardPile[-1].value):
                    validIndex = i
                    break
            if validIndex is not None:
                card = self.players[self.currentPlayer].pop(validIndex)
                print(f"AI plays: {card}")
                if card.color == "negro":
                    chosen = random.choice(["azul","rojo","amarillo","verde"])
                    card.color = chosen
                    self.currentColor = chosen
                    print(f"AI chooses color {chosen} for wild")
                else:
                    self.currentColor = card.color
                self.discardPile.append(card)
                self.turnStep = self.applyEffects(card, self.turnStep)
                self.turnStep, self.currentPlayer = self.evaluateStep(self.turnStep, self.currentPlayer)
            else:
                # No hay carta válida => roba 1
                if not self.deck.isEmpty():
                    newCard = self.deck.popCard()
                    self.players[self.currentPlayer].append(newCard)
                    print(f"AI draws 1 card: {newCard}")
                else:
                    print("Deck empty => AI cannot draw.")
                self.turnStep, self.currentPlayer = self.evaluateStep(self.turnStep, self.currentPlayer)
            self.updateBoard()
            if self.currentPlayer == 0:
                messagebox.showinfo("Turn", "Your turn!")
            else:
                self.root.after(1000, self.aiTurn)

def main():
    root = tk.Tk()
    root.title("UNO: +2/+4 Chain with Color Lock, UNO Countdown, Replay")
    folderPath = r"C:\Users\Juan Jose Restrepo\Desktop\Juego-UNO-Hecho-en-Python\unoGame\assets\cards"
    
    imageDict, backImage = loadImagesByName(folderPath)
    if backImage is None:
        from PIL import Image
        placeholder = Image.new("RGB", (80,125), color="gray")
        backImage = ImageTk.PhotoImage(placeholder)

    deck = Deck(imageDict)
    deck.shuffleDeck()
    
    numPlayers = simpledialog.askinteger("Players", "Enter number of players (2-4):", minvalue=2, maxvalue=4)
    if not numPlayers:
        numPlayers = 2
    
    game = UNOGame(root, deck, numPlayers, backImage)
    root.mainloop()

if __name__ == "__main__":
    main()
