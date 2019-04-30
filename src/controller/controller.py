#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""The main controller for the game"""

# Global variables ------------------------------------------------------------

global height
global width
global options_settings

height = 805
width = 805

# Imports ---------------------------------------------------------------------

from view.GUI import *
from entity.parser import *
from entity.node import *
from entity.timer import *
from entity.game import *
from entity.main_generator import *
from entity.random_generator import *
from entity.option import *
import webbrowser
import random
import time
import IA
import os

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
                if options_settings.ShowAllTimer == "non":
                    self.timer1.hide()
                self.timer1.pause()
            if(self.game.turn == 2):
                self.timer2.start()
                self.timer2.show()
                if(self.timer2.run() == "done"): #view if the timer2 is done, 
                    return loose(self.gui,self.game.turn)
            else:
                if options_settings.ShowAllTimer == "non":
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
        return launchMenu(gui)
    gui.canvas.tag_bind('returnM','<Button-1>',auxMenu)

def loose(gui,player):
	gui.canvas.delete("all")
	gui.drawLoose(player)
	gui.actual = "loose"
	def auxMenu(evt, gui = gui):
		return launchMenu(gui)
	gui.canvas.tag_bind('menu','<Button-1>',auxMenu)
        

def launchOption(gui):
	global options_settings
	gui.actual = "option"
	gui.canvas.delete("all")
	gameplayOptions = ('facile', 'normal', 'difficile')
	colorOptions = ('bleue','rouge','vert','jaune','orange','violet','marron')
	yesNo = ('oui','non')
	choiceDifficult = StringVar()
	choiceColor = StringVar()
	choiceYesNo = StringVar()
	choiceDifficult.set(options_settings.difficulty)
	choiceColor.set(options_settings.colorPoison)
	choiceYesNo.set(options_settings.ShowAllTimer)
	colorPoison = OptionMenu(gui.screen, choiceColor, *colorOptions)
	gameplay = OptionMenu(gui.screen, choiceDifficult, *gameplayOptions)
	timerOption = OptionMenu(gui.screen, choiceYesNo, *yesNo)
	gui.drawOption(gameplay,colorPoison,timerOption)
	def auxMenu(evt, gui = gui):
		options_settings.difficulty = choiceDifficult.get()
		if choiceColor.get() == 'bleue':
			options_settings.colorPoison = 'lightblue'
		elif choiceColor.get() == 'rouge':
			options_settings.colorPoison = 'red'
		elif choiceColor.get() == 'vert':
			options_settings.colorPoison = 'green'
		elif choiceColor.get() == 'jaune':
			options_settings.colorPoison = 'yellow'
		elif choiceColor.get() == 'orange':
			options_settings.colorPoison = 'orange'
		elif choiceColor.get() == 'violet':
			options_settings.colorPoison = 'purple'
		elif choiceColor.get() == 'marron':
			options_settings.colorPoison = 'brown'
		options_settings.ShowAllTimer = choiceYesNo.get()
		gui.option = options_settings
		return launchMenu(gui)	
	def auxRanCrea(evt, gui = gui):
		return launchRandomCrea(gui)
	def auxManCrea(evt, gui = gui):
		return launchGameManualCrea(gui)
	gui.canvas.tag_bind('returnM','<Button-1>',auxMenu)
	gui.canvas.tag_bind('randomCrea','<Button-1>',auxRanCrea)
	gui.canvas.tag_bind('manualCrea','<Button-1>',auxManCrea)
	

