from cardgame import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Dealer():
    """This class (and subsequent object) contains the properties and methods
    necessary for the Dealer in a game of Blackjack to function properly.
    """
    def __init__(self):
        self.hand = []
        self.score = 0
        self.shownscore = 0
        self.state = "H"
    def updateScore(self):
        self.score = 0
        aceInHand = False
        for card in self.hand:
            if card[0] == 1:
                aceInHand = True
            elif card[0] <= 10:
                self.score += card[0]
            else:
                self.score += 10
        if aceInHand:
            if self.score + 11 > 21:
                self.score += 1
            else:
                self.score += 11
        if self.score > 21:
            self.state = "B"
        elif self.score < 17:
            self.state = "H"
        else:
            self.state = "S"
    def determineMove(self):
        if self.score < 17:
            return "H"
        else:
            return "S"
    
class Player():
    """This class is designed to hold information regarding that state of
    the game and contain methods to update its own properties correctly.
    """
    def __init__(self):
        self.hand = []
        self.score = 0
        self.state = "H"
        self.chips = 0
        self.bet = 0
    def updateScore(self):
        self.score = 0
        aceInHand = False
        for card in self.hand:
            if card[0] == 1:
                aceInHand = True
            elif card[0] <= 10:
                self.score += card[0]
            else:
                self.score += 10
        if aceInHand: 
            if self.score + 11 > 21: 
                self.score += 1 
            else: 
                self.score += 11
        if self.score > 21:
            self.state = "B"

