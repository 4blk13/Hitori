###Partie 1###

def lire_grille(nom_fichier) :
    """Fonction qui à partir d'un fichier texte renvoie une liste de listre servant de 
    grille"""
    f = open(nom_fichier, 'r')
    text = f.read()
    liste = text.split('\n')
    i = 0
    while i != len(liste) :
        liste[i] = liste[i].split()
        i +=1
    liste.pop()
    f.close()
    return liste
    
    """ >>>lire_grille("niveau1")
        [['3', '2', '3', '4', '3'], ['2', '1', '4', '2', '1'], ['3', '4', '5', '1', '2'],   
        ['5', '3', '1', '1', '5'], ['5', '1', '2', '3', '5']]
    """
    
    
def afficher_grille(grille) :
    """Fonction qui permet d'afficher la grille sur la console à l'aide d'une liste de 
    liste"""
    i = 0
    j = 0
    ligne = ''
    while i != len(grille) :
        while j != len(grille[i]) :
            ligne = ligne + ' '+ grille[i][j]
            j +=1
        print(ligne)
        print('\r')
        ligne = ''
        i +=1
        j = 0
    return ''
    
    """ >>>afficher_grille([['3', '2', '3', '4', '3'], ['2', '1', '4', '2', '1'], ['3', '4', 
    '5', '1', '2'], ['5', '3', '1', '1', '5'], ['5', '1', '2', '3', '5']])
        3 2 3 4 3
        2 1 4 2 1
        3 4 5 1 2
        5 3 1 1 5
        5 1 2 3 5
    """


def ecrire_grille(grille, nom_fichier) :
    """Fonction qui écrit la grille dans le fichier texte"""
    f = open(nom_fichier, 'w') 
    i = 0
    j = 0
    ligne = ''
    while i != len(grille) :
        while j != len(grille[i]) :
            ligne = ligne + ' '+ str(grille[i][j])
            j +=1
        f.write(ligne)
        f.write('\r')
        ligne = ''
        i +=1
        j = 0
    f.close()
    return ''

##############


###Partie 2###
from random import *

def sans_conflit(grille, noircies) :
    """Fonction qui vérifie la règle 1 c'est-à-dire vérifie si dans toute la grille il y a des  
    chiffres présents plusieurs fois et visibles dans une même colonne et ligne"""
    for i in range(len(grille)) :
        for j in range(len(grille[i])) :
            for k in range(j+1, len(grille[i])) :
                if grille[i][j] == grille[i][k] :
                    if ( (i, j) not in noircies ) and ( (i, k) not in noircies) :
                        return False
    for i in range(len(grille)) :
        for j in range(len(grille)) :
            for k in range(j+1, len(grille[i])) :
                if grille[j][i] == grille[k][i] :
                    if ( (j, i) not in noircies) and ( (k, i) not in noircies) :
                        return False
    return True
    
    """ >>>sans_conflit([['3', '2', '3', '4', '3'], ['2', '1', '4', '2', '1'], ['3', '4', '5', 
        '1', '2'], ['5', '3', '1', '1', '5'], ['5', '1', '2', '3', '5']], {(0, 0), (4, 4)})
        False
    """


def sans_voisines_noircies(grille, noircies) :
    for element in noircies :
        (i, j) = element
        if (i+1, j) in noircies or (i-1, j) in noircies or (i, j-1) in noircies or (i, j+1) in noircies :
            return False
    return True
    
    """ >>>sans_voisines_noircies([['3', '2', '3', '4', '3'], ['2', '1', '4', '2', '1'], ['3', 
        '4', '5', '1', '2'], ['5', '3', '1', '1', '5'], ['5', '1', '2', '3', '5']], {(0, 0),        
        (4, 4)})
        True
    """



def dans_image(image, i, j):
    """Fonction intérmédiaire à la fonction connexe qui vérifie si une case est dans la 
    grille"""
    return (0 <= i < len(image) 
            and 0 <= j < len(image[i]))
    
    """ >>>dans_image([['3', '2', '3', '4', '3'], ['2', '1', '4', '2', '1'], ['3', '4', '5', 
        '1', '2'], ['5', '3', '1', '1', '5'], ['5', '1', '2', '3', '5']], 3, 4)
        True
    """


