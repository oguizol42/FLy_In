import parsing


class DronesManager:
    def __init__(self) -> None:
        self.travel_log: list[list[parsing.MapParsing.Drone]] = []
        super().__init__()

    def dijkstra_algorythm(self) -> None:
        pass


# 1/ Prend les drones par ordre de numero
# 2/ Trouve le chemin le plus court en fonction de l'emplacement de tous les precedents dans le temps
# 3/ Mise du journal de positionnement de tous les drones impliques (celui en court et les precedents) dans le temps (parsing.Drone.positioning_log)
# 4/ Mise a jour du journal de deplacement en fonction de chaque tour (liste de liste de drones): self.travel_log
# Le deplacement de tous les drones ne sera affiche qu'une fois boucle
