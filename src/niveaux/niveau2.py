import pygame
import random
import math


def lancer_niveau2(fenetre, LARGEUR, HAUTEUR):
    pygame.display.set_caption("Re-Use - Niveau 2")

    VERT_VIF = (72, 240, 100)
    BLANC = (230, 245, 232)
    GRIS = (90, 115, 95)
    NOIR = (5, 10, 6)
    CIEL = (40, 80, 140)
    SOL_COULEUR = (55, 100, 58)
    BLEU_P = (30, 90, 180)
    JAUNE_P = (210, 180, 30)
    VERT_P = (30, 150, 60)
    MARRON_P = (110, 70, 30)
    TAPIS_COULEUR = (80, 80, 80)
    TAPIS_LIGNE = (100, 100, 100)

    police_grande = pygame.font.SysFont("Arial", 42, bold=True)
    police_moyenne = pygame.font.SysFont("Arial", 24)
    police_petite = pygame.font.SysFont("Arial", 16)
    police_touche = pygame.font.SysFont("Arial", 20, bold=True)

    horloge = pygame.time.Clock()

    couleurs_types = {
        "plastique": BLEU_P,
        "papier": JAUNE_P,
        "verre": VERT_P,
        "organique": MARRON_P,
    }

    objets_modeles = [
        {"nom": "Bouteille", "type": "plastique", "taille": 26},
        {"nom": "Canette", "type": "plastique", "taille": 24},
        {"nom": "Sac", "type": "plastique", "taille": 22},
        {"nom": "Journal", "type": "papier", "taille": 28},
        {"nom": "Carton", "type": "papier", "taille": 30},
        {"nom": "Enveloppe", "type": "papier", "taille": 24},
        {"nom": "Pot verre", "type": "verre", "taille": 26},
        {"nom": "Bocal", "type": "verre", "taille": 28},
        {"nom": "Pomme", "type": "organique", "taille": 24},
        {"nom": "Epluchures", "type": "organique", "taille": 22},
    ]

    TAPIS_Y = HAUTEUR - 180
    TAPIS_H = 60
    TAPIS_X_DEBUT = 100
    TAPIS_X_FIN = LARGEUR - 100

    POUB_W = 80
    POUB_H = 90
    POUB_Y = 80
    poubelles = [
        {"type": "verre", "label": "Verre", "couleur": VERT_P, "touche": "gauche"},
        {"type": "plastique", "label": "Plastique", "couleur": BLEU_P, "touche": "haut"},
        {"type": "papier", "label": "Papier", "couleur": JAUNE_P, "touche": "bas"},
        {"type": "organique", "label": "Bio", "couleur": MARRON_P, "touche": "droite"},
    ]
    espacement = LARGEUR // (len(poubelles) + 1)
    for i in range(len(poubelles)):
        poubelles[i]["x"] = espacement * (i + 1) - POUB_W // 2

    symboles_touches = {
        "gauche": "<",
        "haut": "^",
        "bas": "v",
        "droite": ">",
    }

    score = 0
    vies = 3
    vitesse_tapis = 2
    objets_tries = 0
    OBJECTIF = 10
    fin = False
    message_fin = ""

    dechets_sur_tapis = []
    timer_apparition = 0
    DELAI_APPARITION = 90
    anim_envoi = []

    feedback_texte = ""
    feedback_couleur = BLANC
    feedback_timer = 0
    tapis_offset = 0

    def creer_dechet():
        modele = random.choice(objets_modeles)
        dechet = {
            "nom": modele["nom"],
            "type": modele["type"],
            "taille": modele["taille"],
            "x": float(TAPIS_X_FIN - 40),
            "y": float(TAPIS_Y + TAPIS_H // 2),
        }
        return dechet

    def deplacer_tapis():
        for i in range(len(dechets_sur_tapis)):
            dechets_sur_tapis[i]["x"] = dechets_sur_tapis[i]["x"] - vitesse_tapis

    def verifier_tri(dechet, type_poubelle):
        if dechet["type"] == type_poubelle:
            return True
        return False

    def dessiner_fond():
        pygame.draw.rect(fenetre, CIEL, (0, 0, LARGEUR, HAUTEUR))
        pygame.draw.rect(fenetre, SOL_COULEUR, (0, HAUTEUR - 90, LARGEUR, 90))
        pygame.draw.line(fenetre, (70, 130, 55), (0, HAUTEUR - 90), (LARGEUR, HAUTEUR - 90), 3)

    def dessiner_tapis():
        pygame.draw.rect(fenetre, TAPIS_COULEUR, (TAPIS_X_DEBUT, TAPIS_Y, TAPIS_X_FIN - TAPIS_X_DEBUT, TAPIS_H), border_radius=8)
        pas = 30
        debut = TAPIS_X_DEBUT + 10 - (tapis_offset % pas)
        x = debut
        while x < TAPIS_X_FIN - 10:
            pygame.draw.line(fenetre, TAPIS_LIGNE, (int(x), TAPIS_Y + 10), (int(x), TAPIS_Y + TAPIS_H - 10), 2)
            x = x + pas
        pygame.draw.rect(fenetre, GRIS, (TAPIS_X_DEBUT, TAPIS_Y, TAPIS_X_FIN - TAPIS_X_DEBUT, TAPIS_H), 3, border_radius=8)
        pygame.draw.circle(fenetre, GRIS, (TAPIS_X_DEBUT, TAPIS_Y + TAPIS_H // 2), 15)
        pygame.draw.circle(fenetre, GRIS, (TAPIS_X_FIN, TAPIS_Y + TAPIS_H // 2), 15)

    def dessiner_dechet(dechet):
        couleur = couleurs_types[dechet["type"]]
        taille = dechet["taille"]
        cx = int(dechet["x"])
        cy = int(dechet["y"])
        pygame.draw.rect(fenetre, couleur, (cx - taille // 2, cy - taille // 2, taille, taille), border_radius=6)
        pygame.draw.rect(fenetre, NOIR, (cx - taille // 2, cy - taille // 2, taille, taille), 2, border_radius=6)
        texte = police_petite.render(dechet["nom"], True, BLANC)
        fenetre.blit(texte, (cx - texte.get_width() // 2, cy - taille // 2 - 18))

    def dessiner_poubelle(p):
        x = p["x"]
        y = POUB_Y
        c = p["couleur"]
        pygame.draw.rect(fenetre, (50, 50, 50), (x, y + 10, POUB_W, POUB_H - 10), border_radius=6)
        pygame.draw.rect(fenetre, c, (x, y + 10, POUB_W, 25), border_radius=6)
        pygame.draw.rect(fenetre, c, (x - 4, y, POUB_W + 8, 14), border_radius=4)
        texte = police_petite.render(p["label"], True, BLANC)
        fenetre.blit(texte, (x + POUB_W // 2 - texte.get_width() // 2, y + POUB_H - 18))
        symbole = symboles_touches[p["touche"]]
        touche_texte = police_touche.render(symbole, True, c)
        pygame.draw.rect(fenetre, NOIR, (x + POUB_W // 2 - 16, y + POUB_H + 6, 32, 28), border_radius=6)
        pygame.draw.rect(fenetre, GRIS, (x + POUB_W // 2 - 16, y + POUB_H + 6, 32, 28), 2, border_radius=6)
        fenetre.blit(touche_texte, (x + POUB_W // 2 - touche_texte.get_width() // 2, y + POUB_H + 8))

    def dessiner_animations():
        for i in range(len(anim_envoi)):
            a = anim_envoi[i]
            couleur = couleurs_types[a["type"]]
            taille = a["taille"]
            cx = int(a["x"])
            cy = int(a["y"])
            pygame.draw.rect(fenetre, couleur, (cx - taille // 2, cy - taille // 2, taille, taille), border_radius=6)

    def dessiner_hud():
        pygame.draw.rect(fenetre, (10, 25, 12), (0, 0, LARGEUR, 48))
        texte_score = police_moyenne.render("Score : {}".format(score), True, VERT_VIF)
        fenetre.blit(texte_score, (20, 10))
        for v in range(3):
            if v < vies:
                couleur_vie = (200, 50, 70)
            else:
                couleur_vie = (50, 50, 50)
            pygame.draw.rect(fenetre, couleur_vie, (200 + v * 35, 14, 20, 20), border_radius=4)
        texte_niv = police_moyenne.render("Niveau 2 - Le Convoyeur", True, BLANC)
        fenetre.blit(texte_niv, (LARGEUR // 2 - texte_niv.get_width() // 2, 10))
        texte_prog = police_petite.render("{} / {} tries".format(objets_tries, OBJECTIF), True, GRIS)
        fenetre.blit(texte_prog, (LARGEUR - texte_prog.get_width() - 20, 16))
        texte_vit = police_petite.render("Vitesse : {}".format(vitesse_tapis), True, GRIS)
        fenetre.blit(texte_vit, (LARGEUR - texte_vit.get_width() // 2 - 20, 32))

    def dessiner_feedback():
        if feedback_timer > 0:
            texte = police_grande.render(feedback_texte, True, feedback_couleur)
            fenetre.blit(texte, (LARGEUR // 2 - texte.get_width() // 2, HAUTEUR // 3))

    def dessiner_ecran_fin():
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))
        fenetre.blit(overlay, (0, 0))
        t1 = police_grande.render(message_fin, True, VERT_VIF)
        t2 = police_moyenne.render("Score final : {}".format(score), True, BLANC)
        t3 = police_moyenne.render("ESC pour revenir au menu", True, GRIS)
        fenetre.blit(t1, (LARGEUR // 2 - t1.get_width() // 2, HAUTEUR // 2 - 70))
        fenetre.blit(t2, (LARGEUR // 2 - t2.get_width() // 2, HAUTEUR // 2))
        fenetre.blit(t3, (LARGEUR // 2 - t3.get_width() // 2, HAUTEUR // 2 + 50))

    def dessiner_instructions():
        texte = police_petite.render("Fleches pour trier : < Verre   ^ Plastique   v Papier   > Bio", True, GRIS)
        fenetre.blit(texte, (LARGEUR // 2 - texte.get_width() // 2, TAPIS_Y + TAPIS_H + 20))

    en_cours_niveau = True

    while en_cours_niveau:

        if not fin:
            tapis_offset = tapis_offset + vitesse_tapis

            timer_apparition = timer_apparition + 1
            if timer_apparition >= DELAI_APPARITION and len(dechets_sur_tapis) < 3:
                nouveau = creer_dechet()
                dechets_sur_tapis.append(nouveau)
                timer_apparition = 0

            deplacer_tapis()

            dechets_restants = []
            for i in range(len(dechets_sur_tapis)):
                if dechets_sur_tapis[i]["x"] < TAPIS_X_DEBUT - 20:
                    vies = vies - 1
                    feedback_texte = "Perdu ! Dechet non trie"
                    feedback_couleur = (220, 60, 60)
                    feedback_timer = 50
                    if vies <= 0:
                        fin = True
                        message_fin = "Perdu..."
                else:
                    dechets_restants.append(dechets_sur_tapis[i])
            while len(dechets_sur_tapis) > 0:
                dechets_sur_tapis.remove(dechets_sur_tapis[0])
            for i in range(len(dechets_restants)):
                dechets_sur_tapis.append(dechets_restants[i])

        anims_restantes = []
        for i in range(len(anim_envoi)):
            a = anim_envoi[i]
            dx = a["cible_x"] - a["x"]
            dy = a["cible_y"] - a["y"]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 5:
                a["x"] = a["x"] + (dx / dist) * 12
                a["y"] = a["y"] + (dy / dist) * 12
                anims_restantes.append(a)
        while len(anim_envoi) > 0:
            anim_envoi.remove(anim_envoi[0])
        for i in range(len(anims_restantes)):
            anim_envoi.append(anims_restantes[i])

        if feedback_timer > 0:
            feedback_timer = feedback_timer - 1

        dessiner_fond()
        dessiner_tapis()

        for i in range(len(poubelles)):
            dessiner_poubelle(poubelles[i])

        for i in range(len(dechets_sur_tapis)):
            dessiner_dechet(dechets_sur_tapis[i])

        dessiner_animations()
        dessiner_hud()
        dessiner_feedback()
        dessiner_instructions()

        if fin:
            dessiner_ecran_fin()

        pygame.display.flip()
        horloge.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "quitter", score

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "menu", score

                if not fin and len(dechets_sur_tapis) > 0:
                    touche_pressee = ""
                    if ev.key == pygame.K_LEFT:
                        touche_pressee = "gauche"
                    elif ev.key == pygame.K_UP:
                        touche_pressee = "haut"
                    elif ev.key == pygame.K_DOWN:
                        touche_pressee = "bas"
                    elif ev.key == pygame.K_RIGHT:
                        touche_pressee = "droite"

                    if touche_pressee != "":
                        type_poubelle = ""
                        cible_x = 0
                        cible_y = 0
                        for i in range(len(poubelles)):
                            if poubelles[i]["touche"] == touche_pressee:
                                type_poubelle = poubelles[i]["type"]
                                cible_x = poubelles[i]["x"] + POUB_W // 2
                                cible_y = POUB_Y + POUB_H // 2
                                break

                        premier = dechets_sur_tapis[0]

                        anim = {
                            "x": premier["x"],
                            "y": premier["y"],
                            "type": premier["type"],
                            "taille": premier["taille"],
                            "cible_x": cible_x,
                            "cible_y": cible_y,
                        }
                        anim_envoi.append(anim)

                        if verifier_tri(premier, type_poubelle):
                            score = score + 100
                            objets_tries = objets_tries + 1
                            feedback_texte = "Bien trie ! +100"
                            feedback_couleur = VERT_VIF
                            feedback_timer = 40

                            if objets_tries % 5 == 0 and objets_tries > 0:
                                vitesse_tapis = vitesse_tapis + 1
                                feedback_texte = "Vitesse augmentee !"

                            if objets_tries >= OBJECTIF:
                                fin = True
                                message_fin = "Niveau termine !"
                        else:
                            vies = vies - 1
                            feedback_texte = "Mauvaise poubelle !"
                            feedback_couleur = (220, 60, 60)
                            feedback_timer = 40
                            if vies <= 0:
                                fin = True
                                message_fin = "Perdu..."

                        dechets_sur_tapis.remove(premier)

    return "menu", score