def launchRandomCrea(gui):
	graph = None
	def wrongInput(input,useless):
		if input != '':
			try:
				val = int(input)
				if(val < 0):
					val = val * -1 
				return True
			except ValueError:
				return False
		return True
	gui.actual = "randomCrea"
	gui.canvas.delete("all")
	maxNodes = Entry(gui.screen,width=7,validate='key')
	maxNodes['validatecommand'] = (maxNodes.register(wrongInput),'%P','%S')
	minArrows = Entry(gui.screen,width=7,validate='key')
	minArrows['validatecommand'] = (minArrows.register(wrongInput),'%P','%S')
	maxArrows = Entry(gui.screen,width=7,validate='key')
	maxArrows['validatecommand'] = (maxArrows.register(wrongInput),'%P','%S')
	gui.drawRandomCrea(maxNodes,minArrows,maxArrows)
	def auxOption(evt, gui = gui):
		return launchOption(gui)
	def auxSave(evt, gui = gui,maxNodes = maxNodes ,minArrows = minArrows,maxArrows = maxArrows):
		nonlocal graph
		if graph == None:
			if maxNodes.get() == "":
				mN = 0
			else:
				mN = int(maxNodes.get())
			if maxNodes.get() == "":
				minA = 0
			else:
				minA = int(minArrows.get())
			if maxNodes.get() == "":
				maxA = 0
			else:
				maxA = int(maxArrows.get())
			graph = AutomatedGraph(mN, minA, maxA)
			graph.create()
		try:
			save_graph("")
			graph = None
		except Exception as e:
			pass
	def auxShow(evt, gui = gui,maxNodes = maxNodes ,minArrows = minArrows,maxArrows = maxArrows):
		nonlocal graph
		if maxNodes.get() == "":
			mN = 0
		else:
			mN = int(maxNodes.get())
		if maxNodes.get() == "":
			minA = 0
		else:
			minA = int(minArrows.get())
		if maxNodes.get() == "":
			maxA = 0
		else:
			maxA = int(maxArrows.get())
		
		graph = AutomatedGraph(mN, minA, maxA)
		graph.create()
		graph.display_graph()
	gui.canvas.tag_bind('returnO','<Button-1>',auxOption)
	gui.canvas.tag_bind('Save','<Button-1>',auxSave)
	gui.canvas.tag_bind('Show','<Button-1>',auxShow)
	
def launchGameManualCrea(gui):
	graph = None
	gui.actual = "manualCrea"
	gui.canvas.delete("all")
	text = Text(gui.screen,width=50,height=20)
	rules = "Bienvenue sur le créateur manuel \
de graphes!!!\nici vous pouvez indiquer quels sont \
les noeuds\nque vous voulez en séparant chaque numéro\n\
par du texte, si vous voulez un empoisonné\nalors tapez 'p' après le numéro\nune fois ceci fait, finissez par un point virgule.\n\
Ensuite vous pouvez initialiser\nles connexions entre les noeuds\n\
de la même manière, d'abords le predecesseur\nensuite ses successeurs\n\
en faisant attention à les séparer par du texte.\n\
Finissez par un point virgule.\n\
Exemple-----------------------:\n\
noeuds: 1,2,3,4,5,6,7,8p,9;\n\
connexions: 1 et 2 et 7; 7 et 8 et 9;\n\
6 et 2 et 5 et 4; 3 et 7;"
	
	text.insert('1.0', rules)
	gui.drawManualCrea(text)
	def auxOption(evt, gui = gui):
		var = text.get('1.0','end')
		return launchOption(gui)
	def auxShow(evt, gui = gui, text = text):
		nonlocal graph
		graph = manuelGeneration(text.get('1.0','end'))
		graph.create()
		graph.display_graph()
	def auxSave(evt, gui = gui, text = text):
		nonlocal graph
		graph = manuelGeneration(text.get('1.0','end'))
		graph.create()
		try:
			save_graph("")
		except Exception as e:
			pass
	gui.canvas.tag_bind('returnO','<Button-1>',auxOption)
	gui.canvas.tag_bind('Save','<Button-1>',auxSave)
	gui.canvas.tag_bind('Show','<Button-1>',auxShow)
	
		
		
