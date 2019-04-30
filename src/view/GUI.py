#!/usr/bin/env python3
# -*- coding: utf8 -*-

from tkinter import *
from tkinter import font as tkFont
# from aggdraw import *

class GUI:
	def __init__(self, width,height):
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
		self.timerFont = tkFont.Font(family='Arial', size=int(self.height*0.0200))
		self.option = None
		
	
	def setArrows(self,arrows):
		for arrow in arrows:
			for i in range(len(arrow.points_sting)):
				if(i%2==0):
					arrow.points_sting[i] = float(arrow.points_sting[i])*(self.graph_width/self.ogw)+self.width/2-self.graph_width*0.49
				else:
					print("y du point avant:",arrow.points_sting[i])
					arrow.points_sting[i] = self.height-(self.height-float(arrow.points_sting[i]))*(self.graph_height/self.ogh)-(self.height-self.graph_height-self.height*0.166)
					print("y du point mtn: ",arrow.points_sting[i])
		self.arrows = arrows
		
	
	def setNodes(self,nodes):
		self.nodes = nodes
	
	def setGraphDimensions(self,width,height):
		self.graph_height = int(height)
		self.graph_width = int(width)
		self.ogw = self.graph_width
		self.ogh = self.graph_height
		if(self.width < self.graph_width):
			self.graph_width = self.width*0.75
		if(self.height-100 < self.graph_height):
			self.graph_height = self.height*0.75

	def drawLoose(self,player):
		looseFont = tkFont.Font(family='Arial', size=int(self.height*0.0200), weight='bold')
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		if(self.actual == "gameIA" and player == 2):
			self.canvas.create_text(self.width*0.50, self.height*0.12, text="Vous avez gagné ! :)",tag="title",font=looseFont)
		elif(self.actual == "gameIA" and player == 1):
			self.canvas.create_text(self.width*0.50, self.height*0.12, text="Vous avez perdu ... :(",tag="title",font=looseFont)
		else:
			self.canvas.create_text(self.width*0.50, self.height*0.12, text="Le joueur "+str(player)+" a perdu",tag="title",font=looseFont)
		self.canvas.create_rectangle(self.width*0.393, self.height*0.393, self.width*0.607, self.height*0.5,outline='black',fill='white',activefill='grey',width=1,tag='menu')
		self.canvas.create_text(self.width*0.5, self.height*0.45, text="retour au menu",tag="menu",font=ariaRespon)
	
	def drawTurn(self,game):
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		if(self.actual == "gameIA" and game.turn == 2):
			self.canvas.create_text(self.width*0.50, self.height*0.95, text="Au tour de l'IA",tag="graph",font=ariaRespon)
		else:
			self.canvas.create_text(self.width*0.50, self.height*0.95, text="Au tour du joueur "+str(game.turn),tag="graph",font=ariaRespon)
	
	def drawNode(self,node):
		if node.poisoned:
			color = self.option.colorPoison
		else:
			color = 'white'
		self.canvas.create_oval(node.coord[0]*(self.graph_width/self.ogw)-27+self.width/2-self.graph_width*0.49, self.height-node.coord[1]*(self.graph_height/self.ogh)-18-(self.height-self.graph_height-self.height*0.166), node.coord[0]*(self.graph_width/self.ogw)+27+self.width/2-self.graph_width*0.49,self.height-node.coord[1]*(self.graph_height/self.ogh)+18-(self.height-self.graph_height-self.height*0.166),tag=("_"+node.id_node+"_","graph"),fill=color,width=1.5)
		self.canvas.create_text(node.coord[0]*(self.graph_width/self.ogw)+self.width/2-self.graph_width*0.49, self.height-node.coord[1]*(self.graph_height/self.ogh)-(self.height-self.graph_height-self.height*0.166), text=node.id_node,tag=("_"+node.id_node+"_","graph"))
		
	def delNode(self,node):
		self.canvas.delete('_'+node.id_node+'_')
	
	def drawTimer(self):
		return self.canvas.create_text(self.width*0.50,self.height*0.083,font=self.timerFont)
	
	def drawTimeRest(self,player):
		self.canvas.create_text(self.width*0.50,self.height*0.0555,font=self.timerFont,text="Temps restant au joueur "+str(player)+" : ",tag="graph")
	
	def drawArrow(self,arrow):
		if arrow.id_arrow[0] in self.nodes and arrow.id_arrow[1] in self.nodes:
				self.canvas.create_line(float(arrow.points_line[0])*(self.graph_width/self.ogw)+self.width/2-self.graph_width*0.49,self.height-(self.height-arrow.points_line[1])*(self.graph_height/self.ogh)-(self.height-self.graph_height-self.height*0.166), float(arrow.points_line[2])*(self.graph_width/self.ogw)+self.width/2-self.graph_width*0.49, self.height-(self.height-arrow.points_line[3])*(self.graph_height/self.ogh)-(self.height-self.graph_height-self.height*0.166),tag="graph",width=0.5)
				self.canvas.create_polygon(arrow.points_sting,tag="graph",width=2.5)
		
	def drawArrows(self):
		print(self.arrows)
		for arrow in self.arrows:
			self.drawArrow(arrow)
	def drawNodes(self):
		print(self.nodes.values())
		#self.canvas.create_rectangle(self.width/2-self.graph_width*0.49, self.height*0.166, self.width/2+self.graph_width-self.graph_width*0.49, self.height*0.166+self.graph_height,outline='black',width=1)
		for node in self.nodes.values():
			self.drawNode(node)
			
	def hideTimer(self,tag):
		self.canvas.create_rectangle(self.width*0.411, self.height*0.066, self.width*0.611, self.height*0.094,outline='white',fill='white',width=0,tag=tag)
	
	def drawMenu(self):
		describeFont = tkFont.Font(family='Arial', size=int(self.height*0.018))
		self.canvas.create_text(self.width*0.65, self.height*0.380,font=describeFont,tag="winDescription",anchor="nw")
		titleFont = tkFont.Font(family='Arial', size=int(self.height*0.0442), weight='bold')
		self.canvas.create_text(self.width*0.50, self.height*0.12, text="Le Chomp sur Graphe",tag="title",font=titleFont)
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		self.canvas.create_rectangle(self.width*0.393, self.height*0.214, self.width*0.607, self.height*0.321,outline='black',fill='white',activefill='grey',width=1,tag=('1joueur','buttonChoice'))
		self.canvas.create_rectangle(self.width*0.393, self.height*0.393, self.width*0.607, self.height*0.5,outline='black',fill='white',activefill='grey',width=1,tag=('2joueur','buttonChoice'))
		self.canvas.create_rectangle(self.width*0.393, self.height*0.571, self.width*0.607, self.height*0.678,outline='black',fill='white',activefill='grey',width=1,tag=('option','buttonChoice'))
		self.canvas.create_rectangle(self.width*0.393, self.height*0.75, self.width*0.607, self.height*0.857,outline='black',fill='white',activefill='grey',width=1,tag=('about','buttonChoice'))
		self.canvas.create_rectangle(self.width*0.642, self.height*0.235, self.width*0.771, self.height*0.3,outline='black',fill='white',activefill='grey',width=1,tag=('rules','buttonChoice'))
		self.canvas.create_text(self.width*0.5, self.height*0.271, text="1 Joueur",tag="1joueur",font=ariaRespon)
		self.canvas.create_text(self.width*0.5, self.height*0.45, text="2 Joueurs",tag="2joueur",font=ariaRespon)
		self.canvas.create_text(self.width*0.5, self.height*0.628, text="Options",tag="option",font=ariaRespon)
		self.canvas.create_text(self.width*0.5, self.height*0.8, text="À propos",tag="about",font=ariaRespon)
		self.canvas.create_text(self.width*0.7, self.height*0.271, text="règles",tag="rules",font=ariaRespon)
		
	def drawRules(self):
		titleFont = tkFont.Font(family='Arial', size=int(self.height*0.0442), weight='bold')
		describeFont = tkFont.Font(family='Arial', size=int(self.width*0.0165))
		self.canvas.create_text(self.width*0.50, self.height*0.12, text="Les règles du Chomp",tag="rulesTitle",font=titleFont)
		self.canvas.create_text(self.width*0.200, self.height*0.247,font=describeFont, text="Le but du jeu est de forcer votre adversaire à cliquer sur le noeud empoisonné.\n\nLe jeu se joue tour par tour, si vous cliquez sur un noeud alors celui-ci\n\net tout les noeuds reliés à lui disparaitront.\n\nLe joueur ayant fait disparaitre le noeud empoisonné perd la partie.",tag="rulesDescribe",anchor="nw")
		self.canvas.create_rectangle(self.height*0.016,self.height*0.016,self.height*0.116,self.height*0.072,tag="returnM",fill="white",activefill="grey")
		self.canvas.create_text(self.height*0.064,self.height*0.044,text="Menu",activefill="grey",font=describeFont,tag="returnM")
		
	def drawOption(self,gameplay,colorPoison,timerOption):
		titleFont = tkFont.Font(family='Arial', size=int(self.height*0.0442), weight='bold')
		describeFont = tkFont.Font(family='Arial', size=int(self.width*0.0165))
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		self.canvas.create_text(self.width*0.50, self.height*0.12, text="Options",tag="optionTitle",font=titleFont)
		self.canvas.create_rectangle(self.height*0.016,self.height*0.016,self.height*0.116,self.height*0.072,tag="returnM",fill="white",activefill="grey")
		self.canvas.create_text(self.height*0.064,self.height*0.044,text="Menu",activefill="grey",font=describeFont,tag="returnM")
		#self.canvas.create_text(self.width*0.69,self.height*0.32,text="Difficulté:",font=describeFont,tag="difficulty")
		#self.canvas.create_window(self.width*0.69,self.height*0.36,window=gameplay)
		self.canvas.create_text(self.width*0.69,self.height*0.42,text="Couleur du noeud empoisonné:",font=describeFont,tag="colorPoison")
		self.canvas.create_window(self.width*0.69,self.height*0.46,window=colorPoison)
		#self.canvas.create_text(self.width*0.69,self.height*0.52,text="Afficher les timers des joueurs\nsimultanément:",font=describeFont,tag="timerOption")
		#self.canvas.create_window(self.width*0.69,self.height*0.56,window=timerOption)
		self.canvas.create_rectangle(self.width*0.149, self.height*0.322, self.width*0.347,self.height*0.416,outline='black',fill='white',activefill='grey',width=1,tag=('randomCrea','buttonChoice'))
		self.canvas.create_rectangle(self.width*0.149, self.height*0.5, self.width*0.347,self.height*0.602,outline='black',fill='white',activefill='grey',width=1,tag=('manualCrea','buttonChoice'))
		self.canvas.create_text(self.width*0.248,self.height*0.360,text="Création automatique\nde graphe",activefill="grey",font=ariaRespon,tag="randomCrea")
		self.canvas.create_text(self.width*0.248,self.height*0.559,text="Création manuelle\nde graphe",activefill="grey",font=ariaRespon,tag="manualCrea")
	
	def drawRandomCrea(self,maxNodes,minArrows,maxArrows):
		titleFont = tkFont.Font(family='Arial', size=int(self.height*0.0442), weight='bold')
		describeFont = tkFont.Font(family='Arial', size=int(self.width*0.0165))
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		self.canvas.create_rectangle(self.height*0.016,self.height*0.016,self.height*0.116,self.height*0.072,tag="returnO",fill="white",activefill="grey")
		self.canvas.create_text(self.height*0.064,self.height*0.044,text="Options",activefill="grey",font=describeFont,tag="returnO")
		self.canvas.create_text(self.width*0.50, self.height*0.12, text="Création automatique de graphe",tag="optionTitle",font=titleFont)
		self.canvas.create_text(self.width*0.496,self.height*0.223,text="Nombre de sommets souhaités:",font=describeFont,tag="maxNodes")
		self.canvas.create_text(self.width*0.496,self.height*0.310,text="Nombre de liaisons minimum par sommet souhaités:",font=describeFont,tag="minArr")
		self.canvas.create_text(self.width*0.496,self.height*0.397,text="Nombre de liaisons maximum par sommet:",font=describeFont,tag="maxArr")
		self.canvas.create_window(self.width*0.496,self.height*0.26,window=maxNodes)
		self.canvas.create_window(self.width*0.496,self.height*0.347,window=minArrows)
		self.canvas.create_window(self.width*0.496,self.height*0.434,window=maxArrows)
		self.canvas.create_rectangle(self.width*0.428, self.height*0.515, self.width*0.577,self.height*0.583,outline='black',fill='white',activefill='grey',width=1,tag=('Show','buttonChoice'))
		self.canvas.create_text(self.width*0.5,self.height*0.552,text="Prévisualiser",font=describeFont,tag="Show")
		self.canvas.create_rectangle(self.width*0.428, self.height*0.627, self.width*0.577,self.height*0.695,outline='black',fill='white',activefill='grey',width=1,tag=('Save','buttonChoice'))
		self.canvas.create_text(self.width*0.5,self.height*0.664,text="Sauvegarder",font=describeFont,tag="Save")
		
	def drawChooseGraphe(self,graphList):
		titleFont = tkFont.Font(family='Arial', size=int(self.height*0.0442), weight='bold')
		describeFont = tkFont.Font(family='Arial', size=int(self.width*0.0165))
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		self.canvas.create_rectangle(self.height*0.016,self.height*0.016,self.height*0.116,self.height*0.072,tag="returnM",fill="white",activefill="grey")
		self.canvas.create_text(self.height*0.064,self.height*0.044,text="Menu",activefill="grey",font=describeFont,tag="returnM")
		self.canvas.create_text(self.width*0.50, self.height*0.12, text="Choississez votre graphe",tag="chooseTitle",font=titleFont)
		self.canvas.create_window(self.width*0.496,self.height*0.372,window=graphList)
		self.canvas.create_rectangle(self.width*0.881,self.height*0.919,self.width*0.981,self.height*0.975,tag="play",fill="white",activefill="grey")
		self.canvas.create_text(self.width*0.931,self.height*0.944,text="Jouer",activefill="grey",font=describeFont,tag="play")
		self.canvas.create_rectangle(self.width*0.422,self.height*0.521,self.width*0.571,self.height*0.583,tag="visual",fill="white",activefill="grey")
		self.canvas.create_text(self.width*0.496,self.height*0.546,text="Visualiser",activefill="grey",font=describeFont,tag="visual")
		
	def drawManualCrea(self,text):
		titleFont = tkFont.Font(family='Arial', size=int(self.height*0.0442), weight='bold')
		describeFont = tkFont.Font(family='Arial', size=int(self.width*0.0165))
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		self.canvas.create_text(self.width*0.50, self.height*0.12, text="Création Manuelle de graphe",tag="optionTitle",font=titleFont)
		self.canvas.create_window(self.width*0.496,self.height*0.447,window=text)
		self.canvas.create_rectangle(self.width*0.881,self.height*0.919,self.width*0.981,self.height*0.975,tag="Save",fill="white",activefill="grey")
		self.canvas.create_text(self.width*0.931,self.height*0.944,text="sauver",activefill="grey",font=describeFont,tag="Save")
		self.canvas.create_rectangle(self.width*0.683,self.height*0.919,self.width*0.819,self.height*0.975,tag="Show",fill="white",activefill="grey")
		self.canvas.create_text(self.width*0.751,self.height*0.944,text="prévisualiser",activefill="grey",font=describeFont,tag="Show")
		self.canvas.create_rectangle(self.height*0.016,self.height*0.016,self.height*0.116,self.height*0.072,tag="returnO",fill="white",activefill="grey")
		self.canvas.create_text(self.height*0.064,self.height*0.044,text="Options",activefill="grey",font=describeFont,tag="returnO")
		
	def drawCredit(self):
		titleFont = tkFont.Font(family='Arial', size=int(self.height*0.0442), weight='bold')
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		self.canvas.create_text(self.width*0.50, self.height*0.12, text="© Léo Chardon",tag="leo",font=titleFont,activefill="lightblue")
		self.canvas.create_text(self.width*0.50, self.height*0.22, text="© Remy Barberet",tag="remy",font=titleFont,activefill="lightblue")
		self.canvas.create_text(self.width*0.50, self.height*0.32, text="© Melissa Buczko",tag="mel",font=titleFont,activefill="lightblue")
		self.canvas.create_text(self.width*0.50, self.height*0.42, text="© Armand Colin",tag="armand",font=titleFont,activefill="lightblue")
		self.canvas.create_text(self.width*0.50, self.height*0.52, text="Projet tuteuré par Monsieur Samuele Giraudo\ndans le cadre d'un DUT Informatique 2nd année à l'UPEM",tag="optionTitle",font=ariaRespon)
		
	def showDescription(self,text):
		self.canvas.itemconfigure("winDescription",text=text)
		
	def drawMenuButton(self):
		describeFont = tkFont.Font(family='Arial', size=int(self.width*0.0165))
		self.canvas.create_rectangle(self.height*0.016,self.height*0.016,self.height*0.116,self.height*0.072,tag="returnC",fill="white",activefill="grey")
		self.canvas.create_text(self.height*0.064,self.height*0.044,text="Retour",activefill="grey",font=describeFont,tag="returnC")

	
	def launchGUI(self):
		self.canvas.pack()
		self.screen.mainloop()


