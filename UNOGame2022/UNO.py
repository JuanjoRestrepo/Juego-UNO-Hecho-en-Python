import pygame, random, os, sys

main_dir = os.path.split(os.path.abspath(__file__))[0]
os.environ['SDL_VIDEO_CENTERED'] = '1'

class Button: # Con esta clase crearemos una colección de botones con el color, coordenadas y texto que definamos

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = (self.x, self.y, self.w, self.h)
        self.color = []
        self.text = []

    def contains_point(self, point):
        """Return True if my sprite rectangle contains point pt """
        (my_x, my_y) = self.x, self.y
        my_width = self.w
        my_height = self.h
        (x, y) = point
        return ( x >= my_x and x < my_x + my_width and y >= my_y and y < my_y + my_height)
    

class Text:
    
    def __init__(self, x, y, text):
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 48)
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.text = self.font.render(text.format(), True, (255,255,255))
            

class CardSprite: # Vamos a cargar una imagen que contiene todas las cartas.
                  # Esta imagen es un objeto diferente a la carta, por tanto tendrá su propia clase
    
    def __init__(self): # Cargamos una lista de coordenadas donde están las cartas
        #self.sheet = pygame.image.load(r"C:/Users/ferri/AppData/Local/Programs/Python/Python38/Python as a CS/UNO/Copia UNO.jpg")
        self.sheet = pygame.image.load(os.path.join(main_dir, 'UNO', "Copia UNO.jpg"))
        self.x = self.sheet.get_width() # 800
        self.y = self.sheet.get_height() # 882
        
    def load_grid_images(self):
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size
        sprite_rects = []
        cardheighty = 0
        cardwidthx = 0
        cardsizex = self.x // 10
        cardsizey = 125
        for card in range(56): # El rango sería mejor definirlo en función del número de cartas del mazo, revisar
            card_coordinates = [cardwidthx, cardheighty, cardsizex, cardsizey]
            sprite_rects.append(card_coordinates)
            cardwidthx += cardsizex
            if cardwidthx >= self.x:
                cardwidthx = 0
                cardheighty += cardsizey
        return self.images_at(sprite_rects) 

    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]


class Card:
    suits = ["Rojo", "Amarillo", "Verde", "Azul", "Comodín"] #suit es un atributo de clase
    ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
             "pierdeturno", "cambiasentido", "robados", "eligecolor", "robacuatro"] #rank es otro atributo de clase
     
    def __init__(self, suit=0, rank=0): # __init__ crea una instancia de la clase Card; cada carta tiene un suit y un rank
        self.suit = suit
        self.rank = rank
        self.position = []
        self.image = None

    def contains_point(self, point):
        """ Return True if my sprite rectangle contains point pt """
        (my_x, my_y) = self.position
        my_width = self.image.get_width()
        my_height = self.image.get_height()
        (x, y) = point
        return ( x >= my_x and x < my_x + my_width and y >= my_y and y < my_y + my_height)
    
   
class Deck:
    def __init__(self):
        self.cards = [] # Creamos el atributo cards. Recordar que los atributos en __init__, aparte de self, son opcionales
        for suit in range(4):
            for rank in range(0, 10):
                self.cards.append(Card(suit, rank))
        for suit in range(4):
            for rank in range(10, 13):
                self.cards.append(Card(suit, rank))
        for suit in range(4, 5):
            for rank in range(13, 15):
                self.cards.append(Card(suit, rank))
                self.cards.append(Card(suit, rank))

        sprite = CardSprite()
        images = sprite.load_grid_images()

        i = 0
        for image in images:
            self.cards[i].image = image
            i +=1

        questionmark = sprite.image_at([720,750,80,125])
        self.image = questionmark
        self.position = (650, 256)        

    def shuffle(self): 
        rng = random.Random()
        rng.shuffle(self.cards)

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card) # Usamos el método remove
            return True
        return False

    def pop(self):
        return self.cards.pop() # Pop toma la última carta y la reparte

    def is_empty(self):
        return self.cards == [] # True si no quedan cartas en el mazo

    def deal(self, hands, num_cards=999):
        num_hands = len(hands)
        for i in range(num_cards):
            if self.is_empty():
                break
            card = self.pop()
            hand = hands[i % num_hands]
            hand.add(card)

    def contains_point(self, point):
        """ Return True if my sprite rectangle contains point pt """
        (my_x, my_y) = self.position
        my_width = self.image.get_width()
        my_height = self.image.get_height()
        (x, y) = point
        return ( x >= my_x and x < my_x + my_width and y >= my_y and y < my_y + my_height)    