def launchGameIA(gui,graphe_name):
    """ This function launch a party vs IA"""
    gui.actual = "gameIA"
    gui.canvas.delete("all")
    graph = Parser(height, graphe_name)
    gui.setGraphDimensions(graph.graph_width,graph.graph_height)
    gui.setNodes(graph.get_nodes())
    gui.setArrows(graph.get_arrows())
    initialize_edges(gui.nodes, gui.arrows)
    game = Game();
    gui.drawArrows()
    gui.drawNodes()
    gui.drawTurn(game)
    timer = Timer(gui, gui.drawTimer(),90) #start the timer, gui is Interface, gui.drawTimer() a function
                                          # for draw number of timer and the integer is minutes remaining
    gui.drawTimeRest(game.turn)
    condition = Condition(gui,timer,timer,game)
    condition.loop() # launch condition for tkinter loop

    for node in gui.nodes.values():
        def auxPlayTurn(evt, node = node, game = game, condition = condition):
            playTurnIA(gui,node,game,condition)
        gui.canvas.tag_bind("_"+node.id_node+"_",'<Button-1>', auxPlayTurn) # define all event

		
def playTurnIA(gui, node,game,condition):
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
	time.sleep(0) #We leave 1 second for the player to view his screen 
	if(game.turn == 2): 
		gui.canvas.delete("hider")
		delete_node(gui.nodes, IA.chooseNode(gui.nodes)) # IA delete
		if(noMorePoisonedNodes(gui.nodes)): # if there are no more poisoned, loose
			return loose(gui,game.turn)
		game.play()
		gui.canvas.delete("graph")
		gui.drawArrows()
		gui.drawNodes()
		gui.drawTurn(game)
		gui.drawTimeRest(game.turn)

def chooseGraphe(gui,number):
	gui.actual = "chooseGraphe"
	gui.canvas.delete("all")
	graphes = [x for x in os.listdir("../ressources/graphes/") if x.endswith(".svg")]
	Selection = Listbox(gui.screen)
	for i in range(len(graphes)):
		Selection.insert(i+1,graphes[i])
	print(graphes)
	gui.drawChooseGraphe(Selection)
	Selection.select_set(0) 
	Selection.event_generate("<<ListboxSelect>>")
	def auxPlay(evt,Selection = Selection,number = number):
		if number == 1:
			return launchGameIA(gui,Selection.get(Selection.curselection()))
		if number == 2:
			return launchGame(gui,Selection.get(Selection.curselection()))
	def auxVisu(evt,Selection = Selection,number = number):
		return graphVisualtion(gui,Selection.get(Selection.curselection()),number)
	def auxMenu(evt, gui = gui):
		return launchMenu(gui)	
	gui.canvas.tag_bind('returnM','<Button-1>',auxMenu)
	gui.canvas.tag_bind("play",'<Button-1>',auxPlay)
	gui.canvas.tag_bind("visual",'<Button-1>',auxVisu)
	
def graphVisualtion(gui,graph_name,number):
	gui.canvas.delete("all")
	graph = Parser(height, graph_name)
	gui.setGraphDimensions(graph.graph_width,graph.graph_height)
	gui.setNodes(graph.get_nodes())
	gui.setArrows(graph.get_arrows())
	initialize_edges(gui.nodes, gui.arrows)
	gui.drawArrows()
	gui.drawNodes()
	gui.drawMenuButton()
	def auxChoose(evt,number = number,gui = gui):
		return chooseGraphe(gui,number)
	gui.canvas.tag_bind('returnC','<Button-1>',auxChoose)
		
def launchGame(gui,graphe_name):
    """ This function launch a party"""
    gui.actual = "game"
    gui.canvas.delete("all")
    graph = Parser(height, graphe_name)
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
        def auxPlayTurn(evt, gui = gui, node = node, game = game):
            playTurn(gui, node, game)
            
        gui.canvas.tag_bind("_"+node.id_node+"_",'<Button-1>', auxPlayTurn) # define all event


def playTurn(gui, node, game) :
    delete_node(gui.nodes, node.id_node)
    if(noMorePoisonedNodes(gui.nodes)):
        return loose(gui,game.turn)
    game.play()
    gui.canvas.delete("graph")
    gui.drawArrows()
    gui.drawNodes()
    gui.drawTurn(game)
    gui.drawTimeRest(game.turn)

