import pygame
import math
import random
from physics import appliquer_gravite, mettre_a_jour_position, verifier_collision
from physics import calculer_vitesse_lancer, rebond_sol, calculer_distance, GRAVITE


def lancer_niveau1(fenetre, LARGEUR, HAUTEUR):
    pygame.display.set_caption("Re-Use - Niveau 1")

    VERT_F = (45, 90, 39)
    VERT_C = (123, 198, 126)
    BEIGE = (245, 240, 232)
    ORANGE = (232, 137, 43)
    BLANC = (255, 255, 255)
    NOIR = (30, 30, 30)

    BLEU_P = (50, 130, 220)
    JAUNE_P = (230, 190, 50)
    VERT_P = (60, 180, 80)
    MARRON_P = (140, 90, 40)

    police_grande = pygame.font.SysFont("Arial", 42, bold=True)
    police_moyenne = pygame.font.SysFont("Arial", 24)
    police_petite = pygame.font.SysFont("Arial", 16)
    police_btn = pygame.font.SysFont("Arial", 26, bold=True)

    horloge = pygame.time.Clock()

    couleurs_types = {
        "plastique": BLEU_P,
        "papier": JAUNE_P,
        "verre": VERT_P,
        "organique": MARRON_P,
    }

    objets_modeles = [
        {"nom": "Bouteille", "type": "plastique", "taille": 20},
        {"nom": "Canette", "type": "plastique", "taille": 18},
        {"nom": "Journal", "type": "papier", "taille": 22},
        {"nom": "Carton", "type": "papier", "taille": 24},
        {"nom": "Pot verre", "type": "verre", "taille": 20},
        {"nom": "Pomme", "type": "organique", "taille": 18},
        {"nom": "Epluchures", "type": "organique", "taille": 16},
    ]

    SOL_Y = HAUTEUR - 90
    JOUEUR_X = int(LARGEUR * 0.15)
    JOUEUR_Y = SOL_Y - 70

    POUB_W = 80
    POUB_H = 100
    POUB_ESPACE = int((LARGEUR * 0.5) / 4)
    POUB_X_DEBUT = int(LARGEUR * 0.45)
    POUB_Y = SOL_Y - POUB_H

    poubelles = [
        {"type": "plastique", "label": "Plastique", "couleur": BLEU_P, "x": POUB_X_DEBUT},
        {"type": "papier", "label": "Papier", "couleur": JAUNE_P, "x": POUB_X_DEBUT + POUB_ESPACE},
        {"type": "verre", "label": "Verre", "couleur": VERT_P, "x": POUB_X_DEBUT + 2 * POUB_ESPACE},
        {"type": "organique", "label": "Bio", "couleur": MARRON_P, "x": POUB_X_DEBUT + 3 * POUB_ESPACE},
    ]

    TOTAL_OBJETS = 12
    sequence = []
    for i in range(TOTAL_OBJETS):
        choix = random.randint(0, len(objets_modeles) - 1)
        objet = {
            "nom": objets_modeles[choix]["nom"],
            "type": objets_modeles[choix]["type"],
            "taille": objets_modeles[choix]["taille"],
        }
        sequence.append(objet)

    index_objet = 0
    objet_actuel = sequence[0]
    score = 0
    vies = 3
    fin = False
    message_fin = ""

    en_visee = False
    vol_x = 0.0
    vol_y = 0.0
    vol_vx = 0.0
    vol_vy = 0.0
    en_vol = False
    vol_info = None

    feedback_texte = ""
    feedback_couleur = BLANC
    feedback_timer = 0
    rect_btn_fin = pygame.Rect(0, 0, 0, 0)

    def dessiner_coeur(cx, cy, couleur):
        pygame.draw.circle(fenetre, couleur, (cx - 5, cy), 7)
        pygame.draw.circle(fenetre, couleur, (cx + 5, cy), 7)
        pygame.draw.polygon(fenetre, couleur, [(cx - 11, cy + 2), (cx + 11, cy + 2), (cx, cy + 14)])

    def dessiner_fond():
        pygame.draw.rect(fenetre, BEIGE, (0, 0, LARGEUR, SOL_Y))
        pygame.draw.rect(fenetre, VERT_F, (0, SOL_Y, LARGEUR, HAUTEUR - SOL_Y))
        pygame.draw.rect(fenetre, VERT_C, (0, SOL_Y, LARGEUR, 4))

    def dessiner_joueur():
        jx = JOUEUR_X
        jy = JOUEUR_Y
        pygame.draw.rect(fenetre, VERT_F, (jx, jy, 40, 60), border_radius=8)
        pygame.draw.circle(fenetre, (240, 200, 160), (jx + 20, jy - 15), 18)
        pygame.draw.circle(fenetre, NOIR, (jx + 14, jy - 18), 3)
        pygame.draw.circle(fenetre, NOIR, (jx + 26, jy - 18), 3)
        pygame.draw.rect(fenetre, VERT_F, (jx + 5, jy + 60, 12, 18), border_radius=4)
        pygame.draw.rect(fenetre, VERT_F, (jx + 23, jy + 60, 12, 18), border_radius=4)
        if objet_actuel is not None and not en_vol:
            pygame.draw.line(fenetre, (240, 200, 160), (jx + 40, jy + 15), (jx + 70, jy + 5), 6)
        else:
            pygame.draw.rect(fenetre, (240, 200, 160), (jx + 40, jy + 10, 10, 30), border_radius=4)

    def dessiner_objet(info, cx, cy):
        couleur = couleurs_types[info["type"]]
        taille = info["taille"]
        pygame.draw.rect(fenetre, couleur, (cx - taille // 2, cy - taille // 2, taille, taille), border_radius=6)
        pygame.draw.rect(fenetre, NOIR, (cx - taille // 2, cy - taille // 2, taille, taille), 2, border_radius=6)
        texte = police_petite.render(info["nom"], True, NOIR)
        fenetre.blit(texte, (cx - texte.get_width() // 2, cy + taille // 2 + 2))

    def dessiner_poubelle(p):
        x = p["x"]
        y = POUB_Y
        c = p["couleur"]
        pygame.draw.rect(fenetre, (60, 60, 60), (x, y + 10, POUB_W, POUB_H - 10), border_radius=6)
        pygame.draw.rect(fenetre, c, (x, y + 10, POUB_W, 30), border_radius=6)
        pygame.draw.rect(fenetre, c, (x - 4, y, POUB_W + 8, 14), border_radius=4)
        texte = police_petite.render(p["label"], True, BLANC)
        fenetre.blit(texte, (x + POUB_W // 2 - texte.get_width() // 2, y + POUB_H - 22))

    def dessiner_visee(mx, my):
        ox = JOUEUR_X + 70
        oy = JOUEUR_Y + 5
        pygame.draw.line(fenetre, ORANGE, (ox, oy), (mx, my), 2)
        vx_sim, vy_sim, dist_sim = calculer_vitesse_lancer(ox, oy, mx, my)
        if dist_sim < 1:
            return
        sx = float(ox)
        sy = float(oy)
        svx = vx_sim
        svy = vy_sim
        for i in range(40):
            svy = appliquer_gravite(svy)
            sx = sx + svx
            sy = sy + svy
            if sy > SOL_Y:
                break
            rayon = 4 - i // 12
            if rayon < 2:
                rayon = 2
            pygame.draw.circle(fenetre, ORANGE, (int(sx), int(sy)), rayon)

    def dessiner_hud():
        pygame.draw.rect(fenetre, VERT_F, (0, 0, LARGEUR, 48), border_radius=0)
        texte_score = police_moyenne.render("Score : {}".format(score), True, ORANGE)
        fenetre.blit(texte_score, (20, 10))
        for v in range(3):
            if v < vies:
                dessiner_coeur(220 + v * 35, 20, (220, 50, 50))
            else:
                dessiner_coeur(220 + v * 35, 20, (80, 80, 80))
        texte_niv = police_moyenne.render("Niveau 1", True, BLANC)
        fenetre.blit(texte_niv, (LARGEUR // 2 - texte_niv.get_width() // 2, 10))
        restants = TOTAL_OBJETS - index_objet
        texte_rest = police_petite.render("{} objets restants".format(restants), True, VERT_C)
        fenetre.blit(texte_rest, (LARGEUR - texte_rest.get_width() - 20, 16))

    def dessiner_feedback():
        if feedback_timer > 0:
            texte = police_grande.render(feedback_texte, True, feedback_couleur)
            fenetre.blit(texte, (LARGEUR // 2 - texte.get_width() // 2, HAUTEUR // 3))

    def dessiner_ecran_fin():
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(200)
        if message_fin == "Perdu...":
            overlay.fill((100, 20, 20))
        else:
            overlay.fill((0, 0, 0))
        fenetre.blit(overlay, (0, 0))
        t1 = police_grande.render(message_fin, True, ORANGE)
        t2 = police_moyenne.render("Score final : {}".format(score), True, BLANC)
        fenetre.blit(t1, (LARGEUR // 2 - t1.get_width() // 2, HAUTEUR // 2 - 90))
        fenetre.blit(t2, (LARGEUR // 2 - t2.get_width() // 2, HAUTEUR // 2 - 30))
        if message_fin == "Perdu...":
            btn_texte = "Recommencer"
        else:
            btn_texte = "Niveau suivant"
        rect_btn = pygame.Rect(LARGEUR // 2 - 150, HAUTEUR // 2 + 20, 300, 55)
        pygame.draw.rect(fenetre, ORANGE, rect_btn, border_radius=14)
        txt_btn = police_btn.render(btn_texte, True, BLANC)
        fenetre.blit(txt_btn, (LARGEUR // 2 - txt_btn.get_width() // 2, HAUTEUR // 2 + 32))
        rect_menu = pygame.Rect(LARGEUR // 2 - 120, HAUTEUR // 2 + 90, 240, 45)
        pygame.draw.rect(fenetre, VERT_F, rect_menu, border_radius=14)
        txt_menu = police_btn.render("Menu", True, BLANC)
        fenetre.blit(txt_menu, (LARGEUR // 2 - txt_menu.get_width() // 2, HAUTEUR // 2 + 100))
        return rect_btn, rect_menu

    def passer_objet_suivant():
        nouveau_index = index_objet + 1
        if vies <= 0:
            return nouveau_index, None, True, "Perdu..."
        elif nouveau_index >= TOTAL_OBJETS:
            return nouveau_index, None, True, "Niveau termine !"
        else:
            return nouveau_index, sequence[nouveau_index], False, ""

    en_cours_niveau = True

    while en_cours_niveau:

        if en_vol and vol_info is not None:
            vol_vy = appliquer_gravite(vol_vy)
            vol_x = vol_x + vol_vx
            vol_y = vol_y + vol_vy

            if vol_y >= SOL_Y - 10:
                vol_vx, vol_vy, arrete = rebond_sol(vol_vy, vol_vx)
                if arrete:
                    en_vol = False
                    vol_info = None
                    vies = vies - 1
                    feedback_texte = "Rate !"
                    feedback_couleur = (220, 60, 60)
                    feedback_timer = 50
                    index_objet, objet_actuel, fin, message_fin = passer_objet_suivant()
                else:
                    vol_y = float(SOL_Y - 10)

            if en_vol and vol_info is not None:
                for i in range(len(poubelles)):
                    p = poubelles[i]
                    touche = verifier_collision(
                        int(vol_x), int(vol_y),
                        p["x"], POUB_Y, POUB_W, POUB_H
                    )
                    if touche:
                        if vol_info["type"] == p["type"]:
                            score = score + 100
                            feedback_texte = "Bien trie ! +100"
                            feedback_couleur = VERT_C
                        else:
                            vies = vies - 1
                            feedback_texte = "Mauvaise poubelle !"
                            feedback_couleur = (220, 60, 60)
                        feedback_timer = 50
                        en_vol = False
                        vol_info = None
                        index_objet, objet_actuel, fin, message_fin = passer_objet_suivant()
                        break

        if feedback_timer > 0:
            feedback_timer = feedback_timer - 1

        dessiner_fond()
        dessiner_joueur()

        if objet_actuel is not None and not en_vol:
            dessiner_objet(objet_actuel, JOUEUR_X + 70, JOUEUR_Y + 5)

        if en_visee and objet_actuel is not None and not en_vol:
            mx, my = pygame.mouse.get_pos()
            dessiner_visee(mx, my)

        if en_vol and vol_info is not None:
            dessiner_objet(vol_info, int(vol_x), int(vol_y))

        for i in range(len(poubelles)):
            dessiner_poubelle(poubelles[i])

        dessiner_hud()
        dessiner_feedback()

        if fin:
            rect_btn_fin, rect_menu_fin = dessiner_ecran_fin()

        pygame.display.flip()
        horloge.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "quitter", score

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "menu", score

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if fin:
                    if rect_btn_fin.collidepoint(ev.pos[0], ev.pos[1]):
                        if message_fin == "Perdu...":
                            return "recommencer", score
                        else:
                            return "suivant", score
                    if rect_menu_fin.collidepoint(ev.pos[0], ev.pos[1]):
                        return "menu", score

            if not fin:
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if objet_actuel is not None and not en_vol:
                        en_visee = True

                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    if en_visee and objet_actuel is not None and not en_vol:
                        en_visee = False
                        mx = ev.pos[0]
                        my = ev.pos[1]
                        ox = JOUEUR_X + 70
                        oy = JOUEUR_Y + 5
                        vx_lancer, vy_lancer, dist_lancer = calculer_vitesse_lancer(ox, oy, mx, my)
                        if dist_lancer > 5:
                            vol_x = float(ox)
                            vol_y = float(oy)
                            vol_vx = vx_lancer
                            vol_vy = vy_lancer
                            vol_info = objet_actuel
                            en_vol = True
                            objet_actuel = None

    return "menu", score
