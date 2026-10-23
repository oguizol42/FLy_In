import parsing


class DronesManager:
    def __init__(self) -> None:
        super().__init__()
        self.travel_log: list[list[parsing.MapParsing.Drone]] = []
        self.drone_list: list[parsing.MapParsing.Drone] = []

    def dijkstra_algorythm(self) -> None:
        pass

    def drones_manager(self) -> None:
        """Manage Drones Movements"""
        drone: parsing.MapParsing.Drone

        if self.drone_list is None or self.drone_list == []:
            raise ValueError("There is no drone in the map")

        print("ALGORYTHME:\n")  # TEMPO
        for drone in self.drone_list:
            print(f"Traitement drone D{drone.id}")  # TEMPO


# Zone types:
#     ◦ normal – Standard zone with 1 turn movement cost (default)
#     ◦ blocked – Inaccessible zone. Drones must not enter or pass through this zone.
#     Any path using it is invalid.
#     ◦ restricted – A sensitive or dangerous zone. Movement to this zone costs 2
#     turns.
#     ◦ priority – A preferred zone. Movement to this zone costs 1 turn but should
#     be prioritized in pathfinding

# 1/ Prend les drones par ordre de numero
# 2/ Trouve le chemin le plus court en fonction de l'emplacement de tous les precedents dans le temps
# 3/ Mise du journal de positionnement de tous les drones impliques (celui en court et les precedents)
#    dans le temps (parsing.Drone.positioning_log)
# 4/ Mise a jour du journal de deplacement en fonction de chaque tour (liste de liste de drones): self.travel_log
# Le deplacement de tous les drones ne sera affiche qu'une fois boucle

# self.drone_list: list[MapParsing.Drone] = []

# class Drone(BaseModel):
# 	id: int
# 	hub_pos: "MapParsing.HubData | MapParsing.Connection"
# 	positioning_log: list [int, "MapParsing.HubData | MapParsing.Connection"]