def voisins(i, j):
    """Renvoie la liste des voisins d'une case"""
    return [(i+1, j), 
            (i, j+1), 
            (i-1, j), 
            (i, j-1)]
    
    """ >>>voisins(3, 4)
        [(4, 4), (3, 5), (2, 4), (3, 3)]
    """


def grille_copie(grille, noircies) :
    """Autre fonction intérmédiaire à la fonction connexe qui copie une grille sous la forme 
    d'une grille contenant des 0 et des 1 avec 0 si la case est visible et 1 si la case est 
    noircie"""
    grille_copy = []
    for i in range(len(grille)) :
        grille_intermediaire = []
        for j in range(len(grille[i])) :
            if (i, j) in noircies :
                grille_intermediaire.append(1)
            else :
                grille_intermediaire.append(0)
        grille_copy.append(grille_intermediaire)
    return grille_copy
    
    """ >>>grille_copie([['3', '2', '3', '4', '3'], ['2', '1', '4', '2', '1'], ['3', '4', '5', 
        '1', '2'], ['5', '3', '1', '1', '5'], ['5', '1', '2', '3', '5']], {(0, 0), (4, 4)})
        [[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 1]]
    """


def connexe(grille, noircies, k, c_nouv, i=0, j=0):
    """Fonction qui vérifie la règle 3, c'est-à-dire vérifie si les cases blanches forment une 
    unique zone. Pour cela on se sert d'une grille_bis créée à l'aide de grille_copie qu'on 
    colorie à l'aide d'une nouvelle couleur pour pouvoir compter après le nombre de 0 
    restants""" 
    if k == 0 :
        i, j = randint(0, len(grille)-1), randint(0, len(grille[0])-1)
        while grille[i][j] != 0 :
            i, j = randint(0, len(grille)-1), randint(0, len(grille[0])-1)
    c_prec = grille[i][j]
    if c_prec == c_nouv :
        return
    grille[i][j] = c_nouv
    for vi, vj in voisins(i, j):
        if (dans_image(grille, vi, vj) 
            and grille[vi][vj] == c_prec):
                connexe(grille, noircies, i+1, c_nouv, vi, vj)
    blanc = 0
    for i in range(len(grille)) :
            blanc = blanc+ grille[i].count(0)
    if blanc == 0 :
        return True
    else :
        return False
    
    """ >>>connexe([['0', '1', '0', '0', '0'], ['0', '0', '1', '0', '1'], ['0', '1', '1', '1',
        '0'], ['0', '0', '1', '1', '0'], ['1', '1', '0', '0', '0']], {(0, 0), (4, 4)}, 3)
        True
    """

##############

###Partie 3 & 4###
from upemtk import *
import copy

lstgrilles = ["niveau1.txt", "niveau2.txt", "niveau3.txt", "niveau4.txt", "niveau5.txt"]

