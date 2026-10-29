import parsing


class DronesManager:
    def __init__(self) -> None:
        super().__init__()
        self.travel_log: list[list[parsing.MapParsing.Drone]] = []
        self.drone_list: list[parsing.MapParsing.Drone] = []

    def dijkstra_algorythm(self) -> None:
        pass

    # Prend chaque Drone dans l'ordre et cherche le chemin le plus cours en fonction du positionnement des autre drones et des zones

    # Chaque hub contient:
    #   - la liste des hub connectes par ordre de priorite
    #   - la liste des drones present a l'instant t (le tour en cours)
    #
    # Chaque connection contient la liste des drones presents a l'instant t (le tour en cours)
    #
    # Chaque dorne contient:
    #   - parcours definie precedement du depart a l'arrivee, ou None si aucun effectue
    #   - parcours tempo permettant les retours en arrieres
    #     (generalement une copie du parcours en cours juste avant de faire un retour en arriere d'un hub)
    #   - etat du parcours en cours (tous les hub traverse et l'emplacement en cours)
    #
    # Deplacement des Drones:
    # While sur tous les drones:
    #   Examine le type de hub connecte a celui en cours dans l'ordre
    #   (cette boucle est effectue jusqu'a ce que tous les parcours possible aient ete testes):
    #       => si toutes les destinations de ce hub testees:
    #           => si hub_start, la boucle principale est terminee (tous les parcours ont ete testes):
    #               => si aucun parcours trouve, les tests sont termine, un message d'erreur apparait
    #               => sinon: on passe aux tets sur le drone suivant
    #           => sinon: revient un hub en arriere et continue les tests
    #       => Si hub_end:
    #           - s'y deplace
    #           - compare le nombre de tours effectue avec celui du parcours precedent:
    #               => si moins de tours ou aucun parcours enregistre precedement, ce parcours est enregistre a la place de l'autre
    #       => Si deja visite ou blocked, passe au test sur le hub suivant
    #       => Si deja occupe, passe les tours jusqu'a ce qu'il soit libre et s'y deplace

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
#     ◦ blocked – Inaccessible zone. Drones must not enter
#       or pass through this zone.
#     Any path using it is invalid.
#     ◦ restricted – A sensitive or dangerous zone.
#       Movement to this zone costs 2 turns.
#     ◦ priority – A preferred zone. Movement to this zone costs 1 turn
#       but should be prioritized in pathfinding

# 1/ Prend les drones par ordre de numero
# 2/ Trouve le chemin le plus court en fonction de l'emplacement
#    de tous les precedents dans le temps
# 3/ Mise du journal de positionnement de tous les drones impliques
#    (celui en court et les precedents)
#    dans le temps (parsing.Drone.positioning_log)
# 4/ Mise a jour du journal de deplacement en fonction de chaque tour
#    (liste de liste de drones): self.travel_log
# Le deplacement de tous les drones ne sera affiche qu'une fois boucle

# self.drone_list: list[MapParsing.Drone] = []

# class Drone(BaseModel):
# 	id: int
# 	hub_pos: "MapParsing.HubData | MapParsing.Connection"
# 	positioning_log: list [int, "MapParsing.HubData | MapParsing.Connection"]
