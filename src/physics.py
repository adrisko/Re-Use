# physics.py - module pour gerer les trajectoires et la physique du jeu
# on utilise le module math pour sqrt et hypot
import math

GRAVITE = 0.45  # valeur simplifiee de la gravite pour le rendu a l'ecran

# applique la gravite sur la vitesse verticale
def appliquer_gravite(vy):
    vy = vy + GRAVITE
    return vy

# met a jour la position d'un objet en fonction de sa vitesse
def mettre_a_jour_position(x, y, vx, vy):
    x = x + vx
    y = y + vy
    return x, y, vx, vy

# verifie si un point (px, py) est dans une zone rectangulaire
def verifier_collision(px, py, zone_x, zone_y, zone_w, zone_h):
    if px >= zone_x and px <= zone_x + zone_w:
        if py >= zone_y and py <= zone_y + zone_h:
            return True
    return False

# calcule la distance entre deux points
def calculer_distance(x1, y1, x2, y2):
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist

# calcule la puissance du lancer en fonction de la distance de la souris
def calculer_puissance(dist):
    puissance = dist / 6
    if puissance > 26:
        puissance = 26
    return puissance

# calcule la vitesse de lancer (vx et vy) en fonction de la direction et puissance
def calculer_vitesse_lancer(ox, oy, mx, my):
    dx = mx - ox
    dy = my - oy
    dist = calculer_distance(ox, oy, mx, my)
    if dist < 1:
        return 0, 0, 0
    puissance = calculer_puissance(dist)
    vx = (dx / dist) * puissance
    vy = (dy / dist) * puissance
    return vx, vy, dist

# simule le rebond au sol
def rebond_sol(vy, vx):
    if abs(vy) > 3:
        vy = vy * -0.35
        vx = vx * 0.7
        return vx, vy, False  # False = pas arrete
    else:
        return 0, 0, True  # True = objet arrete
