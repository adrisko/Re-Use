# module physique pour gerer les trajectoires des objets
# valeur trouvée en testant, ça marche bien pour le rendu
GRAVITE = 0.45

# applique la gravite sur la vitesse verticale
def appliquer_gravite(vy, gravite=0.45):
    vy = vy + gravite
    return vy

# met a jour la position avec les vitesses
def mettre_a_jour_position(x, y, vx, vy):
    x = x + vx
    y = y + vy
    return x, y

# verifie si un point est dans un rectangle pygame
# TODO: peut-être ajouter la résistance de l'air plus tard
def verifier_collision(obj_x, obj_y, zone_rect):
    return zone_rect.collidepoint(int(obj_x), int(obj_y))
