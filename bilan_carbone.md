# Bilan carbone - Re-Use

## Hypotheses

- Duree moyenne d'une partie : 2 minutes
- Type de machine : PC portable (consommation moyenne 30W)
- Rafraichissement : 60 images par seconde (60 FPS)
- Ecran : 1280x720 pixels
- Bibliotheque : Pygame

## Calculs

Consommation par partie :
- Puissance = 30 W
- Duree = 2 min = 0.0333 h
- Energie = 30 x 0.0333 = 1 Wh = 0.001 kWh

Emissions CO2 par partie (mix electrique francais = 50 g CO2/kWh) :
- 0.001 x 50 = 0.05 g CO2 par partie

Pour 1000 parties :
- 1000 x 0.05 = 50 g CO2
- C'est l'equivalent de 300 metres en voiture

## Actions d'eco-conception

- On limite le jeu a 60 FPS avec clock.tick(60) pour pas utiliser le CPU a fond
- Les graphismes sont dessines par code (pas de fichiers images lourds a charger)
- Le nombre de calculs par frame est reduit (on fait les calculs de physique une seule fois par boucle)
- Pas de musique de fond en boucle pour reduire la charge CPU
- La resolution est fixe (1280x720) pas besoin de calculs d'adaptation
