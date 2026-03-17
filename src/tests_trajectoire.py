# tests_trajectoire.py - tests simples pour verifier que la physique marche
from physics import appliquer_gravite, mettre_a_jour_position, verifier_collision
from physics import calculer_distance, calculer_puissance, rebond_sol, GRAVITE

# test 1 : la gravite augmente la vitesse verticale
vy = 0
vy = appliquer_gravite(vy)
print("Test 1 - gravite : vy apres 1 pas =", vy)
assert vy == GRAVITE, "Test 1 rate"
print("Test 1 OK")

# test 2 : la position se met a jour correctement
x, y, vx, vy = mettre_a_jour_position(100, 200, 5, 3)
print("Test 2 - position : x={}, y={}".format(x, y))
assert x == 105 and y == 203, "Test 2 rate"
print("Test 2 OK")

# test 3 : collision detectee quand le point est dans la zone
resultat = verifier_collision(50, 50, 40, 40, 30, 30)
print("Test 3 - collision dedans :", resultat)
assert resultat == True, "Test 3 rate"
print("Test 3 OK")

# test 4 : pas de collision quand le point est en dehors
resultat = verifier_collision(10, 10, 40, 40, 30, 30)
print("Test 4 - collision dehors :", resultat)
assert resultat == False, "Test 4 rate"
print("Test 4 OK")

# test 5 : la puissance est bien limitee a 26
p = calculer_puissance(300)
print("Test 5 - puissance max :", p)
assert p == 26, "Test 5 rate"
print("Test 5 OK")

# test 6 : le rebond arrete l'objet quand la vitesse est faible
vx, vy, arrete = rebond_sol(2, 5)
print("Test 6 - rebond faible : arrete =", arrete)
assert arrete == True, "Test 6 rate"
print("Test 6 OK")

print("")
print("Tous les tests sont passes !")
