import pygame
import sys


class Displaying:
    def __init__(self) -> None:
        self.hub_size: int = 60

        self.map_start_x: int = 0
        self.map_start_y: int = 0

        self.map_end_x: int = 0
        self.map_end_y: int = 0

        self.map_offsetX: int = 0
        self.map_offsetY: int = 0

        self.map_size_x: int = 0
        self.map_size_y: int = 0

    def display_map_datas(self) -> None:
        """Display Graphical Map from File"""
        if self.map_text is None:
            raise ValueError("No Map Loaded")
        if self.map_clean is None or self.map_clean == []:
            raise ValueError("Map is not Cleaned")
        if self.hub_list is None or self.hub_list == []:
            raise ValueError("Zones are not listed")
        if self.connection_list is None or self.connection_list == []:
            raise ValueError("Connections are not listed")
        if self.nb_drones is None or self.nb_drones < 1:
            raise ValueError("Quantite of drones not determined")
        print()
        print(f"NOMBRE DE DRONES:\n{self.nb_drones}")
        print(f"\nZONES LIST:\n{self.hub_list}")
        print(f"\nCONNECTIONS LIST:\n{self.connection_list}")

    def calcul_map_size(self) -> None:
        """Calcul size of the Map"""

        # Determine coord start and end of the map
        for hub in self.hub_list:
            print(
                f"coord X: {hub[0].coordX}, coord X: {hub[0].coordY}"
            )  # TEMPO
            if hub[0].coordX < self.map_start_x:
                self.map_start_x = hub[0].coordX
            elif hub[0].coordY < self.map_start_y:
                self.map_start_y = hub[0].coordY
            if hub[0].coordX > self.map_end_x:
                self.map_end_x = hub[0].coordX
            elif hub[0].coordY > self.map_end_y:
                self.map_end_y = hub[0].coordY
        print(f"Map Start: [{self.map_start_x},{self.map_start_y}]")  # TEMPO
        print(f"Map End: [{self.map_end_x},{self.map_end_y}]")  # TEMPO

        # Calcul offset with coord [0,0] if negative coord
        if self.map_start_x < 0:
            self.map_offsetX = self.map_start_x * -1
        if self.map_start_y < 0:
            self.map_offsetY = self.map_start_y * -1
        print(
            f"Map Offset X: {self.map_offsetX}, "
            f"Map Offset Y: {self.map_offsetY}"
        )  # TEMPO

        # Calcul size of the map:
        self.map_size_x = self.map_end_x - self.map_start_x + 1
        self.map_size_y = self.map_end_y - self.map_start_y + 1

        self.map_size_x = self.map_size_x * (self.hub_size + 5)
        self.map_size_y = self.map_size_y * (self.hub_size + 5)
        print(
            f"Map Size X: {self.map_size_x}, Map Size Y: {self.map_size_y}"
        )  # TEMPO

    def displaying_map(self) -> None:
        """Display Map and maps elements"""
        pygame.init()

        # Creat window
        window = pygame.display.set_mode((self.map_size_x, self.map_size_y))
        pygame.display.set_caption("My super MAP !!!!!!!!!!")

        # main loop
        in_progress = True
        while in_progress:

            # Capture events
            for evenement in pygame.event.get():
                if (
                    evenement.type == pygame.QUIT
                ):  # Si on clique sur la croix rouge
                    in_progress = False

            # Fill window with one color TEMPO
            window.fill((30, 30, 30))  # Un gris foncé sympa
            a = 31  # TEMPO
            pygame.draw.circle(
                window, pygame.Color("crimson"), (a, 31), self.hub_size / 2
            )  # TEMPO
            a = a + self.hub_size + 5
            pygame.draw.circle(
                window, pygame.Color("crimson"), (a, 31), self.hub_size / 2
            )  # TEMPO
            a = a + self.hub_size + 5
            pygame.draw.circle(
                window, pygame.Color("crimson"), (a, 31), self.hub_size / 2
            )  # TEMPO
            a = a + self.hub_size + 5
            pygame.draw.circle(
                window, pygame.Color("crimson"), (a, 31), self.hub_size / 2
            )  # TEMPO
            a = a + self.hub_size + 5
            pygame.draw.circle(
                window, pygame.Color("crimson"), (a, 31), self.hub_size / 2
            )  # TEMPO
            a = a + self.hub_size + 5
            pygame.draw.circle(
                window, pygame.Color("crimson"), (a, 31), self.hub_size / 2
            )  # TEMPO
            a = a + self.hub_size + 5
            pygame.draw.circle(
                window, pygame.Color("crimson"), (a, 31), self.hub_size / 2
            )  # TEMPO
            a = a + self.hub_size + 5
            pygame.draw.circle(
                window, pygame.Color("crimson"), (a, 31), self.hub_size / 2
            )  # TEMPO

            pygame.display.flip()

            # Étape C : Mettre à jour l'affichage de l'écran
            # pygame.display.flip()

        # quit display
        pygame.quit()
        sys.exit()


# Calcul de la taille de la fenetre de la map
# Affichage de la map
# Affichage chaque element
# Gestion animation des elements dans la map
