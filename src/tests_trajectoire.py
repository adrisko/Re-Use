# tests pour le module physics
# on utilise juste des print et assert, pas besoin de pytest

import pygame
pygame.init()

from src.physics import appliquer_gravite, mettre_a_jour_position, verifier_collision, GRAVITE

# test 1 : la gravite augmente bien vy
vy = 0
vy = appliquer_gravite(vy)
assert vy == 0.45, "la gravite devrait ajouter 0.45"
print("Test 1 OK - gravite augmente vy")

# test 2 : position apres un pas de temps
x, y = mettre_a_jour_position(100, 200, 5, 3)
assert x == 105, "x devrait etre 105"
assert y == 203, "y devrait etre 203"
print("Test 2 OK - position mise a jour correctement")

# test 3 : collision detectee quand le point est dans la zone
zone = pygame.Rect(50, 50, 100, 100)
resultat = verifier_collision(75, 75, zone)
assert resultat == True, "le point est dans la zone, devrait etre True"
print("Test 3 OK - collision detectee")

# test 4 : collision non detectee quand le point est en dehors
resultat2 = verifier_collision(200, 200, zone)
assert resultat2 == False, "le point est en dehors, devrait etre False"
print("Test 4 OK - pas de collision en dehors")

# test 5 : vitesse de 0, l'objet bouge pas
x2, y2 = mettre_a_jour_position(100, 200, 0, 0)
assert x2 == 100 and y2 == 200, "avec vitesse 0 ca devrait pas bouger"
print("Test 5 OK - vitesse nulle, position inchangee")

print("")
print("Tous les tests sont passes !")
