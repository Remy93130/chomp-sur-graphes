#!/usr/bin/env python3
# -*- coding: utf8 -*-

from entity.node import *

from entity.parser import *

import copy

def chooseNode(nodes) :
	poisoned = getPoisoned(nodes)
	dictionnaire = dict()
	x = copy.deepcopy(nodes)
	for node in x.values() :
		temp = copy.deepcopy(x)
		delete_node(temp, node.id_node)
		dictionnaire[node.id_node] = evaluatePosition(temp, 100)
	print(dictionnaire)

	maxx = list(dictionnaire.keys())[0]
	for i in dictionnaire.keys() :
		if dictionnaire[i] > dictionnaire[maxx] :
			maxx = i
	return maxx

def getPoisoned(nodes) :
	for node in nodes.values() :
		if node.poisoned :
			return node.id_node
	return list(nodes.values())[0]

def printNodes(nodes) :
	for node in nodes.values() :
		print(node.id_node + " : ", end="")
		print(node.edges)

def evaluatePosition(nodes, time) :
	summ = 0
	player = True
	for i in range(time) :
		temp = copy.deepcopy(nodes)
		player = True

		while not noMorePoisonedNodes(temp) :
			delete_node(temp, safeIfPossible(temp))
			# delete_node(temp, random.choice(list(temp.keys())))
			player = not player

		if not player :
			summ += 1

	return summ / time

def safeIfPossible(nodes) :
	safe = safe_nodes(nodes)
	if not safe :
		return list(nodes.keys())[0]

	return random.choice(safe)

if __name__ == "__main__" :
	graph = Parser(700, "2.svg")
	nodes = graph.get_nodes()
	edges = graph.get_arrows()

	initialize_edges(nodes, edges)

	printNodes(nodes)

	print("Choosed node : "+chooseNode(nodes))