class Hand(Deck):
    pass

    def __init__(self, name=""):
        self.cards = []
        self.name = name
        if name == "AI":
            self.status = 1 # jugador controlado por el ordenador
        else:
            self.status = 0 # jugador humano

    def add(self, card):
        self.cards.append(card)
           
        
class UNOGame:    
    
    def place_cards(self):
        # Definimos un patrón para pegar las cartas una junto a otra
        [paste_x, paste_y] = [64, 480]
        [paste_xAI, paste_yAI] = [64, 32]
        
        # Definimos la posición que ocuparán las cartas sobre el tablero al empezar la partida
        for hand in self.hands:
            for card in hand.cards:
                card.hidden = self.deck.image # Para el atributo hidden usamos la carta con el signo de interrogación,
                                              # que anteriormente asignamos al atributo image del mazo
                if hand.name == "AI":
                    card.position = [paste_xAI, paste_yAI]
                    paste_xAI += 85
                else:
                    card.position = [paste_x, paste_y]
                    paste_x += 85        

    def place_buttons(self):
        self.font = pygame.font.SysFont("Fixedsys Excelsior", 32)
        size = 45
        x = self.play_area[0]
        y = self.play_area[1]
        # Definimos los botones para elegir entre los cuatro colores, así como el botón de pasar turno y el del color en juego
        for n in range(4):
            a_button = Button(x - 55, y + 145, size, size)
            x += 50
            self.all_buttons.append(a_button)

        coordinates = [850, 275, 125, 25],[750, 325, 330, 25],[225, 400, 175, 30],[575, 400, 175, 30]
        for c in coordinates:
            a_button = Button(c[0], c[1], c[2], c[3])
            self.all_buttons.append(a_button) 

        c = 0
        for button in self.all_buttons:
            button.color = self.colors[c]
            c += 1
            if c == 6:
                break

        self.all_buttons[4].text = self.font.render("Pasar turno".format(), True, (0,0,0))
        self.all_buttons[5].text = self.font.render("El color en juego es el {0}".format(self.color_in_play), True, (255,255,255))
        self.all_buttons[6].text = self.font.render("Volver a jugar".format(), True, (0,0,0))
        self.all_buttons[6].color = self.colors[0]
        self.all_buttons[7].text = self.font.render("Salir del juego".format(), True, (0,0,0))
        self.all_buttons[7].color = self.colors[3]

    def blit_buttons(self, i=0, j=6):
        for n in range(i, j):
            button_color = self.all_buttons[n].color
            button_rect = (self.all_buttons[n].x, self.all_buttons[n].y, self.all_buttons[n].w, self.all_buttons[n].h)
            if n == 5:
                self.all_buttons[n].text = self.font.render("El color en juego es el {0}".format(self.color_in_play), True, (255,255,255))
            button_text = self.all_buttons[n].text
            self.main_surface.fill(button_color, button_rect)
            try:
                self.main_surface.blit(button_text, button_rect)
            except:
                TypeError

    def update_cards(self):
        # Ponemos las cartas sobre el tablero
        for hand in self.hands:
            for card in hand.cards:
                if hand.name == "AI":
                    self.main_surface.blit(card.hidden, card.position) # Si es una carta de la IA, elegimos la imagen del signo de interrogación
                else:
                    self.main_surface.blit(card.image, card.position)
        self.main_surface.blit(self.deck.image, self.deck.position)
        self.main_surface.blit(self.card_in_play.image, self.play_area)

    def update_surface(self):
        size = 45
        #last_play = Text(600, 200, "La carta en juego es " + self.card_in_play.suits[self.color] + self.card_in_play.ranks[self.number])
        # Pintamos la superficie            
        self.main_surface.fill(self.surface_color)
        self.update_cards()
        self.blit_buttons(4,6)
        #self.main_surface.blit(last_play.text, last_play.position) 
        pygame.display.flip()

    def play_discard(self):
        self.deck.cards = self.discard_deck.cards # Asignamos al mazo las cartas del mazo de descartes
        self.deck.shuffle() # Barajamos el nuevo mazo
        self.discard_deck.cards = [] # Vaciamos el mazo de descartes para reiniciar el ciclo
       
    def start_UNO(self): # Creamos la partida del juego de cartas UNO, que es un tipo de juego de cartas
        self.deck = Deck()
        self.deck.shuffle()

        # Iniciamos el módulo pygame
        pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "lobby.mp3"))
        pygame.mixer.music.play(-1)

        # Creamos una superficie de juego, donde colocar las cartas
        surface_sizex = 1280 # Ancho del tablero, en píxeles
        surface_sizey = 640 # Alto del tablero, en píxeles
        self.surface_color = (19,136,8) # Red/Green/Blue; la superficie del tablero será de color verde oscuro
        self.play_area = (320, 264)
        self.main_surface = pygame.display.set_mode((surface_sizex, surface_sizey)) # Creamos el tablero
        pygame.display.set_caption('UNO')
        self.colors = ([234, 26, 39], [248, 224, 0], [0, 164, 78], [2, 149, 216], [255, 165, 0], [0, 0, 0]) # Rojo, amarillo, verde, azul, naranja, negro
        self.main_surface.fill(self.surface_color)
         
        # Cargamos el logo del juego para la carga inicial
        logo = pygame.image.load(os.path.join(main_dir, 'UNO', "UNO_logo_small.png"))
        h = logo.get_height() 
        w = logo.get_width() 
        welcome = Text(345, 580, "Pulsa cualquier tecla para continuar")
        self.main_surface.blit(logo, (surface_sizex//2 - w//2, surface_sizey//2 - h//2))
        self.main_surface.blit(welcome.text, welcome.position)
        pygame.display.flip()

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN: # Hemos pulsado una tecla
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Permitimos al jugador introducir su nombre
        name = Text(100, 100, "Introduce tu nombre (pulsa enter cuando hayas terminado):")
        self.main_surface.fill(self.surface_color)
        self.main_surface.blit(name.text, name.position)
        pygame.display.flip()
        
        self.player_name = ''
        font = pygame.font.SysFont("Fixedsys Excelsior", 48)
        enter = 0
        while enter == 0:
            event = pygame.event.poll() # Buscar eventos y asignárselos a la variable event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    enter = 1
                else:
                    self.player_name += event.unicode
                self.main_surface.fill(self.surface_color)
                txt_surface = font.render(self.player_name, True, pygame.Color('dodgerblue2'))
                self.main_surface.blit(txt_surface, (100, 200))
                self.main_surface.blit(name.text, name.position)
                pygame.display.flip()

        self.main_surface.fill(self.surface_color)
        tachan = Text(100, 300, "¡Bienvenido, " + self.player_name + "! La partida comenzará en unos segundos")
        self.main_surface.blit(tachan.text, tachan.position)
        pygame.display.flip()

        self.names = [self.player_name, "AI"]
        self.main_surface.fill(self.surface_color)

    def play_UNO(self): # Iniciamos la partida de UNO 
        # Creamos las manos del juego
        pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "lobby.mp3"))
        pygame.mixer.music.play(-1)
        self.hands = []
        for name in self.names:
            self.hands.append(Hand(name))

        # Repartimos las cartas
        self.deck.deal(self.hands, 7 * len(self.names)) # Tomamos el objeto mazo que pertenece al objeto juego (self),
                                                       # y repartimos siete cartas a cada jugador

        # Colocamos las cartas sobre el tablero            
        self.place_cards()

        # Sacamos una carta para empezar a jugar
        self.card_in_play = self.deck.pop()
        self.card_in_play.position = self.play_area
        self.color = self.card_in_play.suit # Me interesa separar el color de la carta, para poder implementar el comodín eligecolor
        self.number = self.card_in_play.rank

        # Creamos algunas cositas más parabotones extra
        self.all_buttons = []
        self.color_in_play = self.card_in_play.suits[self.color]

        turn = 0
        pierdeturno = 0
        self.has_drawn = 2 # Para cubrir el caso en que la carta inicial sea una carta de efectos
        i = 0
    
        self.place_buttons()
        self.update_surface()
        self.discard_deck = Deck() # Creamos un mazo de descartes
        self.discard_deck.cards = [] # Vaciamos el mazo de descartes

        while True:
            event = pygame.event.poll() # Buscar eventos y asignárselos a la variable event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Comenzamos el bucle estableciendo los efectos en función de la carta en juego (self.card_in_play):
            
            if self.card_in_play.rank == 10: #"pierdeturno": # El turno pasará al otro jugador
                if self.has_drawn == 0:
                    pierdeturno += 1
                    self.has_drawn = 1

            elif self.card_in_play.rank == 11: #"cambiasentido": 
                self.has_drawn = 1 # Esto es simplemente para poder simplificar la fórmula de efectos y expresarla como 10 <= rank <= 14

            elif self.card_in_play.rank == 12: #"robados":
                if self.has_drawn != 1: # No queremos que al comenzar el siguiente turno se vuelvan a robar dos cartas
                    for n in range(2):
                        if self.deck.is_empty(): # Si no quedan cartas en el mazo
                            self.play_discard()
                        self.hands[(i+1) % len(self.hands)].cards.append(self.deck.pop()) # Robo dos cartas y las añado a mi mano
                    self.has_drawn = 1
                                    
            elif self.card_in_play.rank == 13: #"eligecolor": 
                if self.has_drawn != 1: # No queremos que al final de este turno se vuelvan a robar cuatro cartas
                    # Aquí hay que añadir un árbol de decisión según sea jugador IA o jugador humano, para elegir el color
                    if self.hands[i].status == 1: # si el jugador es IA
                        rng = random.Random()
                        self.color = rng.randrange(0, 4)
                    else: # si el jugador es humano
                        self.blit_buttons(0, 4)                            
                        pygame.display.flip()
                        has_picked_color = 0
                        while has_picked_color == 0:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN: # Hemos hecho click
                                    place_of_click = event.dict["pos"]
                                    b = 0
                                    for button in self.all_buttons[0:4]:
                                        if button.contains_point(place_of_click):
                                            has_picked_color = 1
                                            self.color = b
                                        b += 1
                    self.card_in_play.suit = self.color
                    self.color_in_play = self.card_in_play.suits[self.color]
                    self.has_drawn = 1
                                     
            elif self.card_in_play.rank == 14: #"robacuatro":                   
                if self.has_drawn != 1: # No queremos que al final de este turno se vuelvan a robar cuatro cartas
                    for n in range(4):
                        if self.deck.is_empty(): # Si no quedan cartas en el mazo
                            self.play_discard()
                        self.hands[(i+1) % len(self.hands)].cards.append(self.deck.pop()) # Robo cuatro cartas y las añado a mi mano
                    # Aquí hay que añadir un árbol de decisión según sea jugador IA o jugador humano, para elegir el color
                    if self.hands[i].status == 1: # si el jugador es IA
                        rng = random.Random()
                        self.color = rng.randrange(0, 4)
                    else: # si el jugador es humano
                        self.blit_buttons(0, 4) 
                        pygame.display.flip()
                        has_picked_color = 0
                        while has_picked_color == 0:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN: # Hemos hecho click
                                    place_of_click = event.dict["pos"]
                                    b = 0
                                    for button in self.all_buttons[0:4]:
                                        if button.contains_point(place_of_click):
                                            has_picked_color = 1
                                            self.color = b
                                        b += 1
                    self.card_in_play.suit = self.color
                    self.color_in_play = self.card_in_play.suits[self.color]
                    self.has_drawn = 1

            # Actualizamos las cartas
            self.place_cards()
            self.update_surface()
            
            # Los efectos ya están consolidados (esperemos). Ahora hay que definir el cambio de turno
            turn += 1
            i = (turn + pierdeturno) % len(self.hands) # 0 en el primer turno, salvo que la primera carta en juego sea pierdeturno
            self.playable_cards = []
            suits_in_hand = []
            hand = self.hands[i].cards # Llamamos hand a la mano que está jugando, para que el código sea más legible

            # Comienza el siguiente turno, propiamente dicho
            # Determinamos si tenemos cartas en la mano que podamos jugar:
            for card in hand:
                suits_in_hand.append(card.suit) # Anotamos el color de cada carta, para comprobar después si podemos usar el comodín robacuatro
                if card.suit == self.color or card.rank == self.card_in_play.rank or card.rank == 13: #"eligecolor":
                    # Si la carta comparte color o número con la que está en juego, o si es el comodín de elegir color
                    self.playable_cards.append(card)

            if self.color not in suits_in_hand: # Si no tenemos ninguna carta del mismo color que la que está en el área de juego
                for card in hand:
                    if card.rank == 14: #"robacuatro": 
                        self.playable_cards.append(card) # Lo añadimos a las cartas que podemos jugar
                        
            if self.hands[i].status == 1: # si el jugador es IA
                self.AI_plays(hand)

            else: # si el jugador es humano
                self.human_plays(hand)

            # Consideraciones de final de turno, a continuación

            self.color = self.card_in_play.suit
            self.color_in_play = self.card_in_play.suits[self.color]

            if self.deck.is_empty(): # Si no quedan cartas en el mazo
                self.play_discard()

            self.place_cards()
            self.update_surface()
            
            if self.hands[i].is_empty(): # Si no quedan cartas en la mano
                end_game = 0
                self.main_surface.fill(self.surface_color)
                if self.hands[i].name == self.player_name: # Ha ganado el jugador humano
                    pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "win.mp3"))
                    pygame.mixer.music.play(-1)
                    win = Text(100, 300, "¡Enhorabuena, " + self.player_name + "! Has ganado la partida")
                    self.main_surface.blit(win.text, win.position)               
                else: # Ha ganado la IA
                    pygame.mixer.music.load(os.path.join(main_dir, 'UNO', "loss.mp3"))
                    pygame.mixer.music.play(-1)
                    loss = Text(100, 300, "¡Lo sentimos, " + self.player_name + "! El ordenador ha ganado la partida")
                    self.main_surface.blit(loss.text, loss.position)            
                self.blit_buttons(6, 8)
                pygame.display.flip()
                while end_game == 0:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN: # Hemos hecho click
                            place_of_click = event.dict["pos"]
                            for button in self.all_buttons[6:8]:
                                if button.contains_point(place_of_click):
                                    if button == self.all_buttons[6]:
                                        end_game = 1
                                        running = False
                                        self.deck = Deck()
                                        self.deck.shuffle()
                                        self.play_UNO()
                                    else:                                       
                                        pygame.quit()
                                        sys.exit()
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def AI_plays(self, hand):
        if self.playable_cards == []: # No podemos jugar ninguna carta, tenemos que robar
            drawn_card = self.deck.pop()
            if drawn_card.suit == self.color or drawn_card.rank == self.card_in_play.rank or drawn_card.suit == 4: #"Comodín":
                # Si la carta robada comparte color o número con la que está en juego, o si es un comodín
                self.card_in_play = drawn_card # Jugamos la carta robada
                self.has_drawn = 0
                # hand.remove(drawn_card) ¡No es necesario, porque no llega a añadir la carta a la mano! Dará error
                self.discard_deck.cards.append(drawn_card)
            else:
                hand.append(drawn_card) # Añadimos la carta robada a nuestra mano
            
        else: # No nos hace falta robar, porque tenemos en la mano cartas que podemos jugar                          
            rng = random.Random()
            selected_card = self.playable_cards[rng.randrange(0, len(self.playable_cards))] # La IA elige la carta que jugar
            self.card_in_play = selected_card # La carta elegida será la próxima carta en juego
            self.has_drawn = 0
            self.card_in_play.position = self.play_area # Adjudicamos a la carta elegida la zona de juego
            hand.remove(selected_card)
            self.discard_deck.cards.append(selected_card)
  
    def human_plays(self, hand):
        self.has_drawn = 0
        has_played = 0
        has_playable_cards = 0
        while self.has_drawn == 0:
            if self.playable_cards == []: # No podemos jugar ninguna carta, tenemos que robar
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN: # Hemos hecho click
                        place_of_click = event.dict["pos"]
                        if self.deck.contains_point(place_of_click):
                            drawn_card = self.deck.pop()                                
                            if drawn_card.suit == self.color or drawn_card.rank == self.card_in_play.rank or drawn_card.suit == 4: #"Comodín":
                                self.playable_cards.append(drawn_card)
                                has_playable_cards = 1
                            else:
                                pygame.display.flip()
                            self.has_drawn = 1
                            hand.append(drawn_card)
                            # Actualizamos las cartas
                            self.place_cards()
                            self.update_surface()
            else:
                has_playable_cards = 1
                self.has_drawn = 1
                
        while has_played == 0:        
            if has_playable_cards == 1: # Podemos jugar
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN: # Hemos hecho click
                        place_of_click = event.dict["pos"]
                        for card in self.playable_cards:
                            if card.contains_point(place_of_click):
                                self.card_in_play = card
                                hand.remove(card)
                                self.discard_deck.cards.append(card)
                                has_played = 1
                                self.has_drawn = 0

            else: # Tenemos que pasar turno
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN: # Hemos hecho click
                        place_of_click = event.dict["pos"]
                        if self.all_buttons[4].contains_point(place_of_click):
                            has_played = 1

def main():
    game = UNOGame()
    game.start_UNO()
    game.play_UNO()

#call the "main" function if running this script
if __name__ == '__main__': main()
