#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tkinter import *
import time


class Pong:
    def __init__(self):
        global master
        self.bg_col = 'black'
        self.ball_col = 'white'
        self.raq_col = 'white'
        self.dx = 7
        self.dy = 7
        self.win= 1
        self.list_col = ['black', 'white', 'green', 'red', 'blue']
        #scores
        self.score_1 = 0
        self.score_2 = 0
        #lancement
        self.Menu()

    def Menu(self):
        self.menu = Frame(master, borderwidth = 2,  bg='white')
        self.button_play = Button(self.menu, text="Nouvelle partie", width=10, height=2, command=self.new_game).pack(ipadx = 20, pady =20)
        self.button_param = Button(self.menu, text="Parametres", width=10, height=2, command=self.menu_parametres).pack(ipadx = 20, pady = 20)
        self.button_quit = Button(self.menu, text="Quitter", command=master.quit).pack(ipadx = 20, pady = 20)
        self.menu.grid()

    def new_game(self):
        #canvas
        self.hauteur=master.winfo_screenheight()
        self.largeur=master.winfo_screenwidth()
        self.canvas=Canvas(master, width = self.largeur, height = self.hauteur, bg = self.bg_col)
        self.line = self.canvas.create_line((self.largeur/2),0,(self.largeur/2), self.hauteur, fill='white', dash=(5,5))
        #position balle
        self.posX = (self.largeur / 2) - 5
        self.posY = (self.hauteur / 2) - 5
        #position raquettes
        self.posX1 = 25
        self.posY1 = (self.hauteur/2)-150
        self.posX2 = self.largeur-25
        self.posY2 = (self.hauteur/2)-150
        #création objets
        self.ball = self.canvas.create_oval(self.posX, self.posY, self.posX+10, self.posY+10, fill = self.ball_col)
        self.raquette_1 = self.canvas.create_rectangle(self.posX1,self.posY1,self.posX1+25,self.posY1+300,fill=self.raq_col)
        self.raquette_2 = self.canvas.create_rectangle(self.posX2,self.posY2,self.posX2-25,self.posY2+300,fill=self.raq_col)
        
        master.bind('z', self.move_raq)
        master.bind('s', self.move_raq)
        master.bind('<Up>', self.move_raq)
        master.bind('<Down>', self.move_raq)

        # Initialisation du mouvement de la balle
        self.move_ball()

        # Affichage du jeu
        self.canvas.grid()

    def move_ball(self):
        #rebonds
        global dx, dy
        coord = self.canvas.coords(self.ball)
        if (coord[1] >= (self.hauteur - 10)) or (coord[3] <= 10):
            self.dy = -self.dy
        if (coord[0] < self.canvas.coords(self.raquette_1)[2]) and (coord[1] < self.canvas.coords(self.raquette_1)[3]) and (coord[3] > self.canvas.coords(self.raquette_1)[1]):
            self.dx = -self.dx
        if (coord[2] > self.canvas.coords(self.raquette_2)[0]) and (coord[1] < self.canvas.coords(self.raquette_2)[3]) and (coord[3] > self.canvas.coords(self.raquette_2)[1]):
            self.dx = -self.dx

        #système de points
        if self.canvas.coords(self.ball)[0] < 0:
            self.score_1 += 1
            self.canvas.destroy()
            if self.score_1 == self.win:
                self.end(0)
            else:
                return self.new_game()
        if self.canvas.coords(self.ball)[2] > self.largeur:
            self.score_2 += 1
            self.canvas.destroy()
            if self.score_2 == self.win:
                self.end(1)
            else:
                return self.new_game()

        self.canvas.move(self.ball, self.dx, self.dy)
        master.after(20, self.move_ball)
    
    def move_raq(self, event):
        #mouvements des raquettes
        coo1 = self.canvas.coords(self.raquette_1)
        coo2 = self.canvas.coords(self.raquette_2)
        if event.keysym == 'z':
            self.canvas.move(self.raquette_1, 0, -30)
        elif event.keysym == 's':
            self.canvas.move(self.raquette_1, 0, 30)
        elif event.keysym == 'Up': 
            self.canvas.move(self.raquette_2, 0, -30)
        elif event.keysym == 'Down': 
            self.canvas.move(self.raquette_2, 0, 30)

    def parametres(self):
        self.parameters = Frame(master, width=900, height=600, bg='white')
        self.parameters.grid_propagate(0)
        self.button_return = Button(self.parameters, text="Back", width=5, command=self.parametres_to_menu).grid(padx=3, pady=3)
        self.label_raq_col = Label(self.parameters, text="Raquettes", bg='white')
        self.label_ball_col = Label(self.parameters, text="Balle", bg='white')
        self.label_bg_col = Label(self.parameters, text="Background", bg='white')
        self.label_speed_ball = Label(self.parameters, text="vitesse balle", bg='white')
        self.label_win = Label(self.parameters, text="win points", bg='white')

        #couleur des raquettes
        self.list_raq_col = Listbox(self.parameters, width=5, height=5)
        for item in self.list_col:
            self.list_raq_col.insert(END, item)
        self.list_raq_col.bind('<ButtonRelease-1>', self.change_raq_col)

        #couleur de la balle
        self.list_ball_col = Listbox(self.parameters, width=5, height=5)
        for item in self.list_col:
            self.list_ball_col.insert(END, item)
        self.list_ball_col.bind('<ButtonRelease-1>', self.change_ball_col)

        #couleur du background
        self.list_bg_col = Listbox(self.parameters, width=5, height=5)
        for item in self.list_col:
            self.list_bg_col.insert(END, item)
        self.list_bg_col.bind('<ButtonRelease-1>', self.change_bg_col)

        #vitesse de la balle
        self.scale = Scale(self.parameters, orient=HORIZONTAL, from_=1, to=10, resolution=1, command=self.change_speed_ball)
        self.scale.set(self.dx)

        #points gagnants
        self.scale_points = Scale(self.parameters, orient=HORIZONTAL, from_=1, to=10, resolution=1, command=self.change_win)
        self.scale_points.set(self.win)

        self.label_raq_col.place(rely=0.2)
        self.list_raq_col.place(rely=0.3)

        self.label_ball_col.place(relx=0.2, rely= 0.2)
        self.list_ball_col.place(relx= 0.2, rely=0.3)

        self.label_bg_col.place(relx=0.4, rely= 0.2)
        self.list_bg_col.place(relx= 0.4, rely=0.3)

        self.label_speed_ball.place(relx=0.6, rely=0.2)
        self.scale.place(relx=0.6, rely=0.3)

        self.label_win.place(relx=0.8, rely=0.2)
        self.scale_points.place(relx=0.8, rely=0.3)

        self.parameters.grid()

    def change_raq_col(self, event):
        self.index = self.list_raq_col.curselection()
        self.raq_color = self.list_raq_col.get(self.index)

    def change_ball_col(self, event):
        self.index = self.list_ball_col.curselection()
        self.ball_color = self.list_ball_col.get(self.index)

    def change_bg_col(self, event): 
        self.index = self.list_bg_col.curselection()
        self.bg_color = self.list_bg_col.get(self.index)

    def change_speed_ball(self, event):
        self.dx = int(event)
        self.dy = int(event)

    def change_win(self, event):
        self.win = int(event)

    def end(self, side):
        self.now = round(time.time() - self.now_start, 2)

        if side == 0:
            self.winner = 'RIGHT'
        else:
            self.winner = 'LEFT'

        self.victoire = Frame(master, width=900, height=600, bg=self.bg_col)
        self.label_victoire = Label(self.victoire, text=f"PLAYER {self.winner} WIN in {self.now} seconds", bg='white')
        self.scores = Label(self.victoire, text=f'{self.score_left} - {self.score_right}')
        self.button_menu = Button(self.victoire, text="Menu", command=self.end_to_menu)
        self.button_replay = Button(self.victoire, text="Nouvelle partie", command=self.end_to_game)

        self.label_victoire.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.scores.place(relx=0.5, rely= 0.5, anchor=CENTER)
        self.button_menu.place(relx=0.4, rely= 0.7, anchor=CENTER)
        self.button_replay.place(relx=0.6, rely= 0.7, anchor=CENTER)
        self.victoire.grid()

    
    def menu_parametres(self):
        self.menu.destroy()
        self.parametres()

    def parametres_to_menu(self):
        self.parameters.destroy()
        self.Menu()

    def menu_to_game(self):
        self.menu.destroy()
        self.new_game()
        self.now_start = time.time()

    def end_to_menu(self):
        self.victoire.destroy()
        self.score_left = 0
        self.score_right = 0
        self.now_start = 0
        self.Menu()

    def end_to_game(self):
        self.victoire.destroy()
        self.score_left = 0
        self.score_right = 0
        self.now_start = time.time()
        self.now = 0
        self.new_game()


master = Tk()
master.title('Pong')
master.attributes('-fullscreen', 1)
pong = Pong()
master.mainloop()
