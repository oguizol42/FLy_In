import pygame
import sys

# 1. Initialisation de Pygame
pygame.init()

# 2. Configuration de la fenêtre (Largeur, Hauteur)
LARGEUR, HAUTEUR = 800, 600
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Mon premier carre bleu")

# 3. Définition des couleurs (Rouge, Vert, Bleu)
NOIR = (0, 0, 0)
BLEU = (0, 128, 255)

# Boucle principale du jeu
en_cours = True
while en_cours:

    # Événements (clavier, souris, fermeture de fenêtre)
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:  # Si on clique sur la croix rouge
            en_cours = False

    # Logique du jeu (à remplir plus tard)

    # Dessin
    ecran.fill(NOIR)  # On efface l'écran avec du noir

    # On dessine un rectangle bleu (sur 'ecran', couleur 'BLEU', [X, Y, Largeur, Hauteur])
    pygame.draw.rect(ecran, BLEU, [350, 250, 100, 100])
    pygame.draw.circle(ecran, (0, 128, 0), [51, 51], 50)
    pygame.draw.circle(ecran, (0, 0, 255), [51, 51], 50)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter proprement le programme
pygame.quit()
sys.exit()
