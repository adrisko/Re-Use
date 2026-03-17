# Bilan Carbone - Re-Use

## Hypotheses

- Duree moyenne d'une partie : 2 minutes
- Materiel : PC portable consommant environ 30W
- Affichage : 60 FPS, resolution 1920x1080
- Pas de serveur distant, le jeu tourne en local

## Calcul de la consommation par partie

- Consommation electrique par partie : 30W x (2/60) h = **1 Wh = 0.001 kWh**
- Mix energetique francais : environ 50g CO2/kWh (source : RTE)
- Emissions par partie : 0.001 kWh x 50g CO2/kWh = **0.05g CO2 par partie**

## A grande echelle

- Pour 1000 parties : 1000 x 0.05g = **50g CO2**
- Equivalent : environ 300m en voiture (source : ADEME, 150g CO2/km)

## Mesures d'eco-conception

- **Limitation a 60 FPS** : on utilise `clock.tick(60)` pour ne pas faire tourner le GPU a fond
- **Particules limitees** : maximum 20 particules par explosion pour limiter les calculs
- **Pas de musique de fond** : evite de charger des fichiers audio lourds en memoire
- **Images generees par code** : tous les objets (poubelles, joueur, objets) sont dessines avec pygame.draw, pas de fichiers image externes lourds