def launchMenu(gui):
	""" This function launch the menu of the game"""
	gui.actual = "menu"
	gui.canvas.delete("all")
	gui.drawMenu()
	gui.canvas.bind('<Button-1>',printcoord)
	def auxGameIA(evt, gui = gui): #On Tkinter, you can't pass arguments if you call event function
		return chooseGraphe(gui,1)          #with a bind, so we use auxiliar function for pass our arguments
	def auxGame(evt, gui = gui):
		return chooseGraphe(gui,2) 
	def auxOption(evt, gui = gui):
		return launchOption(gui)
	def auxAbout(evt, gui = gui):
		return about(gui)
	def auxRules(evt, gui = gui):
		return launchRules(gui)
	def noDescription(evt, gui = gui):
		gui.showDescription("")
	def description1J(evt, gui = gui):
		gui.showDescription("Disputez une partie\ncontre l'ordinateur,\nla difficulté dépend\nde celle choisis\ndans les options.")
	def description2J(evt, gui = gui):
		gui.showDescription("Disputez une partie\ncontre un joueur,\nidéal pour un duel.")
	def descriptionOp(evt, gui = gui):
		gui.showDescription("Personnalisez le jeu\nou créez des graphs. ")
	def descriptionAb(evt, gui = gui):
		gui.showDescription("Affichez les crédits.")
	def descriptionRu(evt, gui = gui):
		gui.showDescription("Affichez les règles de ce jeu.")
	gui.canvas.tag_bind("buttonChoice",'<Leave>',noDescription)
	gui.canvas.tag_bind("1joueur",'<Button-1>',auxGameIA)
	gui.canvas.tag_bind("1joueur",'<Motion>',description1J)
	gui.canvas.tag_bind("2joueur",'<Button-1>',auxGame)
	gui.canvas.tag_bind("2joueur",'<Motion>',description2J)
	gui.canvas.tag_bind("option",'<Button-1>',auxOption)
	gui.canvas.tag_bind("option",'<Motion>',descriptionOp)
	gui.canvas.tag_bind("about",'<Button-1>',auxAbout)
	gui.canvas.tag_bind("about",'<Motion>',descriptionAb)
	gui.canvas.tag_bind("rules",'<Button-1>',auxRules)
	gui.canvas.tag_bind("rules",'<Motion>',descriptionRu)


def about(gui):
	gui.actual = "about"
	gui.canvas.delete("all")
	gui.drawMenuButton()
	gui.drawCredit()
	def auxMenu(evt,gui = gui):
		return launchMenu(gui)
	def auxLinkedInLeo(evt,gui = gui):
		webbrowser.open('https://www.linkedin.com/in/leo-chardon/')
	def auxLinkedInRemy(evt,gui = gui):
		webbrowser.open('https://www.linkedin.com/in/r%C3%A9my-barberet/')
	def auxLinkedInMel(evt,gui = gui):
		webbrowser.open('https://www.linkedin.com/in/melissabuczko/')
	def auxLinkedInArmand(evt,gui = gui):
		webbrowser.open('https://www.linkedin.com/in/armand-colin-a95318155/')
	gui.canvas.tag_bind('returnC','<Button-1>',auxMenu)
	gui.canvas.tag_bind('leo','<Button-1>',auxLinkedInLeo)
	gui.canvas.tag_bind('remy','<Button-1>',auxLinkedInRemy)
	gui.canvas.tag_bind('mel','<Button-1>',auxLinkedInMel)
	gui.canvas.tag_bind('armand','<Button-1>',auxLinkedInArmand)

def printcoord(evt):
    print("x: ",evt.x,"; y: ",evt.y)

def controller():
	""" This function start the tkinter interface and the home of the game"""
	global options_settings
	options_settings = Option("difficile","lightblue","non")
	Interface = GUI(width,height)
	Interface.option = options_settings
	launchMenu(Interface)
	Interface.launchGUI() # This active the tkinter thread