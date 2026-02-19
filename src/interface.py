import pygame
from src.niveaux.niveau1 import lancer_niveau1

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
LARGEUR = info.current_w
HAUTEUR = info.current_h
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN)
pygame.display.set_caption("Re-Use")

VERT_BG    = (10,  28,  13)
VERT_CARTE = (18,  50,  22)
VERT_VIF   = (72, 240, 100)
VERT_SOMB  = (35,  80,  42)
BLANC      = (230, 245, 232)
GRIS       = ( 90, 115,  95)
NOIR       = (  5,  10,   6)
GITHUB_BG  = ( 22,  22,  28)

police_titre  = pygame.font.SysFont("Arial", 96)
police_sous   = pygame.font.SysFont("Arial", 22)
police_btn    = pygame.font.SysFont("Arial", 26)
police_petite = pygame.font.SysFont("Arial", 20)
police_url    = pygame.font.SysFont("Arial", 18)

son_active      = True
volume          = 7
meilleur_score  = 0
ecran_actuel    = "accueil"


def arrondi(surface, couleur, rect, rayon):
    pygame.draw.rect(surface, couleur, rect, border_radius=rayon)


def texte_centre(surface, texte, police, couleur, cx, cy):
    rendu = police.render(texte, True, couleur)
    surface.blit(rendu, (cx - rendu.get_width() // 2, cy - rendu.get_height() // 2))


def bouton(surface, texte, cx, cy, larg, haut, fond, col_txt, rayon=16):
    rect = pygame.Rect(cx - larg // 2, cy - haut // 2, larg, haut)
    arrondi(surface, fond, rect, rayon)
    texte_centre(surface, texte, police_btn, col_txt, cx, cy)
    return rect


def bouton_cercle(surface, texte, cx, cy, r, fond, col_txt):
    pygame.draw.circle(surface, fond, (cx, cy), r)
    texte_centre(surface, texte, police_btn, col_txt, cx, cy)
    return pygame.Rect(cx - r, cy - r, r * 2, r * 2)


def dessiner_accueil():
    fenetre.fill(VERT_BG)
    pygame.draw.circle(fenetre, (16, 52, 20), (LARGEUR - 180, 160), 380)
    pygame.draw.circle(fenetre, (12, 38, 15), (130, HAUTEUR - 90), 260)

    re  = police_titre.render("Re",   True, VERT_VIF)
    use = police_titre.render("-Use", True, BLANC)
    total = re.get_width() + use.get_width()
    tx = (LARGEUR - total) // 2
    ty = HAUTEUR // 2 - 220
    fenetre.blit(re,  (tx, ty))
    fenetre.blit(use, (tx + re.get_width(), ty))

    sous = police_sous.render("Trie · Recycle · Sauve la planete ", True, GRIS)
    fenetre.blit(sous, ((LARGEUR - sous.get_width()) // 2, ty + 115))

    pygame.draw.line(fenetre, VERT_SOMB,
                     (LARGEUR // 2 - 180, ty + 165),
                     (LARGEUR // 2 + 180, ty + 165), 1)

    cy_jouer = HAUTEUR // 2 + 10
    rect_jouer = bouton(fenetre, "Jouer",
                        LARGEUR // 2, cy_jouer,
                        340, 72, VERT_VIF, NOIR, rayon=20)

    rect_param = bouton(fenetre, "Paramètres",
                        LARGEUR // 2, cy_jouer + 110,
                        340, 62, VERT_SOMB, BLANC, rayon=16)

    rect_git = bouton(fenetre, "GitHub — Re-Use",
                      LARGEUR // 2, HAUTEUR - 90,
                      360, 52, GITHUB_BG, (170, 170, 185), rayon=14)

    lien = police_url.render("https://github.com/adrisko/Re-Use", True, (55, 90, 60))
    fenetre.blit(lien, ((LARGEUR - lien.get_width()) // 2, HAUTEUR - 58))

    esc = police_url.render("ESC  quitter", True, (45, 65, 50))
    fenetre.blit(esc, (28, HAUTEUR - 34))

    if meilleur_score > 0:
        ms = police_petite.render("  Meilleur score : {}".format(meilleur_score), True, VERT_VIF)
        fenetre.blit(ms, ((LARGEUR - ms.get_width()) // 2, ty + 145))

    return rect_jouer, rect_param, rect_git


def dessiner_niveaux():
    fenetre.fill(VERT_BG)
    pygame.draw.circle(fenetre, (16, 52, 20), (LARGEUR - 160, 200), 320)

    titre = police_titre.render("Niveaux", True, BLANC)
    fenetre.blit(titre, ((LARGEUR - titre.get_width()) // 2, 70))

    sous = police_sous.render("Choisis ta difficulte", True, GRIS)
    fenetre.blit(sous, ((LARGEUR - sous.get_width()) // 2, 188))

    niveaux = [
        ("Niveau 1", "Debutant",       "Trie les plastiques de base",    VERT_VIF,       NOIR),
        ("Niveau 2", "Intermediaire",  "Melanges et matieres difficiles", (255, 200, 60), NOIR),
        ("Niveau 3", "Expert",         "Tout doit etre recycle !",        (255, 90, 90),  BLANC),
    ]

    rects = []
    for i, (nom, diff, desc, coul, tc) in enumerate(niveaux):
        cy = 310 + i * 145
        rect = pygame.Rect(LARGEUR // 2 - 340, cy - 60, 680, 118)
        arrondi(fenetre, VERT_CARTE, rect, 18)
        arrondi(fenetre, coul, pygame.Rect(LARGEUR // 2 - 340, cy - 60, 8, 118), 6)

        t_nom  = police_btn.render(nom,   True, coul)
        t_diff = police_petite.render(diff,  True, GRIS)
        t_desc = police_petite.render(desc,  True, (135, 170, 142))
        fleche = police_btn.render("→",    True, coul)

        fenetre.blit(t_nom,  (LARGEUR // 2 - 310, cy - 28))
        fenetre.blit(t_diff, (LARGEUR // 2 - 310, cy + 14))
        fenetre.blit(t_desc, (LARGEUR // 2,        cy +  8))
        fenetre.blit(fleche, (LARGEUR // 2 + 290,  cy - 14))
        rects.append(rect)

    rect_retour = bouton(fenetre, "← Retour",
                         LARGEUR // 2, HAUTEUR - 80,
                         280, 54, VERT_SOMB, BLANC, rayon=14)

    return rects, rect_retour


def dessiner_parametres():
    overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 210))
    fenetre.blit(overlay, (0, 0))

    cw, ch = 540, 420
    ox = (LARGEUR - cw) // 2
    oy = (HAUTEUR - ch) // 2
    arrondi(fenetre, VERT_CARTE, pygame.Rect(ox, oy, cw, ch), 26)

    t = police_btn.render("Paramètres", True, BLANC)
    fenetre.blit(t, (ox + (cw - t.get_width()) // 2, oy + 28))

    pygame.draw.line(fenetre, VERT_SOMB,
                     (ox + 30, oy + 82), (ox + cw - 30, oy + 82), 1)

    label = police_petite.render("Son", True, BLANC)
    fenetre.blit(label, (ox + 50, oy + 108))

    etat  = "ON"  if son_active else "OFF"
    e_col = VERT_VIF if son_active else (210, 70, 70)
    rect_toggle = bouton(fenetre, etat,
                         ox + cw - 90, oy + 118,
                         100, 40, VERT_SOMB, e_col, rayon=12)

    pygame.draw.line(fenetre, VERT_SOMB,
                     (ox + 30, oy + 168), (ox + cw - 30, oy + 168), 1)

    label_v = police_petite.render("Volume", True, BLANC)
    fenetre.blit(label_v, (ox + 50, oy + 195))

    mid_y = oy + 258

    rect_moins = bouton_cercle(fenetre, "−",
                               ox + 90, mid_y, 30,
                               VERT_SOMB, BLANC)

    vol_str = police_btn.render("{} %".format(volume*10), True, VERT_VIF)
    fenetre.blit(vol_str, (ox + cw // 2 - vol_str.get_width() // 2, mid_y - vol_str.get_height() // 2))

    rect_plus = bouton_cercle(fenetre, "+",
                              ox + cw - 90, mid_y, 30,
                              VERT_SOMB, BLANC)

    bx = ox + 50
    by = oy + 308
    bl = cw - 100
    arrondi(fenetre, VERT_SOMB, pygame.Rect(bx, by, bl, 10), 5)
    if volume > 0:
        arrondi(fenetre, VERT_VIF,
                pygame.Rect(bx, by, int(bl * volume / 10), 10), 5)

    rect_fermer = bouton(fenetre, "✕  Fermer",
                         ox + cw // 2, oy + ch - 44,
                         220, 50, VERT_SOMB, GRIS, rayon=14)

    return rect_toggle, rect_moins, rect_plus, rect_fermer


# ===================== BOUCLE PRINCIPALE =====================
horloge  = pygame.time.Clock()
en_cours = True

while en_cours:

    if ecran_actuel == "accueil":
        rect_jouer, rect_param, rect_git = dessiner_accueil()

    elif ecran_actuel == "niveaux":
        rects_niveaux, rect_retour = dessiner_niveaux()

    elif ecran_actuel == "parametres":
        rect_jouer, rect_param, rect_git = dessiner_accueil()
        rect_toggle, rect_moins, rect_plus, rect_fermer = dessiner_parametres()

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            en_cours = False

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                if ecran_actuel in ("parametres", "niveaux"):
                    ecran_actuel = "accueil"
                else:
                    en_cours = False

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = ev.pos

            if ecran_actuel == "accueil":
                if rect_jouer.collidepoint(mx, my):
                    ecran_actuel = "niveaux"
                elif rect_param.collidepoint(mx, my):
                    ecran_actuel = "parametres"
                elif rect_git.collidepoint(mx, my):
                    webbrowser.open("https://github.com/adrisko/Re-Use")

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
                    print("Niveau 2 - à venir")

                elif rects_niveaux[2].collidepoint(mx, my):
                    print("Niveau 3 - à venir")

            elif ecran_actuel == "parametres":
                if rect_fermer.collidepoint(mx, my):
                    ecran_actuel = "accueil"
                elif rect_toggle.collidepoint(mx, my):
                    son_active = not son_active
                    pygame.mixer.music.set_volume(volume / 10 if son_active else 0)
                elif rect_moins.collidepoint(mx, my):
                    if volume > 0:
                        volume -= 1
                        if son_active:
                            pygame.mixer.music.set_volume(volume / 10)
                elif rect_plus.collidepoint(mx, my):
                    if volume < 10:
                        volume += 1
                        if son_active:
                            pygame.mixer.music.set_volume(volume / 10)

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()