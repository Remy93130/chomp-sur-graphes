#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""The main controller for the game"""

# Global variables ------------------------------------------------------------

global height
height = 900
global width
width =  height

# Imports ---------------------------------------------------------------------

from view.GUI import *
from entity.parser import *
from entity.node import *
from entity.timer import *
from entity.game import *
import random
import time

# Classes ---------------------------------------------------------------------

class Condition:
    """class for the condition, write condition in the function loop of this class"""
    def __init__(self, gui, timer1, timer2, game):
        self.gui = gui
        self.timer1 = timer1
        self.timer2 = timer2
        self.game = game
        
    def loop(self):
        if(self.gui.actual == "game"): #view if we are in a players game 
            if(self.game.turn == 1):
                self.timer1.start()
                self.timer1.show()
                if(self.timer1.run() == "done"): #view if the timer1 is done, 
                    return loose(self.gui,self.game.turn)
            else:
                self.timer1.hide()
                self.timer1.pause()
            if(self.game.turn == 2):
                self.timer2.start()
                self.timer2.show()
                if(self.timer2.run() == "done"): #view if the timer2 is done, 
                    return loose(self.gui,self.game.turn)
            else:
                self.timer2.hide()
                self.timer2.pause()
            return self.gui.screen.after(100, self.loop)
        
        elif(self.gui.actual == "gameIA"): # view if we are in a IA game
            if(self.game.turn == 1):
                self.timer1.start() #start the timer
                self.timer1.show() # show it 
                if(self.timer1.run() == "done"): #view if the timer1 is done, 
                    return loose(self.gui,self.game.turn)
            return self.gui.screen.after(100, self.loop)
        else: #if not, we leave this loop
            self.timer1.stop() #stop the timer 
            self.timer2.stop() #stop the timer
            print("exit")
            return

# Functions -------------------------------------------------------------------

def launchRules(gui):
    gui.actual = "rules"
    gui.canvas.delete("all")
    gui.drawRules()
    def auxMenu(evt, gui = gui):
        launchMenu(gui)
    gui.canvas.tag_bind('returnM','<Button-1>',auxMenu)

def loose(gui,player):
    gui.canvas.delete("all")
    gui.drawLoose(player)
    gui.actual = "loose"
    def auxMenu(evt, gui = gui):
        return launchMenu(gui)
    gui.canvas.tag_bind('menu','<Button-1>',auxMenu)
        

def launchGameIA(gui):
    """ This function launch a party vs IA"""
    gui.actual = "gameIA"
    gui.canvas.delete("all")
    graph = Parser(height, "1.gv.svg")
    gui.setGraphDimensions(graph.graph_width,graph.graph_height)
    gui.setNodes(graph.get_nodes())
    gui.setArrows(graph.get_arrows())
    initialize_edges(gui.nodes, gui.arrows)
    game = Game();
    gui.drawArrows()
    gui.drawNodes()
    gui.drawTurn(game)
    timer = Timer(gui, gui.drawTimer(),60) #start the timer, gui is Interface, gui.drawTimer() a function
                                          # for draw number of timer and the integer is minutes remaining
    gui.drawTimeRest(game.turn)
    condition = Condition(gui,timer,timer,game)
    condition.loop() # launch condition for tkinter loop
    for node in gui.nodes.values():
        def auxDelNode(evt, node = node, game = game, condition = condition):
            delete_node(gui.nodes, node.id_node)
            if(noMorePoisonedNodes(gui.nodes)):
                return loose(gui,game.turn)
            game.play()
            gui.canvas.delete("graph")
            gui.drawArrows()
            gui.drawNodes()
            gui.drawTurn(game)
            gui.hideTimer("hider")
            condition.timer1.pause()
            gui.canvas.update()
            time.sleep(3) #We leave 1 second for the player to view his screen 
            if(game.turn == 2): 
                gui.canvas.delete("hider")
                delete_node(gui.nodes,random.choice(list(gui.nodes.keys()))) # IA delete at random 
                if(noMorePoisonedNodes(gui.nodes)): # if there are no more poisoned, loose
                    return loose(gui,game.turn)
                game.play()
                gui.canvas.delete("graph")
                gui.drawArrows()
                gui.drawNodes()
                gui.drawTurn(game)
                gui.drawTimeRest(game.turn)
        gui.canvas.tag_bind("_"+node.id_node+"_",'<Button-1>', auxDelNode) # define all event
        
def launchGame(gui):
    """ This function launch a party"""
    gui.actual = "game"
    gui.canvas.delete("all")
    graph = Parser(height, "1.gv.svg")
    gui.setGraphDimensions(graph.graph_width,graph.graph_height)
    gui.setNodes(graph.get_nodes())
    gui.setArrows(graph.get_arrows())
    initialize_edges(gui.nodes, gui.arrows)
    game = Game();
    gui.drawArrows()
    gui.drawNodes()
    gui.drawTurn(game)
    timer1 = Timer(gui, gui.drawTimer(),60) #start the timer, gui is Interface, gui.drawTimer() a function
                                          # for draw number of timer and the integer is minutes remaining
    timer2 = Timer(gui,gui.drawTimer(),60)
    gui.drawTimeRest(game.turn)
    condition = Condition(gui,timer1,timer2,game)
    condition.loop() # launch condition for tkinter loop
    for node in gui.nodes.values():
        def auxDelNode(evt, node = node, game = game):
            delete_node(gui.nodes, node.id_node)
            if(noMorePoisonedNodes(gui.nodes)):
                return loose(gui,game.turn)
            game.play()
            gui.canvas.delete("graph")
            gui.drawArrows()
            gui.drawNodes()
            gui.drawTurn(game)
            gui.drawTimeRest(game.turn)
        gui.canvas.tag_bind("_"+node.id_node+"_",'<Button-1>', auxDelNode) # define all event

def printcoord(evt):
    print("x: ",evt.x,"; y: ",evt.y)

def launchMenu(gui):
    """ This function launch the menu of the game"""
    gui.actual = "menu"
    gui.canvas.delete("all")
    gui.drawMenu()
    gui.canvas.bind('<Button-1>',printcoord)
    def auxGameIA(evt, gui = gui): #On Tkinter, you can't pass arguments if you call event function
        return launchGameIA(gui)          #with a bind, so we use auxiliar function for pass our arguments
    def auxGame(evt, gui = gui):
        return launchGame(gui)
    def auxOption(evt, gui = gui):
        return launchGame(gui)
    def auxAbout(evt, gui = gui):
        return launchGame(gui)
    def auxRules(evt, gui = gui):
        return launchRules(gui)
    gui.canvas.tag_bind("1joueur",'<Button-1>',auxGameIA)
    gui.canvas.tag_bind("2joueur",'<Button-1>',auxGame)
    gui.canvas.tag_bind("option",'<Button-1>',printcoord)
    gui.canvas.tag_bind("about",'<Button-1>',printcoord)
    gui.canvas.tag_bind("rules",'<Button-1>',auxRules)

def controller():
    """ This function start the tkinter interface and the home of the game"""
    Interface = GUI(height,width) 
    launchMenu(Interface)
    Interface.launchGUI() # This active the tker threadint