def initialise_grille(grille, longueur_case, case_depart, caseY_depart):
    yCase = 0
    for y in range(caseY_depart, len(grille) + caseY_depart):
        y *= longueur_case
        xCase = 0
        for x in range(case_depart, len(grille[0]) + case_depart):
            x *= longueur_case
            if grille[yCase][xCase] != None:
                rectangle(x, y, x + longueur_case, y + longueur_case, couleur = 'black', remplissage = 'white', epaisseur = 1, tag="grille")
                texte(x+longueur_case/2, y+longueur_case/2, grille[yCase][xCase], taille = longueur_case//2, ancrage="center", tag="grille")
            else:
                rectangle(x, y, x + longueur_case, y + longueur_case, couleur = 'black', remplissage = 'black', epaisseur = 1, tag="grille")
            xCase += 1
        yCase += 1
        
def pixel_vers_case(x, y): 
    """Fonction qui convertit un pixel de l'écran en case de la grille"""
    i = int(x // 75)
    j = int((y) // 75) - 2
    return i, j
    
    """>>>pixel_vers_case(200, 320)
        (2, 2)
    """
    
def cherche_noircies(grille):
    """Une fonction qui cherche les cases noires dans la grille"""
    noircies = set()
    for ligne in range(len(grille)):
        for case in range(len(grille[0])):
            if grille[ligne][case] == None:
                noircies.add((ligne, case))
    return noircies
    
def resoudre(grille, noircies, i, j, visualisation):
    if visualisation == True:
        efface("grille")
        initialise_grille(grille, 75, 0, 2)
        mise_a_jour()
    grilleconnexe = grille_copie(grille, noircies)
    regle1 = sans_conflit(grille, noircies)
    regle2 = sans_voisines_noircies(grille, noircies)
    regle3 = connexe(grilleconnexe, noircies, 0, 3)
    
    if (regle2 == False) or (regle3 == False):
        return None
        
    if (regle1 == True) and (regle2 == True) and (regle3 == True):
        return noircies
    
    else:
        
        if i >= len(grille):
            return None
        
        CheckLigne = True
        for ligne in range(len(grille)):
            if (grille[ligne][j] == grille[i][j]) and ligne != i:
                CheckLigne = False
        CheckColonne = True
        for colonne in range(len(grille[0]))    :
            if (grille[i][colonne] == grille[i][j]) and colonne != j:
                CheckColonne = False
            
        if CheckLigne == True and CheckColonne == True:
            if j < len(grille[0]) - 1:
                return resoudre(grille, noircies, i, j+1, visualisation)
            else:
                return resoudre(grille, noircies, i+1, 0, visualisation)
        else:
            save_case = grille[i][j]
            noircies.add((i, j))
            grille[i][j] = None
            if j < len(grille[0]) - 1:
                solution = resoudre(grille, noircies, i, j+1, visualisation)
            else:
                solution = resoudre(grille, noircies, i + 1, 0, visualisation)
               
            
            if solution is not None:
                return solution
            else:
                noircies.discard((i, j))
                grille[i][j] = save_case
                if j < len(grille[0]) - 1:
                    solution = resoudre(grille, noircies, i, j+1, visualisation)
                else:
                    solution = resoudre(grille, noircies, i + 1, 0, visualisation)
                
                if solution is not None:
                    return solution
                else:
                    return None
                
   
cree_fenetre(1000, 1000)
rectangle(0, 0, 1000, 1000, remplissage='black')
rectangle(240, 120, 760, 200, remplissage='white')
texte(420, 120, 'Hitori', couleur='black', taille=28)
rectangle(220, 220, 780, 300, remplissage='white')
texte(350, 220, 'Choix de la grille', couleur='black')

ecran = 0
grille_choisie = None
noircies = set()
while True:
    ev = attend_ev()
    tev = type_ev(ev)
    
    if (ecran == 0 and 220 <= abscisse(ev) <= 780 and 220 <= ordonnee(ev) <= 300) or (ecran == 2 and 260 <= abscisse(ev) <= 510 and 30 <= ordonnee(ev) <= 90):
        ecran = 1
        efface_tout()
        rectangle(0, 0, 1000, 1000, remplissage='black')
        case_depart = 1
        lstTailleGrilles = []
        for grille in lstgrilles:
            grille = lire_grille(grille)
            lstTailleGrilles.append([[case_depart*20, 400], [(len(grille[0]) + case_depart)*20,(len(grille) + 20)*20]])
            initialise_grille(grille, 20, case_depart, 20)
            case_depart += 10

    if ecran == 1 and tev == "ClicGauche" :
        for lstCoords in lstTailleGrilles:
            if lstCoords[0][0] <= abscisse(ev) <= lstCoords[1][0] and lstCoords[0][1] <= ordonnee(ev) <= lstCoords[1][1]:
                grille_choisie = lire_grille(lstgrilles[lstTailleGrilles.index(lstCoords)])
                noircies = set()
                lstCoups = []
                lstCoups.append(copy.deepcopy(grille_choisie))
                efface_tout()
                initialise_grille(grille_choisie, 75, 0, 2)
                ecran = 2
                rectangle(10, 30, 250, 90, remplissage="light grey")
                texte(130, 60, "Recommencer", couleur="black", ancrage="center")
                rectangle(260, 30, 510, 90, remplissage="light grey")
                texte(385, 60, "Changer de grille", couleur="black", ancrage="center")
                rectangle(520, 30, 740, 90, remplissage="light grey")
                texte(630, 60, "Annuler", couleur="black", ancrage="center")
                rectangle(750, 30, 990, 90, remplissage="light grey")
                texte(870, 60, "Quitter", couleur="black", ancrage="center")
                rectangle(600, 530, 990, 590, remplissage="light grey")
                texte(620, 540, "Solveur avec visualisation", couleur="black")
                rectangle(600, 600, 990, 660, remplissage="light grey")
                texte(620, 610, "Solveur sans visualisation", couleur="black")
                tev = None
                
    if ecran == 2 and tev == "ClicGauche" and 0 <= abscisse(ev) <= len(grille_choisie[0])*75 and 150 <=ordonnee(ev) <= len(grille_choisie)*75 + 150:
        i, j = pixel_vers_case(abscisse(ev), ordonnee(ev))
        grille_choisie[j][i] = None
        lstCoups.append(copy.deepcopy(grille_choisie))
        noircies = cherche_noircies(grille_choisie)
        efface("grille")
        initialise_grille(grille_choisie, 75, 0, 2)
                
    if ecran == 2 and 750 <= abscisse(ev) <= 990 and 30 <= ordonnee(ev) <= 90 :
        ferme_fenetre()
    
    if ecran == 2 and 10 <= abscisse(ev) <= 250 and 30 <= ordonnee(ev) <= 90 :
        grille_choisie = copy.deepcopy(lstCoups[0])
        noircies = set()
        efface("grille")
        initialise_grille(grille_choisie, 75, 0, 2)
        
    if ecran == 2 and 520 <= abscisse(ev) <= 740 and 30 <= ordonnee(ev) <= 90 :
        grille_choisie = copy.deepcopy(lstCoups[len(lstCoups) - 2])
        lstCoups.pop(len(lstCoups) - 1)
        noircies = cherche_noircies(grille_choisie)
        efface("grille")
        initialise_grille(grille_choisie, 75, 0, 2)
        
    if ecran == 2 and 600 <= abscisse(ev) <= 990 and 530 <= ordonnee(ev) <= 590 :
        noirciesSolveur = resoudre(grille_choisie, noircies, 0, 0, True)
        for (i, j) in noirciesSolveur:
            grille_choisie[i][j] = None
        efface("grille")
        initialise_grille(grille_choisie, 75, 0, 2)
        
    if ecran == 2 and 600 <= abscisse(ev) <= 990 and 600 <= ordonnee(ev) <= 660 :
        noirciesSolveur = resoudre(grille_choisie, noircies, 0, 0, False)
        for (i, j) in noirciesSolveur:
            grille_choisie[i][j] = None
        efface("grille")
        initialise_grille(grille_choisie, 75, 0, 2)
        
    if ecran == 2 :
        grilleconnexe = grille_copie(grille_choisie, {(0, 0)})
        if (sans_conflit(grille_choisie, noircies) == True) and (sans_voisines_noircies(grille_choisie, noircies) == True) and (connexe(grilleconnexe, noircies, 0, 3)) == True:
            rectangle(((len(grille_choisie[0])/2)*75)-100, ((len(grille_choisie)/2)*75 + 150) - 50, ((len(grille_choisie[0])/2)*75) + 100, ((len(grille_choisie)/2)*75 + 150) + 50, remplissage='white')
            texte((len(grille_choisie[0])/2)*75, (len(grille_choisie)/2)*75 + 150, 'Gagné !', couleur='green', taille=24, ancrage="center")
        