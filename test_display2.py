import pygame
import sys

# 1. Initialisation de Pygame
pygame.init()

# 2. Création de la fenêtre (Largeur, Hauteur)
ecran = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mon super premier jeu !")

# 3. La Boucle Principale (Game Loop)
en_cours = True
while en_cours:

    # Étape A : Capturer les événements (clics, touches du clavier)
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:  # Si on clique sur la croix rouge
            en_cours = False

    # Étape B : Remplir l'écran avec une couleur (Rouge, Vert, Bleu)
    ecran.fill((255, 255, 255))  # Un blanc foncé sympa
    pygame.display.flip()
    ecran.fill((30, 30, 30))  # Un gris foncé sympa

    # Étape C : Mettre à jour l'affichage de l'écran
    # pygame.display.flip()

# 4. Quitter proprement le programme
pygame.quit()
sys.exit()
