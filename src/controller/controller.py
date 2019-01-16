#!/usr/bin/env python3
# -*- coding: utf8 -*-

global height
height = 900
global width
width =  height

from view.GUI import *
from entity.parser import *
from entity.node import *
from entity.timer import *
from entity.game import *
import random
import time

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
		return launchGame(gui)
	gui.canvas.tag_bind("1joueur",'<Button-1>',auxGameIA)
	gui.canvas.tag_bind("2joueur",'<Button-1>',auxGame)
	gui.canvas.tag_bind("option",'<Button-1>',printcoord)
	gui.canvas.tag_bind("about",'<Button-1>',printcoord)
	gui.canvas.tag_bind("rules",'<Button-1>',printcoord)

class Condition:
	"""class for the condition, write condition in the function loop of this class"""
	def __init__(self,gui,timer,game):
		self.gui = gui
		self.timer = timer
		self.game = game
		
	def loop(self):
		if(self.gui.actual == "game" or self.gui.actual == "gameIA"): #view if we are in a party 
			if(self.timer.run() == "done"): #view if the timer is done, 
				return loose(self.gui,game.turn)
			return self.gui.screen.after(100, self.loop)
		else: #if not, we leave this loop
			return

def loose(gui,player):
	gui.canvas.delete("all")
	gui.drawLoose(player)
	gui.actual = "loose"
	def auxMenu(evt, gui = gui):
		return launchMenu(gui)
	gui.canvas.tag_bind('menu','<Button-1>',auxMenu)
		

def launchGameIA(gui):
	""" This function launch a party"""
	gui.actual = "gameIA"
	print(dir())
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
	timer = Timer(gui, gui.drawTimer(),1) #start the timer, gui is Interface, gui.drawTimer() a function
										  # for draw number of timer and the integer is minutes remaining
	gui.drawTimeRest()
	condition = Condition(gui,timer,game)
	condition.loop() # launch condition for tkinter loop
	for node in gui.nodes.values():
		def auxDelNode(evt, node = node, game = game):
			delete_node(gui.nodes, node.id_node)
			print(noMorePoisonedNodes(gui.nodes))
			if(noMorePoisonedNodes(gui.nodes)):
				return loose(gui,game.turn)
			game.play()
			gui.canvas.delete("graph")
			gui.drawArrows()
			gui.drawNodes()
			gui.drawTurn(game)
			gui.canvas.update()
			time.sleep(1) #We leave 1 second for the player to view his screen 
			if(game.turn == 2): 
				delete_node(gui.nodes,random.choice(list(gui.nodes.keys()))) # IA delete at random 
				if(noMorePoisonedNodes(gui.nodes)): # if there are no more poisoned, loose
					return loose(gui,game.turn)
				game.play() # change player turn
				gui.canvas.delete("graph")
				gui.drawArrows()
				gui.drawNodes()
				gui.drawTurn(game)
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
	timer = Timer(gui, gui.drawTimer(),1) #start the timer, gui is Interface, gui.drawTimer() a function
										  # for draw number of timer and the integer is minutes remaining
	gui.drawTimeRest()
	condition = Condition(gui,timer,game)
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
		gui.canvas.tag_bind("_"+node.id_node+"_",'<Button-1>', auxDelNode) # define all event

def controller():
	""" This function start the tkinter interface and the home of the game"""
	Interface = GUI(height,width) 
	launchMenu(Interface)
	Interface.launchGUI() # This active the tker threadint