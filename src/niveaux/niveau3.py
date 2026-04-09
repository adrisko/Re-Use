import pygame
import random


def lancer_niveau3(fenetre, LARGEUR, HAUTEUR):
    pygame.display.set_caption("Re-Use - Niveau 3")

    VERT_VIF = (72, 240, 100)
    BLANC = (230, 245, 232)
    GRIS = (90, 115, 95)
    NOIR = (5, 10, 6)
    CIEL = (40, 80, 140)
    SOL_COULEUR = (55, 100, 58)

    couleurs_types = {
        "papier": (210, 180, 30),
        "plastique": (30, 90, 180),
        "verre": (30, 150, 60),
        "metal": (150, 150, 160),
    }

    recettes = {
        "papier": "Livre",
        "plastique": "Banc",
        "verre": "Vase",
        "metal": "Velo",
    }

    types_materiaux = ["papier", "plastique", "verre", "metal"]

    police_grande = pygame.font.SysFont("Arial", 42, bold=True)
    police_moyenne = pygame.font.SysFont("Arial", 24)
    police_petite = pygame.font.SysFont("Arial", 16)

    horloge = pygame.time.Clock()

    PLAT_W = 120
    PLAT_H = 20
    PLAT_Y = HAUTEUR - 160
    plat_x = LARGEUR // 2 - PLAT_W // 2

    INV_SLOTS = 3
    INV_Y = HAUTEUR - 100
    INV_SLOT_W = 70
    INV_SLOT_H = 70
    INV_X = LARGEUR // 2 - (INV_SLOTS * INV_SLOT_W + 20) // 2

    inventaire = []
    materiaux_en_chute = []
    objets_recycles = []

    score = 0
    vies = 3
    combinaisons = 0
    OBJECTIF = 3
    vitesse_chute = 3
    timer_apparition = 0
    fin = False
    victoire = False
    message_fin = ""

    feedback_texte = ""
    feedback_couleur = BLANC
    feedback_timer = 0
    flash_timer = 0
    flash_couleur = BLANC

    def faire_tomber_materiau():
        t = random.choice(types_materiaux)
        x = random.randint(60, LARGEUR - 60)
        return {"type": t, "x": float(x), "y": 0.0, "taille": 30}

    def attraper_materiau(m):
        mx = int(m["x"])
        my = int(m["y"])
        mt = m["taille"]
        if my + mt // 2 >= PLAT_Y and my + mt // 2 <= PLAT_Y + PLAT_H + 10:
            if mx + mt // 2 >= plat_x and mx - mt // 2 <= plat_x + PLAT_W:
                return True
        return False

    def verifier_combinaison():
        if len(inventaire) < INV_SLOTS:
            return False, ""
        for i in range(1, len(inventaire)):
            if inventaire[i] != inventaire[0]:
                return False, ""
        return True, recettes[inventaire[0]]

    def dessiner_fond():
        pygame.draw.rect(fenetre, CIEL, (0, 0, LARGEUR, HAUTEUR))
        pygame.draw.rect(fenetre, SOL_COULEUR, (0, HAUTEUR - 90, LARGEUR, 90))
        pygame.draw.line(fenetre, (70, 130, 55), (0, HAUTEUR - 90), (LARGEUR, HAUTEUR - 90), 3)

    def dessiner_plateforme():
        pygame.draw.rect(fenetre, VERT_VIF, (plat_x, PLAT_Y, PLAT_W, PLAT_H), border_radius=6)
        pygame.draw.rect(fenetre, NOIR, (plat_x, PLAT_Y, PLAT_W, PLAT_H), 2, border_radius=6)

    def dessiner_materiau(mat):
        c = couleurs_types[mat["type"]]
        t = mat["taille"]
        cx = int(mat["x"])
        cy = int(mat["y"])
        pygame.draw.rect(fenetre, c, (cx - t // 2, cy - t // 2, t, t), border_radius=6)
        pygame.draw.rect(fenetre, NOIR, (cx - t // 2, cy - t // 2, t, t), 2, border_radius=6)
        txt = police_petite.render(mat["type"], True, BLANC)
        fenetre.blit(txt, (cx - txt.get_width() // 2, cy - t // 2 - 16))

    def dessiner_inventaire():
        txt = police_moyenne.render("Inventaire", True, BLANC)
        fenetre.blit(txt, (LARGEUR // 2 - txt.get_width() // 2, INV_Y - 28))
        for i in range(INV_SLOTS):
            sx = INV_X + i * (INV_SLOT_W + 10)
            pygame.draw.rect(fenetre, (30, 50, 35), (sx, INV_Y, INV_SLOT_W, INV_SLOT_H), border_radius=8)
            pygame.draw.rect(fenetre, GRIS, (sx, INV_Y, INV_SLOT_W, INV_SLOT_H), 2, border_radius=8)
            if i < len(inventaire):
                c = couleurs_types[inventaire[i]]
                pygame.draw.rect(fenetre, c, (sx + 10, INV_Y + 10, INV_SLOT_W - 20, INV_SLOT_H - 20), border_radius=6)
                t = police_petite.render(inventaire[i], True, BLANC)
                fenetre.blit(t, (sx + INV_SLOT_W // 2 - t.get_width() // 2, INV_Y + INV_SLOT_H - 16))

    def dessiner_hud():
        pygame.draw.rect(fenetre, (10, 25, 12), (0, 0, LARGEUR, 48))
        ts = police_moyenne.render("Score : {}".format(score), True, VERT_VIF)
        fenetre.blit(ts, (20, 10))
        for v in range(3):
            if v < vies:
                cv = (200, 50, 70)
            else:
                cv = (50, 50, 50)
            pygame.draw.rect(fenetre, cv, (200 + v * 35, 14, 20, 20), border_radius=4)
        tn = police_moyenne.render("Niveau 3 - L'Atelier", True, BLANC)
        fenetre.blit(tn, (LARGEUR // 2 - tn.get_width() // 2, 10))
        tp = police_petite.render("{} / {} combinaisons".format(combinaisons, OBJECTIF), True, GRIS)
        fenetre.blit(tp, (LARGEUR - tp.get_width() - 20, 16))

    def dessiner_ecran_fin():
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        fenetre.blit(overlay, (0, 0))
        if victoire:
            t1 = police_grande.render("Bravo ! Niveau termine !", True, VERT_VIF)
            fenetre.blit(t1, (LARGEUR // 2 - t1.get_width() // 2, HAUTEUR // 2 - 100))
            texte_objets = ""
            for i in range(len(objets_recycles)):
                if i > 0:
                    texte_objets = texte_objets + ", "
                texte_objets = texte_objets + objets_recycles[i]
            t2 = police_moyenne.render("Objets : " + texte_objets, True, GRIS)
            fenetre.blit(t2, (LARGEUR // 2 - t2.get_width() // 2, HAUTEUR // 2 - 40))
        else:
            t1 = police_grande.render(message_fin, True, VERT_VIF)
            fenetre.blit(t1, (LARGEUR // 2 - t1.get_width() // 2, HAUTEUR // 2 - 100))
        t3 = police_moyenne.render("Score final : {}".format(score), True, BLANC)
        fenetre.blit(t3, (LARGEUR // 2 - t3.get_width() // 2, HAUTEUR // 2 + 10))
        t4 = police_moyenne.render("ESC pour revenir au menu", True, GRIS)
        fenetre.blit(t4, (LARGEUR // 2 - t4.get_width() // 2, HAUTEUR // 2 + 60))

    en_cours_niveau = True

    while en_cours_niveau:

        touches = pygame.key.get_pressed()
        if not fin:
            if touches[pygame.K_LEFT] and plat_x > 0:
                plat_x = plat_x - 8
            if touches[pygame.K_RIGHT] and plat_x < LARGEUR - PLAT_W:
                plat_x = plat_x + 8

            timer_apparition = timer_apparition + 1
            if timer_apparition >= 70 and len(materiaux_en_chute) < 4:
                materiaux_en_chute.append(faire_tomber_materiau())
                timer_apparition = 0

            for i in range(len(materiaux_en_chute)):
                materiaux_en_chute[i]["y"] = materiaux_en_chute[i]["y"] + vitesse_chute

            restants = []
            for i in range(len(materiaux_en_chute)):
                m = materiaux_en_chute[i]
                if attraper_materiau(m):
                    if len(inventaire) >= INV_SLOTS:
                        inventaire.remove(inventaire[0])
                    inventaire.append(m["type"])
                    ok, objet = verifier_combinaison()
                    if ok:
                        while len(inventaire) > 0:
                            inventaire.remove(inventaire[0])
                        score = score + 150
                        combinaisons = combinaisons + 1
                        objets_recycles.append(objet)
                        feedback_texte = "RECYCLE ! {} +150".format(objet)
                        feedback_couleur = VERT_VIF
                        feedback_timer = 60
                        flash_timer = 15
                        flash_couleur = couleurs_types[m["type"]]
                        if combinaisons >= OBJECTIF:
                            fin = True
                            victoire = True
                            message_fin = "Niveau termine !"
                elif m["y"] > HAUTEUR - 90:
                    vies = vies - 1
                    feedback_texte = "Rate !"
                    feedback_couleur = (220, 60, 60)
                    feedback_timer = 40
                    if vies <= 0:
                        fin = True
                        message_fin = "Perdu..."
                else:
                    restants.append(m)
            while len(materiaux_en_chute) > 0:
                materiaux_en_chute.remove(materiaux_en_chute[0])
            for i in range(len(restants)):
                materiaux_en_chute.append(restants[i])

        if feedback_timer > 0:
            feedback_timer = feedback_timer - 1
        if flash_timer > 0:
            flash_timer = flash_timer - 1

        dessiner_fond()
        dessiner_plateforme()
        for i in range(len(materiaux_en_chute)):
            dessiner_materiau(materiaux_en_chute[i])
        dessiner_inventaire()
        dessiner_hud()

        if feedback_timer > 0:
            txt = police_grande.render(feedback_texte, True, feedback_couleur)
            fenetre.blit(txt, (LARGEUR // 2 - txt.get_width() // 2, HAUTEUR // 3))

        if flash_timer > 0:
            ov = pygame.Surface((LARGEUR, HAUTEUR))
            ov.set_alpha(flash_timer * 4)
            ov.fill(flash_couleur)
            fenetre.blit(ov, (0, 0))

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

    return "menu", score
