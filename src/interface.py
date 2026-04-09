import pygame
import webbrowser
from niveaux.niveau1 import lancer_niveau1
from niveaux.niveau2 import lancer_niveau2
from niveaux.niveau3 import lancer_niveau3

pygame.init()

LARGEUR = 1280
HAUTEUR = 720
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Re-Use")

VERT_F = (45, 90, 39)
VERT_C = (123, 198, 126)
BEIGE = (245, 240, 232)
ORANGE = (232, 137, 43)
BLANC = (255, 255, 255)
NOIR = (30, 30, 30)

police_titre = pygame.font.SysFont("Arial", 80, bold=True)
police_sous = pygame.font.SysFont("Arial", 22)
police_btn = pygame.font.SysFont("Arial", 26, bold=True)
police_petite = pygame.font.SysFont("Arial", 18)

son_active = True
volume = 7
meilleur_score = 0
ecran_actuel = "accueil"
horloge = pygame.time.Clock()


def afficher_texte_centre(texte, police, couleur, cx, cy):
    rendu = police.render(texte, True, couleur)
    x = cx - rendu.get_width() // 2
    y = cy - rendu.get_height() // 2
    fenetre.blit(rendu, (x, y))


def dessiner_bouton(texte, cx, cy, largeur, hauteur, couleur_fond, couleur_texte):
    rect = pygame.Rect(cx - largeur // 2, cy - hauteur // 2, largeur, hauteur)
    pygame.draw.rect(fenetre, couleur_fond, rect, border_radius=14)
    afficher_texte_centre(texte, police_btn, couleur_texte, cx, cy)
    return rect


def fondu_noir():
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.fill((0, 0, 0))
    alpha = 0
    while alpha <= 255:
        overlay.set_alpha(alpha)
        fenetre.blit(overlay, (0, 0))
        pygame.display.flip()
        horloge.tick(60)
        alpha = alpha + 12


def dessiner_accueil():
    fenetre.fill(BEIGE)

    pygame.draw.rect(fenetre, VERT_F, (0, 0, LARGEUR, 8))
    pygame.draw.rect(fenetre, VERT_F, (0, HAUTEUR - 8, LARGEUR, 8))

    texte_re = police_titre.render("Re", True, ORANGE)
    texte_use = police_titre.render("-Use", True, VERT_F)
    total_largeur = texte_re.get_width() + texte_use.get_width()
    tx = (LARGEUR - total_largeur) // 2
    ty = HAUTEUR // 2 - 200
    fenetre.blit(texte_re, (tx, ty))
    fenetre.blit(texte_use, (tx + texte_re.get_width(), ty))

    pygame.draw.rect(fenetre, ORANGE, (LARGEUR // 2 - 60, ty + 90, 120, 4), border_radius=2)

    sous = police_sous.render("Trie - Recycle - Sauve la planete", True, VERT_F)
    fenetre.blit(sous, ((LARGEUR - sous.get_width()) // 2, ty + 110))

    cy_jouer = HAUTEUR // 2 + 30
    rect_jouer = dessiner_bouton("Jouer", LARGEUR // 2, cy_jouer, 300, 65, ORANGE, BLANC)
    rect_param = dessiner_bouton("Parametres", LARGEUR // 2, cy_jouer + 100, 300, 55, VERT_F, BLANC)

    if meilleur_score > 0:
        texte_score = police_petite.render("Meilleur score : {}".format(meilleur_score), True, ORANGE)
        fenetre.blit(texte_score, ((LARGEUR - texte_score.get_width()) // 2, ty + 145))

    esc = police_petite.render("ESC pour quitter", True, VERT_C)
    fenetre.blit(esc, (20, HAUTEUR - 30))

    return rect_jouer, rect_param


def dessiner_niveaux():
    fenetre.fill(BEIGE)

    titre = police_titre.render("Niveaux", True, VERT_F)
    fenetre.blit(titre, ((LARGEUR - titre.get_width()) // 2, 50))
    pygame.draw.rect(fenetre, ORANGE, (LARGEUR // 2 - 50, 140, 100, 4), border_radius=2)

    niveaux_info = [
        {"nom": "Niveau 1 - Le Lanceur", "difficulte": "Debutant", "couleur": VERT_C},
        {"nom": "Niveau 2 - Le Convoyeur", "difficulte": "Intermediaire", "couleur": ORANGE},
        {"nom": "Niveau 3 - L'Atelier", "difficulte": "Expert", "couleur": (220, 80, 60)},
    ]

    liste_rects = []
    for i in range(len(niveaux_info)):
        cy = 230 + i * 130
        rect = pygame.Rect(LARGEUR // 2 - 260, cy - 45, 520, 90)
        pygame.draw.rect(fenetre, VERT_F, rect, border_radius=14)
        pygame.draw.rect(fenetre, niveaux_info[i]["couleur"], (rect.x, rect.y, 8, 90), border_radius=4)

        afficher_texte_centre(niveaux_info[i]["nom"], police_btn, BLANC, LARGEUR // 2 + 5, cy - 12)
        afficher_texte_centre(niveaux_info[i]["difficulte"], police_petite, VERT_C, LARGEUR // 2 + 5, cy + 18)
        liste_rects.append(rect)

    rect_retour = dessiner_bouton("Retour", LARGEUR // 2, HAUTEUR - 70, 250, 50, VERT_F, BLANC)

    return liste_rects, rect_retour


def dessiner_parametres():
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    fenetre.blit(overlay, (0, 0))

    panneau_w = 480
    panneau_h = 350
    px = (LARGEUR - panneau_w) // 2
    py = (HAUTEUR - panneau_h) // 2
    pygame.draw.rect(fenetre, BEIGE, (px, py, panneau_w, panneau_h), border_radius=18)
    pygame.draw.rect(fenetre, VERT_F, (px, py, panneau_w, panneau_h), 3, border_radius=18)

    afficher_texte_centre("Parametres", police_btn, VERT_F, LARGEUR // 2, py + 35)

    texte_son = police_petite.render("Son", True, VERT_F)
    fenetre.blit(texte_son, (px + 40, py + 90))

    if son_active:
        etat = "ON"
        couleur_etat = VERT_C
    else:
        etat = "OFF"
        couleur_etat = (200, 80, 60)

    rect_toggle = dessiner_bouton(etat, px + panneau_w - 80, py + 100, 90, 36, couleur_etat, BLANC)

    texte_vol = police_petite.render("Volume : {} %".format(volume * 10), True, VERT_F)
    fenetre.blit(texte_vol, (px + 40, py + 160))

    rect_moins = dessiner_bouton("-", px + panneau_w - 150, py + 170, 50, 36, VERT_F, BLANC)
    rect_plus = dessiner_bouton("+", px + panneau_w - 80, py + 170, 50, 36, VERT_F, BLANC)

    barre_x = px + 40
    barre_y = py + 220
    barre_l = panneau_w - 80
    pygame.draw.rect(fenetre, VERT_C, (barre_x, barre_y, barre_l, 8), border_radius=4)
    if volume > 0:
        longueur_remplie = int(barre_l * volume / 10)
        pygame.draw.rect(fenetre, ORANGE, (barre_x, barre_y, longueur_remplie, 8), border_radius=4)

    rect_fermer = dessiner_bouton("Fermer", LARGEUR // 2, py + panneau_h - 45, 200, 45, ORANGE, BLANC)

    return rect_toggle, rect_moins, rect_plus, rect_fermer


def lancer_niveau_boucle(niveau_depart):
    global meilleur_score
    niveau_en_cours = niveau_depart
    while niveau_en_cours >= 1 and niveau_en_cours <= 3:
        fondu_noir()
        if niveau_en_cours == 1:
            resultat, score_obtenu = lancer_niveau1(fenetre, LARGEUR, HAUTEUR)
        elif niveau_en_cours == 2:
            resultat, score_obtenu = lancer_niveau2(fenetre, LARGEUR, HAUTEUR)
        else:
            resultat, score_obtenu = lancer_niveau3(fenetre, LARGEUR, HAUTEUR)
        if score_obtenu > meilleur_score:
            meilleur_score = score_obtenu
        if resultat == "suivant":
            niveau_en_cours = niveau_en_cours + 1
        elif resultat == "recommencer":
            pass
        elif resultat == "quitter":
            return "quitter"
        else:
            return "menu"
    fondu_noir()
    return "menu"


en_cours = True

while en_cours:

    if ecran_actuel == "accueil":
        rect_jouer, rect_param = dessiner_accueil()
    elif ecran_actuel == "niveaux":
        rects_niveaux, rect_retour = dessiner_niveaux()
    elif ecran_actuel == "parametres":
        rect_jouer, rect_param = dessiner_accueil()
        rect_toggle, rect_moins, rect_plus, rect_fermer = dessiner_parametres()

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
                    ret = lancer_niveau_boucle(1)
                    pygame.display.set_caption("Re-Use")
                    ecran_actuel = "accueil"
                    if ret == "quitter":
                        en_cours = False
                elif rects_niveaux[1].collidepoint(mx, my):
                    ret = lancer_niveau_boucle(2)
                    pygame.display.set_caption("Re-Use")
                    ecran_actuel = "accueil"
                    if ret == "quitter":
                        en_cours = False
                elif rects_niveaux[2].collidepoint(mx, my):
                    ret = lancer_niveau_boucle(3)
                    pygame.display.set_caption("Re-Use")
                    ecran_actuel = "accueil"
                    if ret == "quitter":
                        en_cours = False

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
