# interface.py - ecran principal du jeu Re-Use
# pygame est la seule bibliotheque externe (obligatoire pour le projet)
import pygame
import webbrowser
from niveaux.niveau1 import lancer_niveau1

pygame.init()

# on utilise une taille fixe pour eviter les bugs d'affichage
LARGEUR = 1280
HAUTEUR = 720
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Re-Use")

# couleurs du jeu (on les met dans des variables pour pas se repeter)
VERT_BG = (10, 28, 13)
VERT_VIF = (72, 240, 100)
VERT_SOMB = (35, 80, 42)
BLANC = (230, 245, 232)
GRIS = (90, 115, 95)
NOIR = (5, 10, 6)

# polices pour le texte
police_titre = pygame.font.SysFont("Arial", 80)
police_sous = pygame.font.SysFont("Arial", 22)
police_btn = pygame.font.SysFont("Arial", 26)
police_petite = pygame.font.SysFont("Arial", 18)

# variables du jeu
son_active = True
volume = 7
meilleur_score = 0
ecran_actuel = "accueil"


# fonction pour afficher du texte centre a une position
def afficher_texte_centre(texte, police, couleur, cx, cy):
    rendu = police.render(texte, True, couleur)
    x = cx - rendu.get_width() // 2
    y = cy - rendu.get_height() // 2
    fenetre.blit(rendu, (x, y))