class aiPlayer(Dealer):
    """Very basic AI that copies the Dealer class.

    Args:
        Dealer (_type_): _description_
    """
    def __init__(self, cutoff = 12):
        self.hand = []
        self.score = 0
        self.state = ""
        self.chips = 0
        self.bet = 0
        self.cutoff = cutoff
    def determineMove(self):
        if self.score < self.cutoff:
            return "H"
        else:
            return "S"
    def pickBet(self, chips: int):
        self.chips = chips
        if self.chips < 100:
            self.bet = random.randint(0, self.chips//2)
        else:
            self.bet = random.randint(0, 75)
        if self.bet == 0:
            self.bet = self.chips
        self.chips -= self.bet
        
def dealCards(deck, human, comp1: aiPlayer, comp2: aiPlayer, comp3: aiPlayer):
    players = [human, comp1, comp2, comp3]
    pid = 0
    for card in deck:
        while len(comp3.hand) < 4:
            players[pid].hand += card
            deck.remove(card)
            pid+=1 
            pid%=4

def main():
    """Sets up the betting button to begin the
    main game
    This is the main function because these are the
    first things that needs to run WITH input
    from the user.
    """
    #Initialize game window
    global gameWindow
    gameWindow=tk.Tk()
    gameWindow.title("Blackjack")
    gameWindow.geometry("1100x700")
    gameWindow['bg']="#00512c"

    global main_frame
    main_frame=tk.Frame(gameWindow,bd=2,bg='white')
    main_frame.pack(pady=20,side='bottom')

    title=tk.Label(text='Welcome to Blackjack!',font=("Helvetica", 22))
    title.place(anchor=tk.CENTER,relx=.5,rely=.4)

    global h_frame
    h_frame = tk.LabelFrame(main_frame,bg='green',text='Player',bd=0,labelanchor='n',fg='white')
    h_frame.pack(side='bottom')
    
    global h_labels
    h_labels = []
    
    global h_images
    h_images=[]
    
    global resize_cards
    def resize_cards(card):
        card_img = Image.open(card)
        card_resize_img = card_img.resize((50,72))
        card_image = ImageTk.PhotoImage(card_resize_img)
        global h_images # Prevents garbage collector from deleting images
        h_images+=[card_image]
        return card_image

    #Card Generation
    global player
    player = Player()
    global dealer
    dealer = Dealer()
    global AI1
    AI1 = aiPlayer(12)
    global AI2
    AI2 = aiPlayer(13)
    global AI3
    AI3 = aiPlayer(14)

    #Read Save Data
    with open('data/save.txt', 'r') as file:
        for line in file:
            line=line.split(',')
            if line[0]=="player":
                if int(line[1]) <= 0:
                    player.chips = 100
                else:
                    player.chips=int(line[1])
            elif line[0]=="AI1":
                AI1.pickBet(int(line[1]))
            elif line[0]=="AI2":
                AI2.pickBet(int(line[1]))
            elif line[0]=="AI3":
                AI3.pickBet(int(line[1]))
    
    #This makes it easier to go through turns later
    global table
    table = [player, AI1, AI2, AI3, dealer]

    #Refresh AI chips if they run out
    for g in table[1:4]:
        if g.chips == 0: 
            g.chips = 100

    #Create initial GUI elements for the human player
    global h_betBoxFrame
    h_betBoxFrame = tk.LabelFrame(gameWindow)
    h_betBoxFrame.pack(side=tk.BOTTOM)

    global h_chipCount
    h_chipCount = tk.Label(h_betBoxFrame, text=f'Chips: {player.chips}')
    h_chipCount.pack(side=tk.TOP)

    def onClick(*args):
        """Function for the Place Bet button.
        Sets bet, and begins the game.
        """
        try:
            bet = int(h_betBox.get())
        except ValueError:
            bet = 0
        if bet < 0:
            messagebox.showinfo(message="Me when the double negative: :(", title="Nice try!")
        elif bet > player.chips:
            messagebox.showerror(title="You can't go into the negatives!", message="Debt from gambling is never fun.")
        else:
            player.chips -= bet
            player.bet = bet
            title.destroy()
            h_betBoxFrame.destroy()
            h_chipCount.destroy()
            h_betBox.destroy()
            h_betBoxButton.destroy()
            mainGame()

    global h_betBox
    h_betBox = tk.Entry(h_betBoxFrame, width=len(str(player.chips))+4)
    h_betBox.pack(side=tk.TOP)
    h_betBox.bind('<Return>', onClick)

    global h_betBoxButton
    h_betBoxButton = tk.Button(h_betBoxFrame, text="Place Bet", command=lambda:onClick())
    h_betBoxButton.pack(side=tk.TOP)
    gameWindow.state('zoomed')
    tk.mainloop()

def mainGame():
    """Runs after the initial bet is placed.
    This method is responsible for making the game function.
    """
    ####### Initialize GUI
    #Create and Shuffle deck
    fullDeck = []
    for s in suit:
        for card in [[x,s] for x in value]:
            fullDeck += [card]
    deck = shuffleDeck(fullDeck)

    #Deal cards
    for p in table:
        for i in range(0,2):
            card = random.choice(deck)
            deck.remove(card)
            p.hand+=card

    def drawGUI():
        """This method contains a lot of objects being created,
        specifically because each player at the table (5) needs
        at least 4 different GUI objects on its own before
        even displaying the cards.
        """
        #Draw hand of player and buttons
        global guicards
        guicards = []
        for card in player.hand:
            h_card1 = tk.Label(h_frame, anchor='w')
            h_image1 = resize_cards(f'data/textures/{card[0]}{card[1]}.png')
            h_card1.config(image=h_image1)
            h_card1.pack(pady=20, side='left')
            guicards += [h_card1]
        
        global h_Score
        h_Score = tk.Label(h_frame, text=player.score)
        h_Score.pack(side=tk.RIGHT)

        global h_alttext
        h_alttext = tk.Label(h_frame)
        h_alttext.pack(side=tk.RIGHT)

        global h_buttonFrame
        h_buttonFrame = tk.LabelFrame(gameWindow)
        h_buttonFrame.pack(side=tk.BOTTOM)

        h_StandButton = tk.Button(h_buttonFrame, text='Stand', command=lambda:turnHandler("S", player))
        h_StandButton.pack(side=tk.RIGHT)
        h_HitButton = tk.Button(h_buttonFrame, text='Hit', command=lambda:turnHandler("H", player))
        h_HitButton.pack(side=tk.RIGHT)

        h_betBoxFrame = tk.LabelFrame(gameWindow)
        h_betBoxFrame.pack(side=tk.BOTTOM)

        global h_chipCount
        h_chipCount = tk.Label(h_betBoxFrame, text=f'Chips: {player.chips}')
        h_chipCount.pack(side=tk.TOP)

        ########################
        #Rare scenario where Mid-game insurance bet can be placed if the face-up card from the dealer is an Ace.
        global ibetstate
        ibetstate = 0
        if dealer.hand[1][0] == 1:
            def drawBox():
                global ibetstate
                if ibetstate == 0:
                    global ibetValue
                    ibetValue=tk.StringVar()
                    global h_betBox
                    h_betBox = tk.Entry(h_betBoxFrame, width=5, textvariable=ibetValue)
                    h_betBox.pack(side=tk.TOP)
                    ibetstate = 1
                else:
                    ibetstate = 0
                    h_betBox.destroy()
            
            global h_ibetStatus
            h_ibetStatus = tk.IntVar(value=0)
            h1_ibet = tk.Checkbutton(h_betBoxFrame, text='Insurance Bet?', variable=h_ibetStatus, onvalue=1, offvalue=0, command=lambda:drawBox())
            h1_ibet.pack()
        ########################

        global buttons
        buttons = []
        buttons += [h_StandButton]
        buttons += [h_HitButton]

        #Deck
        global deck_frame
        deck_frame = tk.Frame(gameWindow,bd=2,bg='white')
        deck_frame.place(relx=.5,rely=.3,anchor=tk.CENTER)

        global deck_lframe
        deck_lframe = tk.LabelFrame(deck_frame, bg='#00512c')
        deck_lframe.pack()

        #Draw dealer's hand
        t_frame=tk.Frame(gameWindow,bd=2,bg='white')
        t_frame.place(relx=.5,rely=.5,anchor=tk.CENTER)

        global d_frame
        d_frame = tk.LabelFrame(t_frame,bg='#00512c',text='Dealer',bd=0,labelanchor='n',fg='white')
        d_frame.pack()
        
        global d_Score
        d_Score = tk.Label(d_frame, text=dealer.score)
        d_Score.pack(side=tk.RIGHT)

        global d_alttext
        d_alttext = tk.Label(d_frame)
        d_alttext.pack(side=tk.RIGHT)

        #Draw AI 1's hand
        ai1b_frame=tk.Frame(gameWindow,bd=2,bg='white')
        ai1b_frame.place(anchor=tk.N, relx=.2)

        global ai1_frame
        ai1_frame = tk.LabelFrame(ai1b_frame,bg='#00512c',text='AI 1',bd=0,labelanchor='n',fg='white')
        ai1_frame.pack()
        
        global ai1_Score
        ai1_Score = tk.Label(ai1_frame, text=AI1.score)
        ai1_Score.pack(side=tk.RIGHT)

        global ai1_alttext
        ai1_alttext = tk.Label(ai1_frame)
        ai1_alttext.pack(side=tk.RIGHT)

        global ai1_chipcount
        ai1_chipcount = tk.Label(ai1_frame, text=f'Chips: {AI1.chips}', bg='green', fg='white')
        ai1_chipcount.pack(side=tk.RIGHT)

        #Draw AI2's hand
        ai2b_frame=tk.Frame(gameWindow,bd=2,bg='white')
        ai2b_frame.place(anchor=tk.N, relx=.5)

        global ai2_frame
        ai2_frame = tk.LabelFrame(ai2b_frame,bg='#00512c',text='AI 2',bd=0,labelanchor='n',fg='white')
        ai2_frame.pack()
        
        global ai2_Score
        ai2_Score = tk.Label(ai2_frame, text=AI2.score)
        ai2_Score.pack(side=tk.RIGHT)

        global ai2_alttext
        ai2_alttext = tk.Label(ai2_frame)
        ai2_alttext.pack(side=tk.RIGHT)

        global ai2_chipcount
        ai2_chipcount = tk.Label(ai2_frame, text=f'Chips: {AI2.chips}', bg='green', fg='white')
        ai2_chipcount.pack(side=tk.RIGHT)

        #Draw AI3's hand
        ai3b_frame=tk.Frame(gameWindow,bd=2,bg='white')
        ai3b_frame.place(anchor=tk.N, relx=.8)

        global ai3_frame
        ai3_frame = tk.LabelFrame(ai3b_frame,bg='#00512c',text='AI 3',bd=0,labelanchor='n',fg='white')
        ai3_frame.pack()
        
        global ai3_Score
        ai3_Score = tk.Label(ai3_frame, text=AI3.score)
        ai3_Score.pack(side=tk.RIGHT)

        global ai3_alttext
        ai3_alttext = tk.Label(ai3_frame)
        ai3_alttext.pack(side=tk.RIGHT)

        global ai3_chipcount
        ai3_chipcount = tk.Label(ai3_frame, text=f'Chips: {AI3.chips}', bg='green', fg='white')
        ai3_chipcount.pack(side=tk.RIGHT)

        updateGUI()

    def updateGUI():
        """Updates the GUI with cards after it is initially drawn
        and updates the GUI after the player's turn is complete.
        """
        #Update all scores
        player.updateScore()
        dealer.updateScore()
        AI1.updateScore()
        AI2.updateScore()
        AI3.updateScore()

        #Clear all onscreen cards
        global guicards
        for card in guicards:
            card.destroy()
        guicards = []
        
        #Refresh Player
        for card in player.hand:
            h_card1 = tk.Label(h_frame, anchor='w')
            h_image1 = resize_cards(f'data/textures/{card[0]}{card[1]}.png')
            h_card1.config(image=h_image1)
            h_card1.pack(pady=20, side='left')
            guicards += [h_card1]
        global h_Score
        h_Score.config(text=player.score)

        #Show correct text based on situation
        if player.state == "B":
            h_alttext.config(text="bust!")
        elif player.score == 21:
            h_alttext.config(text="Blackjack!")

        #Refresh Dealer
        for card in dealer.hand:
            d_card1 = tk.Label(d_frame, anchor='w')
            if dealer.hand.index(card) == 0 and player.state not in 'BS':
                d_image1 = resize_cards(f'data/textures/blank.png')
            else:
                d_image1 = resize_cards(f'data/textures/{card[0]}{card[1]}.png')
            d_card1.config(image=d_image1)
            d_card1.pack(pady=20, side='left')
            guicards += [d_card1]
        global d_Score
        
        #Determine shown score
        if player.state in 'BS':
            d_Score.config(text=dealer.score)
            if dealer.state == "B":
                d_alttext.config(text="bust!")
        else:
            if dealer.hand[1][0] <= 10:
                d_Score.config(text=dealer.hand[1][0])
            else:
                d_Score.config(text="10")

        #Refresh AI1
        for card in AI1.hand:
            ai1_card1 = tk.Label(ai1_frame, anchor='w')
            if AI1.hand.index(card) == 0 and player.state not in 'BS':
                ai1_image1 = resize_cards(f'data/textures/blank.png')
            else:
                ai1_image1 = resize_cards(f'data/textures/{card[0]}{card[1]}.png')
            ai1_card1.config(image=ai1_image1)
            ai1_card1.pack(pady=20, side='left')
            guicards += [ai1_card1]

        global ai1_Score
        #Determine shown score
        if player.state in 'BS':
            ai1_Score.config(text=AI1.score)
            if AI1.state == "B":
                ai1_alttext.config(text="bust!")
        else:
            if AI1.hand[1][0] <= 10:
                ai1_Score.config(text=AI1.hand[1][0])
            else:
                ai1_Score.config(text="10")

        #Refresh AI2
        for card in AI2.hand:
            ai2_card1 = tk.Label(ai2_frame, anchor='w')
            if AI2.hand.index(card) == 0 and player.state not in 'BS':
                ai2_image1 = resize_cards(f'data/textures/blank.png')
            else:
                ai2_image1 = resize_cards(f'data/textures/{card[0]}{card[1]}.png')
            ai2_card1.config(image=ai2_image1)
            ai2_card1.pack(pady=20, side='left')
            guicards += [ai2_card1]
        global ai2_Score
        
        #Determine shown score
        if player.state in 'BS':
            ai2_Score.config(text=AI2.score)
            if AI2.state == "B":
                ai2_alttext.config(text="bust!")
        else:
            if AI2.hand[1][0] <= 10:
                ai2_Score.config(text=AI2.hand[1][0])
            else:
                ai2_Score.config(text="10")

        #Refresh AI3
        for card in AI3.hand:
            ai3_card1 = tk.Label(ai3_frame, anchor='w')
            if AI3.hand.index(card) == 0 and player.state not in 'BS':
                ai3_image1 = resize_cards(f'data/textures/blank.png')
            else:
                ai3_image1 = resize_cards(f'data/textures/{card[0]}{card[1]}.png')
            ai3_card1.config(image=ai3_image1)
            ai3_card1.pack(pady=20, side='left')
            guicards += [ai3_card1]
        global ai3_Score

        #Determine shown score
        if player.state in 'BS':
            ai3_Score.config(text=AI3.score)
            if AI3.state == "B":
                ai3_alttext.config(text="bust!")
        else:
            if AI3.hand[1][0] <= 10:
                ai3_Score.config(text=AI3.hand[1][0])
            else:
                ai3_Score.config(text="10")

        #Deck Update
        blank_card = tk.Label(deck_lframe, anchor='n')
        blank_card_img = resize_cards('data/textures/blank.png')
        blank_card.config(image=blank_card_img)
        blank_card.pack()
        guicards+=[blank_card]
        
        blank_card_txt = tk.Label(deck_lframe, text=f'Remaining Cards: {len(deck)}', bg="#00512c", fg='white')
        blank_card_txt.pack()
        guicards+=[blank_card_txt]
        
    def turnHandler(move, o: Player or aiPlayer or Dealer):
        """This method is called when any GUI buttons are clicked.
        It is responsible for updating the states of the players,
        and what is onscreen. At the end of the game, bets are
        returned and the save data is written.

        Args:
            move (str): H or S depending on move (Hit/Stand)
            o (Player or aiPlayer or Dealer): Player Object who is making the turn
        """
        if o.state != "S" and o.state != "B" and move == "H": #If the object is allowed to make a move...
            card = random.choice(deck)
            deck.remove(card)
            o.hand += card
        elif move == "S": #If they want to stand...
            o.state = "S"
        
        o.updateScore()
        #Update state based on score conditions
        
        global player
        global table
        if ( type(o) == type(dealer) or type(o) == type(AI1) ) and o.determineMove() == "H": #If the player is nonhuman and their turn is ongoing,
            turnHandler(o.determineMove(), o) #Determine the next move and take it recursively :)
        
        elif player.state in "BS" and o == player: #If the players turn is complete... / This line needs to be added to the statement above to avoid infinite recursion
            [turnHandler(x.determineMove(), x) for x in table[1:]] #Other players at the table make their turn
            updateGUI()
        
        #Determine win state and distribute bets
            if ibetstate == 1:
                try:
                    ibet = int(ibetValue.get())
                    assert(ibet > 0 and player.bet > 0)
                    if ibet > (player.bet // 2):
                        ibet = player.bet//2    
                    player.chips -= ibet
                except:
                    ibet = 0
            else:
                ibet = 0

            if dealer.hand[1][0] == 1  and dealer.hand[0][0] == 10 and ibetstate == 1 and ibet != 0:
                player.chips += player.bet + ibet*2
                messagebox.showinfo(message="Insurance bet won!")
            elif player.state == "B": messagebox.showerror(message="You lose!")
            elif dealer.state == "B" and player.state != "B":
                player.chips += player.bet*2
                messagebox.showinfo(message= "You win!")
            elif player.score == dealer.score and player.score <= 21:
                player.chips += player.bet
                messagebox.showinfo(message= "Tie!")
            elif player.score > dealer.score and player.score <= 21:
                player.chips += player.bet*2
                messagebox.showinfo(message= "You win!")
            else: messagebox.showerror(message="You lose!")

            ai_alttext = [ai1_alttext, ai2_alttext, ai3_alttext]
            for g in table[1:4]: #All AI's excluding dealer
                if g.score <= 21 and dealer.score > 21:
                    g.chips += g.bet*2
                    ai_alttext[table.index(g)-1].config(text=f'Win! (+{g.bet})', bg='green', fg='white')
                elif g.state == "S" and g.score > dealer.score:
                    g.chips += g.bet*2
                    ai_alttext[table.index(g)-1].config(text=f'Win! (+{g.bet})', bg='green', fg='white')
                elif g.state == "S" and g.score == dealer.score:
                    g.chips += g.bet
                    ai_alttext[table.index(g)-1].config(text=f'Tie! (+0)', bg='green', fg='white')
                else:
                    ai_alttext[table.index(g)-1].config(text=f'Loss! (-{g.bet})', bg='green', fg='white')
                
            global buttons
            for button in buttons:
                button.destroy()
            global h_buttonFrame
            global resetButton
            resetButton = tk.Button(h_buttonFrame, text='Reset', command=lambda:reset())
            resetButton.pack(side=tk.RIGHT)

            #Display new Chip Values
            h_chipCount.config(text=f'Chips: {player.chips}')
            ai1_chipcount.config(text=f'Chips: {AI1.chips}')
            ai2_chipcount.config(text=f'Chips: {AI2.chips}')
            ai3_chipcount.config(text=f'Chips: {AI3.chips}')

            #Write Save Data
            with open('data/save.txt', 'w') as file:
                file.writelines([f'player,{player.chips}\nAI1,{AI1.chips}\nAI2,{AI2.chips}\nAI3,{AI3.chips}'])
        else:
            updateGUI()

    def reset():
        gameWindow.destroy()
        main()

    drawGUI()

if __name__ == main():
    main()