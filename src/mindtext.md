
bool joueur --> True si Joueur False si opposant
dict results --> Dictionnaire clé(noeud) valeur(p)

calcul de results :
pour chaque noeud accessible :
    dict.set(noeud.id, minmax(noeuds.remove(noeud), !(joueur)))

renvoie :
    si joueur :
        max(results.key => results.values)
    sinon :
        min(results.rey => results.values)