# fonction pour dessiner un bouton et retourner son rectangle
def dessiner_bouton(texte, cx, cy, largeur, hauteur, couleur_fond, couleur_texte):
    rect = pygame.Rect(cx - largeur // 2, cy - hauteur // 2, largeur, hauteur)
    pygame.draw.rect(fenetre, couleur_fond, rect, border_radius=14)
    afficher_texte_centre(texte, police_btn, couleur_texte, cx, cy)
    return rect


# dessine l'ecran d'accueil et retourne les rectangles des boutons
def dessiner_accueil():
    fenetre.fill(VERT_BG)

    # titre du jeu
    texte_re = police_titre.render("Re", True, VERT_VIF)
    texte_use = police_titre.render("-Use", True, BLANC)
    total_largeur = texte_re.get_width() + texte_use.get_width()
    tx = (LARGEUR - total_largeur) // 2
    ty = HAUTEUR // 2 - 200
    fenetre.blit(texte_re, (tx, ty))
    fenetre.blit(texte_use, (tx + texte_re.get_width(), ty))

    # sous-titre
    sous = police_sous.render("Trie - Recycle - Sauve la planete", True, GRIS)
    fenetre.blit(sous, ((LARGEUR - sous.get_width()) // 2, ty + 100))

    # boutons
    cy_jouer = HAUTEUR // 2 + 20
    rect_jouer = dessiner_bouton("Jouer", LARGEUR // 2, cy_jouer, 300, 65, VERT_VIF, NOIR)
    rect_param = dessiner_bouton("Parametres", LARGEUR // 2, cy_jouer + 100, 300, 55, VERT_SOMB, BLANC)

    # meilleur score si il y en a un
    if meilleur_score > 0:
        texte_score = police_petite.render("Meilleur score : {}".format(meilleur_score), True, VERT_VIF)
        fenetre.blit(texte_score, ((LARGEUR - texte_score.get_width()) // 2, ty + 130))

    # indication pour quitter
    esc = police_petite.render("ESC pour quitter", True, GRIS)
    fenetre.blit(esc, (20, HAUTEUR - 30))

    return rect_jouer, rect_param


# dessine l'ecran de selection des niveaux
def dessiner_niveaux():
    fenetre.fill(VERT_BG)

    titre = police_titre.render("Niveaux", True, BLANC)
    fenetre.blit(titre, ((LARGEUR - titre.get_width()) // 2, 50))

    # on met les infos des niveaux dans une liste de dictionnaires
    niveaux_info = [
        {"nom": "Niveau 1", "difficulte": "Debutant", "couleur": VERT_VIF},
        {"nom": "Niveau 2", "difficulte": "Intermediaire", "couleur": (255, 200, 60)},
        {"nom": "Niveau 3", "difficulte": "Expert", "couleur": (255, 90, 90)},
    ]

    liste_rects = []
    for i in range(len(niveaux_info)):
        cy = 220 + i * 120
        rect = pygame.Rect(LARGEUR // 2 - 250, cy - 40, 500, 80)
        pygame.draw.rect(fenetre, VERT_SOMB, rect, border_radius=12)

        couleur = niveaux_info[i]["couleur"]
        nom = niveaux_info[i]["nom"]
        diff = niveaux_info[i]["difficulte"]

        afficher_texte_centre(nom, police_btn, couleur, LARGEUR // 2 - 50, cy - 8)
        afficher_texte_centre(diff, police_petite, GRIS, LARGEUR // 2 - 50, cy + 18)
        liste_rects.append(rect)

    rect_retour = dessiner_bouton("Retour", LARGEUR // 2, HAUTEUR - 70, 250, 50, VERT_SOMB, BLANC)

    return liste_rects, rect_retour


# dessine le panneau des parametres par dessus l'ecran actuel
def dessiner_parametres():
    # fond sombre transparent
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    fenetre.blit(overlay, (0, 0))

    # panneau central
    panneau_w = 480
    panneau_h = 350
    px = (LARGEUR - panneau_w) // 2
    py = (HAUTEUR - panneau_h) // 2
    pygame.draw.rect(fenetre, VERT_SOMB, (px, py, panneau_w, panneau_h), border_radius=18)

    afficher_texte_centre("Parametres", police_btn, BLANC, LARGEUR // 2, py + 35)

    # option son
    texte_son = police_petite.render("Son", True, BLANC)
    fenetre.blit(texte_son, (px + 40, py + 90))

    if son_active:
        etat = "ON"
        couleur_etat = VERT_VIF
    else:
        etat = "OFF"
        couleur_etat = (210, 70, 70)

    rect_toggle = dessiner_bouton(etat, px + panneau_w - 80, py + 100, 90, 36, VERT_BG, couleur_etat)

    # volume
    texte_vol = police_petite.render("Volume : {} %".format(volume * 10), True, BLANC)
    fenetre.blit(texte_vol, (px + 40, py + 160))

    rect_moins = dessiner_bouton("-", px + panneau_w - 150, py + 170, 50, 36, VERT_BG, BLANC)
    rect_plus = dessiner_bouton("+", px + panneau_w - 80, py + 170, 50, 36, VERT_BG, BLANC)

    # barre de volume
    barre_x = px + 40
    barre_y = py + 220
    barre_l = panneau_w - 80
    pygame.draw.rect(fenetre, VERT_BG, (barre_x, barre_y, barre_l, 8), border_radius=4)
    if volume > 0:
        longueur_remplie = int(barre_l * volume / 10)
        pygame.draw.rect(fenetre, VERT_VIF, (barre_x, barre_y, longueur_remplie, 8), border_radius=4)

    # bouton fermer
    rect_fermer = dessiner_bouton("Fermer", LARGEUR // 2, py + panneau_h - 45, 200, 45, VERT_BG, GRIS)

    return rect_toggle, rect_moins, rect_plus, rect_fermer


# === boucle principale du jeu ===
horloge = pygame.time.Clock()
en_cours = True

while en_cours:

    # on dessine l'ecran selon la page actuelle
    if ecran_actuel == "accueil":
        rect_jouer, rect_param = dessiner_accueil()

    elif ecran_actuel == "niveaux":
        rects_niveaux, rect_retour = dessiner_niveaux()

    elif ecran_actuel == "parametres":
        # on dessine l'accueil en fond puis les parametres par dessus
        rect_jouer, rect_param = dessiner_accueil()
        rect_toggle, rect_moins, rect_plus, rect_fermer = dessiner_parametres()

    # on gere les evenements (clavier et souris)
    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            en_cours = False

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                if ecran_actuel == "parametres" or ecran_actuel == "niveaux":
                    ecran_actuel = "accueil"
                else:
                    en_cours = False

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx = ev.pos[0]
            my = ev.pos[1]

            if ecran_actuel == "accueil":
                if rect_jouer.collidepoint(mx, my):
                    ecran_actuel = "niveaux"
                elif rect_param.collidepoint(mx, my):
                    ecran_actuel = "parametres"

            elif ecran_actuel == "niveaux":
                if rect_retour.collidepoint(mx, my):
                    ecran_actuel = "accueil"

                elif rects_niveaux[0].collidepoint(mx, my):
                    resultat, score_obtenu = lancer_niveau1(fenetre, LARGEUR, HAUTEUR)
                    if score_obtenu > meilleur_score:
                        meilleur_score = score_obtenu
                    pygame.display.set_caption("Re-Use")
                    ecran_actuel = "accueil"
                    if resultat == "quitter":
                        en_cours = False

                elif rects_niveaux[1].collidepoint(mx, my):
                    print("Niveau 2 - a venir")

                elif rects_niveaux[2].collidepoint(mx, my):
                    print("Niveau 3 - a venir")

            elif ecran_actuel == "parametres":
                if rect_fermer.collidepoint(mx, my):
                    ecran_actuel = "accueil"
                elif rect_toggle.collidepoint(mx, my):
                    if son_active:
                        son_active = False
                    else:
                        son_active = True
                elif rect_moins.collidepoint(mx, my):
                    if volume > 0:
                        volume = volume - 1
                elif rect_plus.collidepoint(mx, my):
                    if volume < 10:
                        volume = volume + 1

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
