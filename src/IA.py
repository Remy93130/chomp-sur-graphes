#!/usr/bin/env python3
# -*- coding: utf8 -*-

from entity.node import *

from entity.parser import *

import copy

TIME = 30
DEEP = 3


def chooseNode(nodes):
    return minmax(nodes, True, DEEP)


# poisoned = getPoisoned(nodes)
# dictionnaire = dict()
# x = copy.deepcopy(nodes)
# for node in x.values() :
# 	temp = copy.deepcopy(x)
# 	delete_node(temp, node.id_node)
# 	dictionnaire[node.id_node] = evaluatePosition(temp, 100)
# print(dictionnaire)

# maxx = list(dictionnaire.keys())[0]
# for i in dictionnaire.keys() :
# 	if dictionnaire[i] > dictionnaire[maxx] :
# 		maxx = i
# return maxx

def getPoisoned(nodes):
    for node in nodes.values():
        if node.poisoned:
            return node.id_node
    return list(nodes.values())[0]


def printNodes(nodes):
    for node in nodes.values():
        print(node.id_node + " : ", end="")
        print(node.edges)


def evaluatePosition(nodes, time):
    summ = 0
    player = True
    for i in range(time):
        temp = copy.deepcopy(nodes)
        player = True

        while not no_more_poisoned_nodes(temp):
            delete_node(temp, safeIfPossible(temp))
            # delete_node(temp, random.choice(list(temp.keys())))
            player = not player

        if not player:
            summ += 1

    return summ / time


def safeIfPossible(nodes):
    safe = safe_nodes(nodes)
    if not safe:
        return list(nodes.keys())[0]

    return random.choice(safe)


def minmax(nodes, player, deep):
    if (deep == 0):
        if player:
            return 1 - evaluatePosition(nodes, TIME)
        else:
            return evaluatePosition(nodes, TIME)

    d = dict()

    # if deep == DEEP :
    # 	print("Beginning :\n")

    temp = copy.deepcopy(nodes)
    for node in nodes.keys():
        if (delete_node(temp, node)):
            if player:
                d[node] = 0
            else:
                d[node] = 1
        else:
            d[node] = minmax(temp, not player, deep - 1)
        temp = copy.deepcopy(nodes)

    # print("Step "+str(deep)+" got dict : ")
    # print(d)
    i = 0

    if player:
        i = maxPos(d)
    else:
        i = minPos(d)

    # print("min/max : "+str(d[i])+" from node "+str(i))
    if deep == DEEP:
        return i
    return d[i]


def maxPos(dic):
    i = list(dic.keys())[0]
    for _id in dic.keys():
        if dic[_id] > dic[i]:
            i = _id
    return i


def minPos(dic):
    i = list(dic.keys())[0]
    for _id in dic.keys():
        if dic[_id] < dic[i]:
            i = _id
    return i


if __name__ == "__main__":
    graph = Parser(700, "2.svg")
    nodes = graph.get_nodes()
    edges = graph.get_arrows()

    initialize_edges(nodes, edges)

    printNodes(nodes)

    print("Choosed node : " + chooseNode(nodes))
