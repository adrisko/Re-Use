import math

GRAVITE = 0.45


def appliquer_gravite(vy):
    vy = vy + GRAVITE
    return vy


def mettre_a_jour_position(x, y, vx, vy):
    x = x + vx
    y = y + vy
    return x, y, vx, vy


def verifier_collision(px, py, zone_x, zone_y, zone_w, zone_h):
    if px >= zone_x and px <= zone_x + zone_w:
        if py >= zone_y and py <= zone_y + zone_h:
            return True
    return False


def calculer_distance(x1, y1, x2, y2):
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist


def calculer_puissance(dist):
    puissance = dist / 6
    if puissance > 26:
        puissance = 26
    return puissance


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


def rebond_sol(vy, vx):
    if abs(vy) > 3:
        vy = vy * -0.35
        vx = vx * 0.7
        return vx, vy, False
    else:
        return 0, 0, True
