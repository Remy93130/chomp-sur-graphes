#!/usr/bin/env python3
# -*- coding: utf8 -*-

from tkinter import *
from tkinter import font as tkFont


# from aggdraw import *

class GUI:
    def __init__(self, width, height):
        self.screen = Tk()
        self.screen.title("Le Chomp sur Graphe")
        self.canvas = Canvas(self.screen, width=width, height=height, background='white')
        self.height = height
        self.width = width
        self.nodes = None
        self.arrows = None
        self.graph_height = None
        self.graph_width = None
        self.actual = ""
        self.timerFont = tkFont.Font(family='Arial', size=int(self.height * 0.0200))

    def setArrows(self, arrows):
        for arrow in arrows:
            for i in range(len(arrow.points_sting)):
                if 0 == i % 2:
                    arrow.points_sting[i] = float(arrow.points_sting[i]) * (
                            self.graph_width / self.ogw) + self.width / 2 - self.graph_width * 0.49
                else:
                    print("y du point avant:", arrow.points_sting[i])
                    arrow.points_sting[i] = self.height - (self.height - float(arrow.points_sting[i])) * (
                            self.graph_height / self.ogh) - (self.height - self.graph_height - self.height * 0.166)
                    print("y du point mtn: ", arrow.points_sting[i])
        self.arrows = arrows

    def setNodes(self, nodes):
        self.nodes = nodes

    def setGraphDimensions(self, width, height):
        self.graph_height = int(height)
        self.graph_width = int(width)
        self.ogw = self.graph_width
        self.ogh = self.graph_height
        if self.width < self.graph_width:
            self.graph_width = self.width * 0.75
        if self.height - 100 < self.graph_height:
            self.graph_height = self.height * 0.75

    def drawLoose(self, player):
        loose_font = tkFont.Font(family='Arial', size=int(self.height * 0.0400), weight='bold')
        aria_respon = tkFont.Font(family='Arial', size=int(self.height * 0.0142), weight='bold')
        if self.actual == "gameIA" and player == 2:
            self.canvas.create_text(self.width * 0.50, self.height * 0.12, text="Vous avez gagné ! :)", tag="title",
                                    font=loose_font)
        elif self.actual == "gameIA" and player == 1:
            self.canvas.create_text(self.width * 0.50, self.height * 0.12, text="Vous avez perdu ... :(", tag="title",
                                    font=loose_font)
        else:
            self.canvas.create_text(self.width * 0.50, self.height * 0.12, text="Le joueur " + str(player) + " a perdu",
                                    tag="title", font=loose_font)
        self.canvas.create_rectangle(self.width * 0.393, self.height * 0.393, self.width * 0.607, self.height * 0.5,
                                     outline='black', fill='white', activefill='grey', width=1, tag='menu')
        self.canvas.create_text(self.width * 0.5, self.height * 0.45, text="retour au menu", tag="menu",
                                font=aria_respon)

    def drawTurn(self, game):
        aria_respon = tkFont.Font(family='Arial', size=int(self.height * 0.0142), weight='bold')
        if self.actual == "gameIA" and game.turn == 2:
            self.canvas.create_text(self.width * 0.50, self.height * 0.95, text="Au tour de l'IA", tag="graph",
                                    font=aria_respon)
        else:
            self.canvas.create_text(self.width * 0.50, self.height * 0.95, text="Au tour du joueur " + str(game.turn),
                                    tag="graph", font=aria_respon)

    def drawNode(self, node):
        if node.poisoned:
            color = 'lightblue'
        else:
            color = 'white'
        self.canvas.create_oval(
            node.coord[0] * (self.graph_width / self.ogw) - 27 + self.width / 2 - self.graph_width * 0.49,
            self.height - node.coord[1] * (self.graph_height / self.ogh) - 18 - (
                    self.height - self.graph_height - self.height * 0.166),
            node.coord[0] * (self.graph_width / self.ogw) + 27 + self.width / 2 - self.graph_width * 0.49,
            self.height - node.coord[1] * (self.graph_height / self.ogh) + 18 - (
                    self.height - self.graph_height - self.height * 0.166), tag=("_" + node.id_node + "_", "graph"),
            fill=color, width=1.5)
        self.canvas.create_text(
            node.coord[0] * (self.graph_width / self.ogw) + self.width / 2 - self.graph_width * 0.49,
            self.height - node.coord[1] * (self.graph_height / self.ogh) - (
                    self.height - self.graph_height - self.height * 0.166), text=node.id_node,
            tag=("_" + node.id_node + "_", "graph"))

    def delNode(self, node):
        self.canvas.delete('_' + node.id_node + '_')

    def drawTimer(self):
        return self.canvas.create_text(self.width * 0.50, self.height * 0.083, font=self.timerFont)

    def drawTimeRest(self, player):
        self.canvas.create_text(self.width * 0.50, self.height * 0.0555, font=self.timerFont,
                                text="Temps restant au joueur " + str(player) + " : ", tag="graph")

    def drawArrow(self, arrow):
        if arrow.id_arrow[0] in self.nodes and arrow.id_arrow[1] in self.nodes:
            self.canvas.create_line(
                float(arrow.points_line[0]) * (self.graph_width / self.ogw) + self.width / 2 - self.graph_width * 0.49,
                self.height - (self.height - arrow.points_line[1]) * (self.graph_height / self.ogh) - (
                        self.height - self.graph_height - self.height * 0.166),
                float(arrow.points_line[2]) * (self.graph_width / self.ogw) + self.width / 2 - self.graph_width * 0.49,
                self.height - (self.height - arrow.points_line[3]) * (self.graph_height / self.ogh) - (
                        self.height - self.graph_height - self.height * 0.166), tag="graph", width=0.5)
            self.canvas.create_polygon(arrow.points_sting, tag="graph", width=2.5)

    def drawArrows(self):
        print(self.arrows)
        for arrow in self.arrows:
            self.drawArrow(arrow)

    def drawNodes(self):
        print(self.nodes.values())
        self.canvas.create_rectangle(self.width / 2 - self.graph_width * 0.49, self.height * 0.166,
                                     self.width / 2 + self.graph_width - self.graph_width * 0.49,
                                     self.height * 0.166 + self.graph_height, outline='black', width=1)
        for node in self.nodes.values():
            self.drawNode(node)

    def hideTimer(self, tag):
        self.canvas.create_rectangle(self.width * 0.411, self.height * 0.066, self.width * 0.611, self.height * 0.094,
                                     outline='white', fill='white', width=0, tag=tag)

    def drawMenu(self):
        describe_font = tkFont.Font(family='Arial', size=int(self.height * 0.018))
        self.canvas.create_text(self.width * 0.65, self.height * 0.380, font=describe_font, tag="winDescription",
                                anchor="nw")
        title_font = tkFont.Font(family='Arial', size=int(self.height * 0.0442), weight='bold')
        self.canvas.create_text(self.width * 0.50, self.height * 0.12, text="Le Chomp sur Graphe", tag="title",
                                font=title_font)
        aria_respon = tkFont.Font(family='Arial', size=int(self.height * 0.0142), weight='bold')
        self.canvas.create_rectangle(self.width * 0.393, self.height * 0.214, self.width * 0.607, self.height * 0.321,
                                     outline='black', fill='white', activefill='grey', width=1,
                                     tag=('1joueur', 'buttonChoice'))
        self.canvas.create_rectangle(self.width * 0.393, self.height * 0.393, self.width * 0.607, self.height * 0.5,
                                     outline='black', fill='white', activefill='grey', width=1,
                                     tag=('2joueur', 'buttonChoice'))
        self.canvas.create_rectangle(self.width * 0.393, self.height * 0.571, self.width * 0.607, self.height * 0.678,
                                     outline='black', fill='white', activefill='grey', width=1,
                                     tag=('option', 'buttonChoice'))
        self.canvas.create_rectangle(self.width * 0.393, self.height * 0.75, self.width * 0.607, self.height * 0.857,
                                     outline='black', fill='white', activefill='grey', width=1,
                                     tag=('about', 'buttonChoice'))
        self.canvas.create_rectangle(self.width * 0.642, self.height * 0.235, self.width * 0.771, self.height * 0.3,
                                     outline='black', fill='white', activefill='grey', width=1,
                                     tag=('rules', 'buttonChoice'))
        self.canvas.create_text(self.width * 0.5, self.height * 0.271, text="1 Joueur", tag="1joueur", font=aria_respon)
        self.canvas.create_text(self.width * 0.5, self.height * 0.45, text="2 Joueurs", tag="2joueur", font=aria_respon)
        self.canvas.create_text(self.width * 0.5, self.height * 0.628, text="Options", tag="option", font=aria_respon)
        self.canvas.create_text(self.width * 0.5, self.height * 0.8, text="À propos", tag="about", font=aria_respon)
        self.canvas.create_text(self.width * 0.7, self.height * 0.271, text="règles", tag="rules", font=aria_respon)

    def drawRules(self):
        title_font = tkFont.Font(family='Arial', size=int(self.height * 0.0442), weight='bold')
        describe_font = tkFont.Font(family='Arial', size=int(self.width * 0.0165))
        self.canvas.create_text(self.width * 0.50, self.height * 0.12, text="Les règles du Chomp", tag="rulesTitle",
                                font=title_font)
        self.canvas.create_text(self.width * 0.200, self.height * 0.247, font=describe_font,
                                text="Le but du jeu est de forcer votre adversaire à cliquer sur le noeud "
                                     "empoisonné.\n\nLe jeu se joue tour par tour, si vous cliquez sur un noeud alors "
                                     "celui-ci\n\net tout les noeuds reliés à lui disparaitront.\n\nLe joueur ayant "
                                     "fait disparaitre le noeud empoisonné perd la partie.",
                                tag="rulesDescribe", anchor="nw")
        self.canvas.create_rectangle(self.height * 0.016, self.height * 0.016, self.height * 0.116, self.height * 0.072,
                                     tag="returnM", fill="white", activefill="grey")
        self.canvas.create_text(self.height * 0.064, self.height * 0.044, text="Menu", activefill="grey",
                                font=describe_font, tag="returnM")

    def showDescription(self, text):
        self.canvas.itemconfigure("winDescription", text=text)

    def launchGUI(self):
        self.canvas.pack()
        self.screen.mainloop()
