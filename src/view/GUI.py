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
	
	def setArrows(self,arrows):
		for arrow in arrows:
			for i in range(len(arrow.points_sting)):
				if(i%2==0):
					arrow.points_sting[i] = float(arrow.points_sting[i])*(self.graph_width/self.ogw)+self.width/2-self.graph_width*0.49
				else:
					arrow.points_sting[i] = float(arrow.points_sting[i])*(self.graph_height/self.ogh)-self.height+self.graph_height+self.height/6+self.difHeight
		self.arrows = arrows
		
	
	def setNodes(self,nodes):
		self.nodes = nodes
	
	def setGraphDimensions(self,width,height):
		print("height :",self.height)
		self.graph_height = int(height)
		self.graph_width = int(width)
		print("graph height:", self.graph_height)
		self.ogw = self.graph_width
		self.ogh = self.graph_height
		self.difHeight = 0
		if(self.width < self.graph_width):
			self.graph_width = self.width*0.75
		if(self.height-50 < self.graph_height):
			self.graph_height = self.height*0.75
			self.difHeight = 0
	def drawLoose(self,player):
		looseFont = tkFont.Font(family='Arial', size=int(self.height*0.0400), weight='bold')
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
			color = 'lightblue'
		else:
			color = 'white'
		self.canvas.create_oval(node.coord[0]*(self.graph_width/self.ogw) +self.width/2-self.graph_width*0.49 -27, self.graph_height+self.height/6 - node.coord[1]*(self.graph_height/self.ogh)-18, node.coord[0]*(self.graph_width/self.ogw) +self.width/2-self.graph_width*0.49 +27, self.graph_height+self.height/6 - node.coord[1]*(self.graph_height/self.ogh)+18,tag=("_"+node.id_node+"_","graph"),fill=color,width=1.5)
		self.canvas.create_text(node.coord[0]*(self.graph_width/self.ogw) +self.width/2-self.graph_width*0.49 , self.graph_height+self.height/6 - node.coord[1]*(self.graph_height/self.ogh), text=node.id_node,tag=("_"+node.id_node+"_","graph"))
		
	def delNode(self,node):
		self.canvas.delete('_'+node.id_node+'_')
	
	def drawTimer(self):
		return self.canvas.create_text(self.width*0.50,self.height*0.083,font=self.timerFont)
	
	def drawTimeRest(self,player):
		self.canvas.create_text(self.width*0.50,self.height*0.0555,font=self.timerFont,text="Temps restant au joueur "+str(player)+" : ",tag="graph")
	
	def drawArrow(self,arrow):
		if arrow.id_arrow[0] in self.nodes and arrow.id_arrow[1] in self.nodes:
				self.canvas.create_line(float(arrow.points_line[0])*(self.graph_width/self.ogw)+self.width/2-self.graph_width*0.49, arrow.points_line[1]*(self.graph_height/self.ogh)-self.height+self.graph_height+self.height/6+self.difHeight, float(arrow.points_line[2])*(self.graph_width/self.ogw)+self.width/2-self.graph_width*0.49, arrow.points_line[3]*(self.graph_height/self.ogh)-self.height+self.graph_height+self.height/6+self.difHeight,tag="graph",width=2.5)
				self.canvas.create_polygon(arrow.points_sting,tag="graph")
		
	def drawArrows(self):
		for arrow in self.arrows:
			self.drawArrow(arrow)
	def drawNodes(self):
		#self.canvas.create_rectangle(self.width/2-self.graph_width*0.49, self.height/6, self.width/2+self.graph_width-self.graph_width*0.49, self.height/6+self.graph_height,outline='black',width=1)
		for node in self.nodes.values():
			self.drawNode(node)
			
	def hideTimer(self,tag):
		self.canvas.create_rectangle(self.width*0.411, self.height*0.066, self.width*0.611, self.height*0.094,outline='white',fill='white',width=0,tag=tag)
	
	def drawMenu(self):
		titleFont = tkFont.Font(family='Arial', size=int(self.height*0.0442), weight='bold')
		self.canvas.create_text(self.width*0.50, self.height*0.12, text="Le Chomp sur Graphe",tag="title",font=titleFont)
		ariaRespon = tkFont.Font(family='Arial', size=int(self.height*0.0142), weight='bold')
		self.canvas.create_rectangle(self.width*0.393, self.height*0.214, self.width*0.607, self.height*0.321,outline='black',fill='white',activefill='grey',width=1,tag='1joueur')
		self.canvas.create_rectangle(self.width*0.393, self.height*0.393, self.width*0.607, self.height*0.5,outline='black',fill='white',activefill='grey',width=1,tag='2joueur')
		self.canvas.create_rectangle(self.width*0.393, self.height*0.571, self.width*0.607, self.height*0.678,outline='black',fill='white',activefill='grey',width=1,tag='option')
		self.canvas.create_rectangle(self.width*0.393, self.height*0.75, self.width*0.607, self.height*0.857,outline='black',fill='white',activefill='grey',width=1,tag='about')
		self.canvas.create_rectangle(self.width*0.642, self.height*0.235, self.width*0.771, self.height*0.3,outline='black',fill='white',activefill='grey',width=1,tag='rules')
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
		
		
	def launchGUI(self):
		self.canvas.pack()
		self.screen.mainloop()


