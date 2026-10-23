import pygame
import sys
import parsing
from typing import Optional


class Displaying:
    map_text: Optional[str]
    map_clean: list[str]
    hub_list: list[parsing.MapParsing.Hub]
    connection_name_list: list[tuple[list[str], int]]
    connection_list: list[parsing.MapParsing.Connection]
    drone_list: list[parsing.MapParsing.Drone]
    nb_drones: int

    def find_hub_by_type2(
        self, type: str
    ) -> Optional[parsing.MapParsing.Hub]: ...

    def __init__(self) -> None:
        super().__init__()

        self.hub_size: int = 50

        self.map_start_x: int = 0
        self.map_start_y: int = 0

        self.map_end_x: int = 0
        self.map_end_y: int = 0

        self.map_offsetX: int = 0
        self.map_offsetY: int = 0

        self.map_size_x: int = 0
        self.map_size_y: int = 0

        self.space_hubs_X: int = 100  # space between two hubs on X axis
        self.space_hubs_Y: int = 100  # space between two hubs on Y axis
        self.space_board_X: int = 50  # space with board on X axis
        self.space_board_Y: int = 50  # space with board on Y axis

    def display_map_datas(self) -> None:
        """Display All Map Informations"""
        if self.map_text is None:
            raise ValueError("No Map Loaded")
        if self.map_clean is None or self.map_clean == []:
            raise ValueError("Map is not Cleaned")
        if self.hub_list is None or self.hub_list == []:
            raise ValueError("Zones are not listed")
        if (
            self.connection_name_list is None
            or self.connection_name_list == []
        ):
            raise ValueError("Connections are not listed")
        if self.nb_drones is None or self.nb_drones < 1:
            raise ValueError("Quantite of drones not determined")
        print()
        print(f"NOMBRE DE DRONES:\n{self.nb_drones}")
        print(f"\nHUBS LIST:\n{self.hub_list}")
        print(f"\nCONNECTIONS LIST:\n{self.connection_name_list}")
        print(f"\nCONNECTIONS LIST PAR HUB:\n{self.connection_list}")
        print(f"\nDRONES LIST:\n{self.drone_list}")

    def display_main_datas(self) -> None:
        """Display Datas Informations of Map"""
        hub: Optional[parsing.MapParsing.Hub]
        # hub_datas: parsing.MapParsing.Hub.HubData
        # hub_metas: parsing.MapParsing.Hub.HubMeta
        connection: parsing.MapParsing.Connection

        if self.map_text is None:
            raise ValueError("No Map Loaded")
        if self.map_clean is None or self.map_clean == []:
            raise ValueError("Map is not Cleaned")
        if self.hub_list is None or self.hub_list == []:
            raise ValueError("Zones are not listed")
        if (
            self.connection_name_list is None
            or self.connection_name_list == []
        ):
            raise ValueError("Connections are not listed")
        if self.nb_drones is None or self.nb_drones < 1:
            raise ValueError("Quantite of drones not determined")
        print()
        print(f"NOMBRE DE DRONES: {self.nb_drones}")

        hub = self.find_hub_by_type2("start_hub")
        if hub is None:
            raise ValueError("start_hub is not defined in this map")

        print(
            f"\nSTART HUB: \n"
            f"  Name: {hub.datas.name}\n"
            f"  Coord: {hub.datas.coordX} {hub.datas.coordY}\n"
            f"  Color: {hub.metas.color}\n"
            f"  Max Drones: {hub.metas.max_drones}"
        )

        hub = self.find_hub_by_type2("end_hub")
        if hub is None:
            raise ValueError("end_hub is not defined in this map")

        print(
            f"\nEND HUB: \n"
            f"  Name: {hub.datas.name}\n"
            f"  Coord: {hub.datas.coordX} {hub.datas.coordY}\n"
            f"  Color: {hub.metas.color}\n"
            f"  Max Drones: {hub.metas.max_drones}"
        )

        print("\nHUBS LIST:")
        for hub in self.hub_list:
            if hub.datas.type == "start_hub" or hub.datas.type == "end_hub":
                continue
            print(
                f"{hub.datas.name} {hub.datas.coordX} {hub.datas.coordY}, "
                f"color: {hub.metas.color}, "
                f"zone type: {hub.metas.zone_type}, "
                f"max drones: {hub.metas.max_drones}"
            )

        print("\nCONNECTIONS LIST:\n")
        for connection in self.connection_list:
            print(
                f"ID: {connection.id}, "
                f"Connection: {connection.hub1.name}-{connection.hub2.name}, "
                f"Qty Drone In: {connection.nb_drones_in}, "
                f"Max Drones Allow: {connection.max_drones_allow}"
            )

        print("\n\n\n")

    def calcul_map_size(self) -> None:
        """Calcul size of the Map"""

        # Determine coord start and end of the map
        for hub in self.hub_list:
            # print(
            #     f"coord X: {hub[0].coordX}, coord Y: {hub[0].coordY}"
            # )  # TEMPO
            if hub.datas.coordX < self.map_start_x:
                self.map_start_x = hub.datas.coordX
            if hub.datas.coordY < self.map_start_y:
                self.map_start_y = hub.datas.coordY
            if hub.datas.coordX > self.map_end_x:
                self.map_end_x = hub.datas.coordX
            if hub.datas.coordY > self.map_end_y:
                self.map_end_y = hub.datas.coordY
        # print(f"Map Start: [{self.map_start_x},{self.map_start_y}]")  # TEMPO
        # print(f"Map End: [{self.map_end_x},{self.map_end_y}]")  # TEMPO

        # Calcul offset with coord [0,0] if negative coord
        if self.map_start_x < 0:
            self.map_offsetX = self.map_start_x * -1
        if self.map_start_y < 0:
            self.map_offsetY = self.map_start_y * -1
        # print(
        #     f"Map Offset X: {self.map_offsetX}, "
        #     f"Map Offset Y: {self.map_offsetY}"
        # )  # TEMPO

        # Calcul size of the map:
        self.map_size_x = self.map_end_x - self.map_start_x + 1
        self.map_size_y = self.map_end_y - self.map_start_y + 1

        self.map_size_x = (
            self.map_size_x * (self.hub_size + self.space_hubs_X)
            - self.space_hubs_X
            + (self.space_board_X * 2)
        )
        self.map_size_y = (
            self.map_size_y * (self.hub_size + self.space_hubs_Y)
            - self.space_hubs_Y
            + (self.space_board_Y * 2)
        )
        # print(
        #     f"Map Size X: {self.map_size_x}, Map Size Y: {self.map_size_y}"
        # )  # TEMPO

    def calcul_real_pos(
        self, hub: parsing.MapParsing.Hub.HubData
    ) -> tuple[int, int]:
        """Calcul coordonnees in graphical map"""
        posX: int
        posY: int

        # Calcul Hub Coord
        posX = hub.coordX + self.map_offsetX
        posX = posX * (self.hub_size + self.space_hubs_X)
        posX = int(posX + self.hub_size / 2)  # pile au bord
        posX += self.space_board_X

        posY = hub.coordY + self.map_offsetY
        posY = posY * (self.hub_size + self.space_hubs_Y)
        posY = int(posY + self.hub_size / 2)  # pile au bord
        posY += self.space_board_Y

        return posX, posY

    def displaying_map(self) -> None:
        """Display Map and maps elements"""
        posX: int = 0
        posY: int = 0
        posX2: int = 0
        posY2: int = 0
        color: str = "yellow"

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

            # Fill window
            window.fill((99, 99, 99))

            # connections setup on screen
            for connection in self.connection_list:
                posX, posY = self.calcul_real_pos(connection.hub1)
                posX2, posY2 = self.calcul_real_pos(connection.hub2)
                pygame.draw.line(
                    window,
                    pygame.Color("brown"),
                    (posX, posY),
                    (posX2, posY2),
                    3,
                )

            # hub setup on screen
            for hub in self.hub_list:
                posX, posY = self.calcul_real_pos(hub.datas)

                # Display Hub
                if hub.metas.color is not None:
                    color = hub.metas.color

                pygame.draw.circle(
                    window,
                    pygame.Color(color),
                    (posX, posY),
                    self.hub_size / 2,
                )

                pygame.draw.circle(
                    window,
                    pygame.Color("red"),
                    (posX, posY),
                    self.hub_size / 2,
                    9,
                )

                pygame.draw.circle(
                    window,
                    pygame.Color("white"),
                    (posX, posY),
                    self.hub_size / 2,
                    6,
                )

                pygame.draw.circle(
                    window,
                    pygame.Color("blue"),
                    (posX, posY),
                    self.hub_size / 2,
                    3,
                )

                # Hub Name
                police = pygame.font.Font(None, 20)
                text = police.render(
                    hub.datas.name, True, pygame.Color("black")
                )

                text_zone = text.get_rect()

                text_zone.center = (posX, posY - int((self.hub_size / 2)) - 5)

                window.blit(text, text_zone)

            pygame.display.flip()

            # Étape C : Mettre à jour l'affichage de l'écran
            # pygame.display.flip()

        # quit display
        pygame.quit()
        sys.exit()

    def displaying_simulation(self) -> None:
        """Display simulation step by step"""
        # • The simulation must output the step-by-step movement of drones
        #   from the start to the end zone.
        # • Each simulation turn is represented by a line.
        # • A line must list all the drone movements
        #   that occur during that turn, space-
        # separated. Each movement must follow the format:
        #           D<ID>-<zone>, or D<ID>-<connection>
        # in case of drones still in flight toward restricted zones.
        #     ◦ D<ID> refers to the unique drone identifier (e.g., D1, D2).
        #     ◦ <zone> is the name of the destination zone.
        #     ◦ <connection> is the name of the connection toward
        #       a restricted zone.
        # • Drones that do not move in a given turn are omitted from that line.
        # • Drones that reach the end zone are considered delivered
        #   and are no longer tracked.
        # • The simulation ends when all drones have reached the end zone.
        # • Example:
        #     D1-roof1 D2-corridorA
        #     D1-roof2 D2-tunnelB
        #     D1-goal D2-goal
        pass


# Calcul de la taille de la fenetre de la map
# Affichage de la map
# Affichage chaque element
# Gestion animation des elements dans la map
