import pygame
import random


def lancer_niveau3(fenetre, LARGEUR, HAUTEUR):
    pygame.display.set_caption("Re-Use - Niveau 3")

    VERT_F = (45, 90, 39)
    VERT_C = (123, 198, 126)
    BEIGE = (245, 240, 232)
    ORANGE = (232, 137, 43)
    BLANC = (255, 255, 255)
    NOIR = (30, 30, 30)

    couleurs_types = {
        "papier": (230, 190, 50),
        "plastique": (50, 130, 220),
        "verre": (60, 180, 80),
    }

    recettes = {
        "papier": "Livre",
        "plastique": "Banc",
        "verre": "Vase",
    }

    types_materiaux = ["papier", "plastique", "verre"]

    police_grande = pygame.font.SysFont("Arial", 42, bold=True)
    police_moyenne = pygame.font.SysFont("Arial", 24)
    police_petite = pygame.font.SysFont("Arial", 16)
    police_btn = pygame.font.SysFont("Arial", 26, bold=True)

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
    vitesse_chute = 2
    timer_apparition = 0
    fin = False
    victoire = False
    message_fin = ""

    feedback_texte = ""
    feedback_couleur = BLANC
    feedback_timer = 0
    flash_timer = 0
    flash_couleur = BLANC
    rect_btn_fin = pygame.Rect(0, 0, 0, 0)
    rect_menu_fin = pygame.Rect(0, 0, 0, 0)

    def dessiner_coeur(cx, cy, couleur):
        pygame.draw.circle(fenetre, couleur, (cx - 5, cy), 7)
        pygame.draw.circle(fenetre, couleur, (cx + 5, cy), 7)
        pygame.draw.polygon(fenetre, couleur, [(cx - 11, cy + 2), (cx + 11, cy + 2), (cx, cy + 14)])

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
        pygame.draw.rect(fenetre, BEIGE, (0, 0, LARGEUR, HAUTEUR))
        pygame.draw.rect(fenetre, VERT_F, (0, HAUTEUR - 90, LARGEUR, 90))
        pygame.draw.rect(fenetre, VERT_C, (0, HAUTEUR - 90, LARGEUR, 4))

    def dessiner_plateforme():
        pygame.draw.rect(fenetre, ORANGE, (plat_x, PLAT_Y, PLAT_W, PLAT_H), border_radius=6)
        pygame.draw.rect(fenetre, NOIR, (plat_x, PLAT_Y, PLAT_W, PLAT_H), 2, border_radius=6)

    def dessiner_materiau(mat):
        c = couleurs_types[mat["type"]]
        t = mat["taille"]
        cx = int(mat["x"])
        cy = int(mat["y"])
        pygame.draw.rect(fenetre, c, (cx - t // 2, cy - t // 2, t, t), border_radius=6)
        pygame.draw.rect(fenetre, NOIR, (cx - t // 2, cy - t // 2, t, t), 2, border_radius=6)
        txt = police_petite.render(mat["type"], True, NOIR)
        fenetre.blit(txt, (cx - txt.get_width() // 2, cy - t // 2 - 16))

    def dessiner_inventaire():
        txt = police_moyenne.render("Inventaire", True, VERT_F)
        fenetre.blit(txt, (LARGEUR // 2 - txt.get_width() // 2, INV_Y - 28))
        for i in range(INV_SLOTS):
            sx = INV_X + i * (INV_SLOT_W + 10)
            pygame.draw.rect(fenetre, VERT_F, (sx, INV_Y, INV_SLOT_W, INV_SLOT_H), border_radius=8)
            pygame.draw.rect(fenetre, VERT_C, (sx, INV_Y, INV_SLOT_W, INV_SLOT_H), 2, border_radius=8)
            if i < len(inventaire):
                c = couleurs_types[inventaire[i]]
                pygame.draw.rect(fenetre, c, (sx + 8, INV_Y + 8, INV_SLOT_W - 16, INV_SLOT_H - 16), border_radius=6)
                t = police_petite.render(inventaire[i], True, BLANC)
                fenetre.blit(t, (sx + INV_SLOT_W // 2 - t.get_width() // 2, INV_Y + INV_SLOT_H - 16))

    def dessiner_hud():
        pygame.draw.rect(fenetre, VERT_F, (0, 0, LARGEUR, 48))
        ts = police_moyenne.render("Score : {}".format(score), True, ORANGE)
        fenetre.blit(ts, (20, 10))
        for v in range(3):
            if v < vies:
                dessiner_coeur(220 + v * 35, 20, (220, 50, 50))
            else:
                dessiner_coeur(220 + v * 35, 20, (80, 80, 80))
        tn = police_moyenne.render("Niveau 3 - L'Atelier", True, BLANC)
        fenetre.blit(tn, (LARGEUR // 2 - tn.get_width() // 2, 10))
        tp = police_petite.render("{} / {} combinaisons".format(combinaisons, OBJECTIF), True, VERT_C)
        fenetre.blit(tp, (LARGEUR - tp.get_width() - 20, 16))

    def dessiner_ecran_fin():
        overlay = pygame.Surface((LARGEUR, HAUTEUR))
        overlay.set_alpha(200)
        if message_fin == "Perdu...":
            overlay.fill((100, 20, 20))
        else:
            overlay.fill((0, 0, 0))
        fenetre.blit(overlay, (0, 0))
        if victoire:
            t1 = police_grande.render("Bravo ! Jeu termine !", True, ORANGE)
            fenetre.blit(t1, (LARGEUR // 2 - t1.get_width() // 2, HAUTEUR // 2 - 110))
            texte_objets = ""
            for i in range(len(objets_recycles)):
                if i > 0:
                    texte_objets = texte_objets + ", "
                texte_objets = texte_objets + objets_recycles[i]
            t2 = police_moyenne.render("Objets recycles : " + texte_objets, True, VERT_C)
            fenetre.blit(t2, (LARGEUR // 2 - t2.get_width() // 2, HAUTEUR // 2 - 50))
        else:
            t1 = police_grande.render(message_fin, True, ORANGE)
            fenetre.blit(t1, (LARGEUR // 2 - t1.get_width() // 2, HAUTEUR // 2 - 110))
        t3 = police_moyenne.render("Score final : {}".format(score), True, BLANC)
        fenetre.blit(t3, (LARGEUR // 2 - t3.get_width() // 2, HAUTEUR // 2 - 10))
        if message_fin == "Perdu...":
            btn_texte = "Recommencer"
        else:
            btn_texte = "Retour au menu"
        rect_btn = pygame.Rect(LARGEUR // 2 - 150, HAUTEUR // 2 + 40, 300, 55)
        pygame.draw.rect(fenetre, ORANGE, rect_btn, border_radius=14)
        txt_btn = police_btn.render(btn_texte, True, BLANC)
        fenetre.blit(txt_btn, (LARGEUR // 2 - txt_btn.get_width() // 2, HAUTEUR // 2 + 52))
        rect_menu = pygame.Rect(LARGEUR // 2 - 120, HAUTEUR // 2 + 110, 240, 45)
        pygame.draw.rect(fenetre, VERT_F, rect_menu, border_radius=14)
        txt_menu = police_btn.render("Menu", True, BLANC)
        fenetre.blit(txt_menu, (LARGEUR // 2 - txt_menu.get_width() // 2, HAUTEUR // 2 + 120))
        return rect_btn, rect_menu

    en_cours_niveau = True

    while en_cours_niveau:

        touches = pygame.key.get_pressed()
        if not fin:
            if touches[pygame.K_LEFT] and plat_x > 0:
                plat_x = plat_x - 16
            if touches[pygame.K_RIGHT] and plat_x < LARGEUR - PLAT_W:
                plat_x = plat_x + 16

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
                        feedback_couleur = VERT_C
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
                            return "menu", score
                    if rect_menu_fin.collidepoint(ev.pos[0], ev.pos[1]):
                        return "menu", score

    return "menu", score
