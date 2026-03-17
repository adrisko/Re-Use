import pygame
import math
import random
from src.physics import appliquer_gravite, mettre_a_jour_position, verifier_collision, GRAVITE

def lancer_niveau1(fenetre, LARGEUR, HAUTEUR):
    pygame.display.set_caption("Re-Use - Niveau 1")

    # ===================== COULEURS =====================
    VERT_VIF   = (72,  240, 100)
    VERT_SOMB  = (35,   80,  42)
    BLANC      = (230, 245, 232)
    GRIS       = (90,  115,  95)
    NOIR       = (5,    10,   6)
    CIEL_HAUT  = (25,   55, 110)
    CIEL_BAS   = (55,  100, 160)
    SOL_COL    = (55,  100,  58)
    SOL_BORD   = (35,   70,  38)
    TAPIS_COL  = (60,   60,  60)
    TAPIS_BAND = (85,   85,  85)
    ROULEAU    = (100, 100, 100)

    BLEU_P     = (30,   90, 180)
    JAUNE_P    = (210, 180,  30)
    VERT_P     = (30,  150,  60)
    MARRON_P   = (110,  70,  30)

    BLEU_CORPS   = (20,  65, 130)
    JAUNE_CORPS  = (160, 135,  20)
    VERT_CORPS   = (20,  110,  40)
    MARRON_CORPS = (80,   50,  20)

    font_big   = pygame.font.SysFont("Arial", 48, bold=True)
    font_med   = pygame.font.SysFont("Arial", 26)
    font_small = pygame.font.SysFont("Arial", 18)
    font_tiny  = pygame.font.SysFont("Arial", 13)
    font_icon  = pygame.font.SysFont("Segoe UI Emoji", 22)

    horloge = pygame.time.Clock()

    TYPES_COULEUR = {
        "plastique": BLEU_P,
        "papier":    JAUNE_P,
        "verre":     VERT_P,
        "organique": MARRON_P,
    }

    OBJETS_MODELES = [
        {"nom": "Bouteille",  "type": "plastique", "forme": "bouteille", "w": 20, "h": 44},
        {"nom": "Canette",    "type": "plastique", "forme": "canette",   "w": 22, "h": 36},
        {"nom": "Journal",    "type": "papier",    "forme": "journal",   "w": 38, "h": 28},
        {"nom": "Carton",     "type": "papier",    "forme": "carton",    "w": 42, "h": 32},
        {"nom": "Pot verre",  "type": "verre",     "forme": "pot",       "w": 26, "h": 34},
        {"nom": "Pomme",      "type": "organique", "forme": "pomme",     "w": 30, "h": 32},
        {"nom": "Epluchures", "type": "organique", "forme": "rect",      "w": 34, "h": 18},
    ]

    SOL_Y    = HAUTEUR - 100
    JOUEUR_X = int(LARGEUR * 0.18)
    JOUEUR_Y = SOL_Y - 90
    JOUEUR_W = 52
    JOUEUR_H = 80

    TAPIS_X  = int(LARGEUR * 0.02)
    TAPIS_Y  = SOL_Y - 32
    TAPIS_W  = int(LARGEUR * 0.13)
    TAPIS_H  = 24

    POUB_W   = int(LARGEUR * 0.075)
    POUB_H   = int(HAUTEUR * 0.18)
    POUB_GAP = int((LARGEUR * 0.52) / 4)
    POUB_X0  = int(LARGEUR * 0.44)
    POUB_Y   = SOL_Y - POUB_H

    configs = [
        ("plastique", "Plastique", BLEU_P,   BLEU_CORPS,   "♻"),
        ("papier",    "Papier",    JAUNE_P,  JAUNE_CORPS,  "📄"),
        ("verre",     "Verre",     VERT_P,   VERT_CORPS,   "🍾"),
        ("organique", "Bio",       MARRON_P, MARRON_CORPS, "🍃"),
    ]
    poubelles = []
    for i, (typ, lbl, coul, corps, ic) in enumerate(configs):
        poubelles.append({
            "type": typ, "x": POUB_X0 + i*POUB_GAP, "y": POUB_Y,
            "w": POUB_W, "h": POUB_H,
            "label": lbl, "couleur": coul, "corps": corps,
            "icone": ic, "shake": 0,
        })

    # on genere 12 objets aleatoires pour la partie
    TOTAL_OBJETS = 12
    sequence = [random.choice(OBJETS_MODELES).copy() for _ in range(TOTAL_OBJETS)]
    idx = 0

    SLOT_W = TAPIS_W // 4
    tapis_offset = 0.0
    TAPIS_VITESSE = 0.9

    def construire_slots():
        s = []
        for k in range(min(4, TOTAL_OBJETS - idx)):
            s.append({"info": sequence[idx + k].copy(), "rel": float(k * SLOT_W + SLOT_W//2)})
        return s

    tapis_slots  = construire_slots()
    objet_joueur = None
    vol          = None
    vise         = False
    score        = 0
    vies         = 3
    fin          = False
    msg_fin      = ""
    feedback     = {"texte": "", "couleur": BLANC, "timer": 0}
    particules   = []

    def prendre_premier():
        nonlocal objet_joueur
        if tapis_slots:
            objet_joueur = tapis_slots[0]["info"]

    prendre_premier()

    # --- DESSIN OBJET ---
    def dessiner_objet(surface, info, cx, cy):
        c  = TYPES_COULEUR[info["type"]]
        cl = tuple(min(255, v+60) for v in c)
        sd = tuple(max(0,   v-60) for v in c)
        w, h, forme = info["w"], info["h"], info["forme"]

        if forme == "bouteille":
            pygame.draw.rect(surface, c,  (cx-w//2+4, cy-h//2+h//3, w-8, h*2//3), border_radius=4)
            pygame.draw.rect(surface, cl, (cx-w//4,   cy-h//2,      w//2, h//3+2), border_radius=3)
            pygame.draw.rect(surface, sd, (cx-w//4+2, cy-h//2-6,    w//2-4, 8),   border_radius=3)
            pygame.draw.rect(surface, cl, (cx-w//2+6, cy-h//2+h//3+4, 4, h//3),  border_radius=2)
            pygame.draw.rect(surface, NOIR,(cx-w//2+4, cy-h//2+h//3, w-8, h*2//3), 2, border_radius=4)
        elif forme == "canette":
            pygame.draw.rect(surface, c,  (cx-w//2, cy-h//2+6, w, h-12), border_radius=5)
            pygame.draw.ellipse(surface, sd,(cx-w//2, cy-h//2,    w, 14))
            pygame.draw.ellipse(surface, sd,(cx-w//2, cy+h//2-14, w, 14))
            pygame.draw.rect(surface, cl, (cx-w//2+4, cy-h//2+10, 5, h-22), border_radius=2)
            pygame.draw.rect(surface, NOIR,(cx-w//2, cy-h//2+6, w, h-12), 2, border_radius=5)
        elif forme == "journal":
            pygame.draw.rect(surface, c,  (cx-w//2, cy-h//2, w, h), border_radius=3)
            for dy in [4, 12, 20]:
                pygame.draw.rect(surface, cl, (cx-w//2+4, cy-h//2+dy, w-8 if dy<15 else w//2, 3))
            pygame.draw.rect(surface, NOIR,(cx-w//2, cy-h//2, w, h), 2, border_radius=3)
        elif forme == "carton":
            pygame.draw.rect(surface, c,  (cx-w//2, cy-h//2, w, h), border_radius=4)
            pygame.draw.line(surface, sd, (cx, cy-h//2), (cx, cy+h//2), 2)
            pygame.draw.line(surface, sd, (cx-w//2, cy), (cx+w//2, cy), 2)
            pygame.draw.rect(surface, NOIR,(cx-w//2, cy-h//2, w, h), 2, border_radius=4)
        elif forme == "pot":
            pygame.draw.ellipse(surface, c,  (cx-w//2, cy-h//2, w, h))
            pygame.draw.ellipse(surface, cl, (cx-w//2+4, cy-h//2+4, w//2, h//3))
            pygame.draw.rect(surface, sd,   (cx-w//4, cy-h//2-6, w//2, 8), border_radius=3)
            pygame.draw.ellipse(surface, NOIR,(cx-w//2, cy-h//2, w, h), 2)
        elif forme == "pomme":
            pygame.draw.ellipse(surface, c,  (cx-w//2, cy-h//2+4, w, h-4))
            pygame.draw.ellipse(surface, cl, (cx-w//2+6, cy-h//2+8, w//3, h//4))
            pygame.draw.line(surface, sd,   (cx, cy-h//2+4), (cx+4, cy-h//2-4), 3)
            pygame.draw.ellipse(surface, NOIR,(cx-w//2, cy-h//2+4, w, h-4), 2)
        else:
            pygame.draw.rect(surface, c,  (cx-w//2, cy-h//2, w, h), border_radius=5)
            pygame.draw.rect(surface, NOIR,(cx-w//2, cy-h//2, w, h), 2, border_radius=5)

        lbl = font_tiny.render(info["nom"], True, BLANC)
        surface.blit(lbl, (cx - lbl.get_width()//2, cy + h//2 + 3))

    # --- DESSIN POUBELLE ---
    def dessiner_poubelle(p):
        x, y, w, h = p["x"], p["y"], p["w"], p["h"]
        c  = p["couleur"]
        co = p["corps"]
        cl = tuple(min(255, v+50) for v in c)

        # c'est pour le shake quand on touche la poubelle
        sx = 0
        if p["shake"] > 0:
            sx = int(math.sin(p["shake"] * 1.4) * 5)
            p["shake"] -= 1
        x += sx

        # Ombre
        pygame.draw.ellipse(fenetre, (20, 40, 20), (x+8, SOL_Y-6, w-10, 12))

        # Corps trapeze
        pts = [(x+6, y+h), (x+w-6, y+h), (x+w-2, y+10), (x+2, y+10)]
        pygame.draw.polygon(fenetre, co,   pts)
        pygame.draw.polygon(fenetre, NOIR, pts, 2)

        # Bande coloree
        pygame.draw.rect(fenetre, c,  (x+2, y+10, w-4, h//3), border_radius=3)
        # Reflet
        pygame.draw.line(fenetre, cl, (x+10, y+14), (x+10, y+14+h//3-8), 4)

        # Couvercle
        couv = [(x-4, y+10), (x+w+4, y+10), (x+w, y), (x, y)]
        pygame.draw.polygon(fenetre, c,    couv)
        pygame.draw.polygon(fenetre, NOIR, couv, 2)

        # Poignee
        pygame.draw.rect(fenetre, co,   (x+w//2-10, y-10, 20, 12), border_radius=4)
        pygame.draw.rect(fenetre, NOIR, (x+w//2-10, y-10, 20, 12), 2, border_radius=4)

        # Roues
        for rx in [x+14, x+w-14]:
            pygame.draw.circle(fenetre, (40,40,40), (rx, SOL_Y-2), 8)
            pygame.draw.circle(fenetre, (70,70,70), (rx, SOL_Y-2), 4)

        # Icone
        ic = font_icon.render(p["icone"], True, BLANC)
        fenetre.blit(ic, (x+w//2-ic.get_width()//2, y+14))

        # Label
        lbl = font_tiny.render(p["label"], True, BLANC)
        fenetre.blit(lbl, (x+w//2-lbl.get_width()//2, y+h-20))

    # --- DESSIN TAPIS ---
    def dessiner_tapis():
        # Support
        pygame.draw.rect(fenetre, (40,40,40), (TAPIS_X-8, TAPIS_Y+TAPIS_H, TAPIS_W+16, 18), border_radius=4)
        for px in [TAPIS_X+14, TAPIS_X+TAPIS_W-14]:
            pygame.draw.rect(fenetre, (50,50,50), (px-5, TAPIS_Y+TAPIS_H+14, 10, 20), border_radius=3)
        # Bande
        pygame.draw.rect(fenetre, TAPIS_COL, (TAPIS_X, TAPIS_Y, TAPIS_W, TAPIS_H), border_radius=6)
        # Lignes animees
        nb = 12
        pas = TAPIS_W // nb
        for b in range(nb+2):
            bx = int(TAPIS_X + (b*pas - tapis_offset) % TAPIS_W)
            if TAPIS_X <= bx <= TAPIS_X+TAPIS_W:
                pygame.draw.line(fenetre, TAPIS_BAND, (bx, TAPIS_Y+3), (bx, TAPIS_Y+TAPIS_H-3), 3)
        pygame.draw.rect(fenetre, (30,30,30), (TAPIS_X, TAPIS_Y, TAPIS_W, TAPIS_H), 2, border_radius=6)
        # Rouleaux
        for rx in [TAPIS_X+10, TAPIS_X+TAPIS_W-10]:
            pygame.draw.circle(fenetre, ROULEAU,   (rx, TAPIS_Y+TAPIS_H//2), 13)
            pygame.draw.circle(fenetre, (60,60,60),(rx, TAPIS_Y+TAPIS_H//2), 7)
            pygame.draw.circle(fenetre, NOIR,      (rx, TAPIS_Y+TAPIS_H//2), 13, 2)
        # Fleche direction
        ax = TAPIS_X + TAPIS_W//2
        ay = TAPIS_Y - 16
        pygame.draw.polygon(fenetre, VERT_VIF, [(ax-14, ay-7), (ax+10, ay), (ax-14, ay+7)])

    # --- DESSIN JOUEUR ---
    def dessiner_joueur(a_objet):
        jx, jy = JOUEUR_X, JOUEUR_Y
        pygame.draw.ellipse(fenetre, (30,60,30), (jx+4, SOL_Y-6, JOUEUR_W, 10))
        pygame.draw.rect(fenetre, (40,55,160), (jx+8,  jy+JOUEUR_H-10, 14, 20), border_radius=4)
        pygame.draw.rect(fenetre, (40,55,160), (jx+28, jy+JOUEUR_H-10, 14, 20), border_radius=4)
        pygame.draw.ellipse(fenetre, NOIR, (jx+4,  jy+JOUEUR_H+8, 20, 10))
        pygame.draw.ellipse(fenetre, NOIR, (jx+24, jy+JOUEUR_H+8, 20, 10))
        pygame.draw.rect(fenetre, (60,80,200), (jx, jy, JOUEUR_W, JOUEUR_H), border_radius=10)
        pygame.draw.rect(fenetre, (80,100,220), (jx+4, jy+8, 20, JOUEUR_H-16), border_radius=6)
        pygame.draw.rect(fenetre, (255,190,140), (jx-10, jy+10, 12, 36), border_radius=5)
        if a_objet:
            pygame.draw.line(fenetre, (255,190,140), (jx+JOUEUR_W, jy+20), (jx+JOUEUR_W+30, jy+5), 9)
        else:
            pygame.draw.rect(fenetre, (255,190,140), (jx+JOUEUR_W, jy+10, 12, 36), border_radius=5)
        pygame.draw.ellipse(fenetre, (255,200,150), (jx+8, jy-34, 36, 36))
        pygame.draw.rect(fenetre, VERT_VIF, (jx+7, jy-36, 38, 10), border_radius=5)
        pygame.draw.circle(fenetre, NOIR, (jx+20, jy-20), 5)
        pygame.draw.circle(fenetre, NOIR, (jx+34, jy-20), 5)
        pygame.draw.circle(fenetre, BLANC, (jx+22, jy-22), 2)
        pygame.draw.circle(fenetre, BLANC, (jx+36, jy-22), 2)
        pygame.draw.arc(fenetre, NOIR, pygame.Rect(jx+18, jy-16, 16, 10), math.pi, 2*math.pi, 2)

    # --- FOND ---
    # on dessine le ciel avec un dégradé ligne par ligne
    def dessiner_fond():
        for ly in range(SOL_Y):
            t = ly / SOL_Y
            r = int(CIEL_HAUT[0] + (CIEL_BAS[0]-CIEL_HAUT[0])*t)
            g = int(CIEL_HAUT[1] + (CIEL_BAS[1]-CIEL_HAUT[1])*t)
            b = int(CIEL_HAUT[2] + (CIEL_BAS[2]-CIEL_HAUT[2])*t)
            pygame.draw.line(fenetre, (r,g,b), (0,ly), (LARGEUR,ly))
        for cx, cy, r in [(200,80,45),(500,60,35),(900,100,50),(1300,70,40)]:
            if cx < LARGEUR:
                pygame.draw.ellipse(fenetre, (200,215,235), (cx-r, cy-r//2, r*2, r))
                pygame.draw.ellipse(fenetre, (200,215,235), (cx-r//2, cy-r, r, r))
        pygame.draw.rect(fenetre, SOL_COL,  (0, SOL_Y, LARGEUR, HAUTEUR-SOL_Y))
        pygame.draw.rect(fenetre, SOL_BORD, (0, SOL_Y, LARGEUR, 8))
        for gx in range(0, LARGEUR, 18):
            pygame.draw.line(fenetre, (70,130,55), (gx, SOL_Y), (gx+4, SOL_Y-10), 2)

    # --- VISEE ---
    def dessiner_vise(mx, my):
        if not vise or objet_joueur is None:
            return
        ox = JOUEUR_X + JOUEUR_W + 30
        oy = JOUEUR_Y + 5
        dx = mx - ox
        dy = my - oy
        dist = math.hypot(dx, dy)
        if dist < 1:
            return
        puissance = min(dist / 6, 26)
        vx = (dx/dist) * puissance
        vy = (dy/dist) * puissance
        sx, sy, svx, svy = float(ox), float(oy), vx, vy
        for i in range(55):
            svy = appliquer_gravite(svy, GRAVITE)
            sx, sy = mettre_a_jour_position(sx, sy, svx, svy)
            if sy > SOL_Y:
                break
            rayon = max(2, 5 - i//10)
            pygame.draw.circle(fenetre, (255,240,80), (int(sx), int(sy)), rayon)
        pygame.draw.line(fenetre, (200,200,50), (ox,oy), (mx,my), 2)
        pct = min(dist / (6*26), 1.0)
        col = (int(50+200*pct), int(220-180*pct), 50)
        pygame.draw.rect(fenetre, (30,30,30), (ox-40, oy-30, 80, 12), border_radius=5)
        pygame.draw.rect(fenetre, col,        (ox-40, oy-30, int(80*pct), 12), border_radius=5)
        t = font_tiny.render("Puissance", True, BLANC)
        fenetre.blit(t, (ox - t.get_width()//2, oy-46))

    # --- PARTICULES ---
    # on limite a 20 particules par explosion pour pas trop charger
    def ajouter_particules(px, py, coul, ok):
        for _ in range(20):
            angle  = random.uniform(0, 2*math.pi)
            vit    = random.uniform(2, 8)
            particules.append({
                "x": float(px), "y": float(py),
                "vx": math.cos(angle)*vit,
                "vy": math.sin(angle)*vit - 3,
                "vie": 45, "r": random.randint(3,7),
                "couleur": coul if ok else (220,60,60),
            })

    def maj_particules():
        for p in particules[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.3
            p["vie"] -= 1
            if p["vie"] <= 0:
                particules.remove(p)

    def dessiner_particules():
        for p in particules:
            pygame.draw.circle(fenetre, p["couleur"], (int(p["x"]), int(p["y"])), p["r"])

    # --- HUD ---
    def dessiner_hud():
        pygame.draw.rect(fenetre, (10,25,12), (0,0,LARGEUR,52))
        pygame.draw.line(fenetre, VERT_SOMB, (0,52), (LARGEUR,52), 2)
        t = font_med.render("Score : {}".format(score), True, VERT_VIF)
        fenetre.blit(t, (20,12))
        for v in range(3):
            col = (200,50,70) if v < vies else (50,50,50)
            hx  = 220 + v*38
            pygame.draw.polygon(fenetre, col, [(hx+14,10),(hx,20),(hx+14,36),(hx+28,20)])
        tn = font_med.render("Niveau 1", True, BLANC)
        fenetre.blit(tn, (LARGEUR//2 - tn.get_width()//2, 12))
        re = font_small.render(f"{TOTAL_OBJETS - idx} objets restants", True, GRIS)
        fenetre.blit(re, (LARGEUR - re.get_width() - 20, 16))
        esc = font_tiny.render("ESC  menu", True, GRIS)
        fenetre.blit(esc, (20, HAUTEUR-26))
        # Prochain objet
        if len(tapis_slots) > 1:
            pr = font_tiny.render("Prochain :", True, GRIS)
            fenetre.blit(pr, (TAPIS_X, TAPIS_Y-62))
            dessiner_objet(fenetre, tapis_slots[1]["info"], TAPIS_X+50, TAPIS_Y-40)

    def dessiner_feedback():
        if feedback["timer"] > 0:
            t  = font_big.render(feedback["texte"], True, feedback["couleur"])
            fy = HAUTEUR//3 - max(0, (30 - feedback["timer"])) * 2
            fenetre.blit(t, (LARGEUR//2 - t.get_width()//2, fy))

    def dessiner_fin():
        ov = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        ov.fill((0,0,0,190))
        fenetre.blit(ov, (0,0))
        t1 = font_big.render(msg_fin, True, VERT_VIF)
        t2 = font_med.render("Score final : {}".format(score), True, BLANC)
        t3 = font_med.render("ESC  →  Menu principal", True, GRIS)
        fenetre.blit(t1, (LARGEUR//2 - t1.get_width()//2, HAUTEUR//2 - 80))
        fenetre.blit(t2, (LARGEUR//2 - t2.get_width()//2, HAUTEUR//2))
        fenetre.blit(t3, (LARGEUR//2 - t3.get_width()//2, HAUTEUR//2 + 60))

    # ===================== BOUCLE =====================
    # boucle principale du niveau 1, tourne a 60 fps
    en_cours = True

    while en_cours:

        # Tapis anime
        tapis_offset = (tapis_offset + TAPIS_VITESSE) % (TAPIS_W // 12 + 1)

        # Slots glissent vers droite et bouclent en boucle infinie
        for s in tapis_slots:
            s["rel"] += 0.5
            if s["rel"] > TAPIS_W - 12:
                s["rel"] = 12.0

        # Physique vol
        if vol is not None:
            vol["vy"] = appliquer_gravite(vol["vy"], GRAVITE)
            vol["x"], vol["y"] = mettre_a_jour_position(vol["x"], vol["y"], vol["vx"], vol["vy"])

            # rebond au sol, le -0.35 c'est pour inverser et reduire la vitesse
            if vol["y"] >= SOL_Y - 12:
                if abs(vol["vy"]) > 3:
                    vol["vy"] *= -0.35
                    vol["vx"] *= 0.7
                    vol["y"]   = float(SOL_Y - 12)
                else:
                    vol = None
                    vies -= 1
                    feedback["texte"]   = "Raté !"
                    feedback["couleur"] = (220,60,60)
                    feedback["timer"]   = 55
                    idx += 1
                    objet_joueur = None
                    if vies <= 0:
                        fin = True; msg_fin = "Perdu..."
                    elif idx >= TOTAL_OBJETS:
                        fin = True; msg_fin = "Niveau terminé !"
                    else:
                        tapis_slots.clear()
                        tapis_slots.extend(construire_slots())
                        prendre_premier()

            # Collision poubelle
            if vol is not None:
                for p in poubelles:
                    zone = pygame.Rect(p["x"]+2, p["y"]-14, p["w"]-4, p["h"]+14)
                    if verifier_collision(vol["x"], vol["y"], zone):
                        ok = vol["info"]["type"] == p["type"]
                        ajouter_particules(int(vol["x"]), int(vol["y"]), p["couleur"], ok)
                        p["shake"] = 14
                        if ok:
                            score += 100
                            feedback["texte"]   = "Bien trié !  +100"
                            feedback["couleur"] = VERT_VIF
                        else:
                            vies -= 1
                            feedback["texte"]   = "Mauvaise poubelle !"
                            feedback["couleur"] = (220,60,60)
                        feedback["timer"] = 55
                        vol = None
                        idx += 1
                        objet_joueur = None
                        if vies <= 0:
                            fin = True; msg_fin = "Perdu..."
                        elif idx >= TOTAL_OBJETS:
                            fin = True; msg_fin = "Niveau terminé !"
                        else:
                            tapis_slots.clear()
                            tapis_slots.extend(construire_slots())
                            prendre_premier()
                        break

        maj_particules()
        if feedback["timer"] > 0:
            feedback["timer"] -= 1

        # Dessin
        dessiner_fond()
        dessiner_tapis()

        # Objets sur tapis (en boucle visible)
        for s in tapis_slots:
            ox2 = TAPIS_X + int(s["rel"])
            if TAPIS_X + 10 <= ox2 <= TAPIS_X + TAPIS_W - 10:
                dessiner_objet(fenetre, s["info"], ox2, TAPIS_Y - 22)

        dessiner_joueur(objet_joueur is not None)

        if objet_joueur is not None:
            dessiner_objet(fenetre, objet_joueur, JOUEUR_X + JOUEUR_W + 30, JOUEUR_Y + 5)

        mx, my = pygame.mouse.get_pos()
        if vise:
            dessiner_vise(mx, my)

        if vol is not None:
            dessiner_objet(fenetre, vol["info"], int(vol["x"]), int(vol["y"]))

        for p in poubelles:
            dessiner_poubelle(p)

        dessiner_particules()
        dessiner_hud()
        dessiner_feedback()

        if fin:
            dessiner_fin()

        pygame.display.flip()
        horloge.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return "quitter", score
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return "menu", score
            if not fin:
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if objet_joueur is not None and vol is None:
                        vise = True
                # si le joueur relache le clic, on lance l'objet
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    if vise and objet_joueur is not None and vol is None:
                        vise = False
                        ox2  = JOUEUR_X + JOUEUR_W + 30
                        oy2  = JOUEUR_Y + 5
                        dx   = mx - ox2
                        dy   = my - oy2
                        dist = math.hypot(dx, dy)
                        if dist > 5:
                            puissance = min(dist / 6, 26)
                            vx = (dx/dist) * puissance
                            vy = (dy/dist) * puissance
                            vol = {
                                "x": float(ox2), "y": float(oy2),
                                "vx": vx, "vy": vy,
                                "info": objet_joueur,
                            }
                            objet_joueur = None

    return "menu", score