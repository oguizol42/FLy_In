import parsing
from typing import Optional


class DronesManager:
    hub_list: list[parsing.MapParsing.Hub]

    def __init__(self) -> None:
        super().__init__()
        self.travel_log: list[list[parsing.MapParsing.Drone]] = []
        self.drone_list: list[parsing.MapParsing.Drone] = []

    def sort_hubs_neighbours(self) -> None:
        """Sort neighboring_hubs of every hubs in order of priority"""
        hub: parsing.MapParsing.Hub
        hub_neighbour: parsing.MapParsing.Hub
        connection: parsing.MapParsing.Connection
        hub_connection: tuple[
            parsing.MapParsing.Hub, parsing.MapParsing.Connection
        ]
        hubs_priority: list[
            tuple[parsing.MapParsing.Hub, parsing.MapParsing.Connection]
        ]
        hubs_normal: list[
            tuple[parsing.MapParsing.Hub, parsing.MapParsing.Connection]
        ]
        hubs_restricted: list[
            tuple[parsing.MapParsing.Hub, parsing.MapParsing.Connection]
        ]
        hubs_blocked: list[
            tuple[parsing.MapParsing.Hub, parsing.MapParsing.Connection]
        ]

        for hub in self.hub_list:
            hubs_priority = []
            hubs_normal = []
            hubs_restricted = []
            hubs_blocked = []
            if hub.neighboring_hubs is not None and hub.neighboring_hubs != []:
                for hub_neighbour, connection in hub.neighboring_hubs:
                    if (
                        hub_neighbour.metas.zone_type == "blocked"
                        or hub_neighbour.datas.type == "start_hub"
                    ):
                        hubs_blocked.append((hub_neighbour, connection))

                    elif hub_neighbour.datas.type == "end_hub":
                        hubs_priority.insert(0, (hub_neighbour, connection))

                    elif hub_neighbour.metas.zone_type == "priority":
                        hubs_priority.append((hub_neighbour, connection))

                    elif hub_neighbour.metas.zone_type == "normal":
                        hubs_normal.append((hub_neighbour, connection))

                    elif hub_neighbour.metas.zone_type == "restricted":
                        hubs_restricted.append((hub_neighbour, connection))

                    hub.neighboring_hubs = []
                    hub.neighboring_hubs_forbiden = []

                    if hub.metas.zone_type != "end_hub":
                        for hub_connection in hubs_priority:
                            hub.neighboring_hubs.append(hub_connection)
                        for hub_connection in hubs_normal:
                            hub.neighboring_hubs.append(hub_connection)
                        for hub_connection in hubs_restricted:
                            hub.neighboring_hubs.append(hub_connection)
                        hub.neighboring_hubs_forbiden = hubs_blocked

        # 2/ parcours tous les hubs et trie neighboring_hubs:
        #   par priorite de zone a parcourir
        #   vide la liste des voisins de end_hub
        #   dans tous les hub enleve start_hub
        #   1-end_hub 2-hubs priority 3-hubs normal
        #   4-hubs restricted 5-hubs blocked
        # Sort neighboring_hubs of every hubs in order of priority

    def next_hub(self) -> None:
        """Move Drone to Next Hub"""
        pass

    def dijkstra_algorythm(self) -> None:
        drone: parsing.MapParsing.Drone
        hub_datas: parsing.MapParsing.Hub.HubData
        hub: parsing.MapParsing.Hub
        tempo_travel_plan: list[
            Optional[
                parsing.MapParsing.Hub.HubData | parsing.MapParsing.Connection
            ]
        ]
        turn_num: int
        # Boucle sur tous les Drones un par un:
        #   va au hub voisin suivant par ordre de priorite:
        #       => si deja occupe, boucle jusqu'a ce qu'il soit libre
        #       => si deja emprunte, test le suivant
        #       => si suivant end_hub, compare le nombre de tours effectues,
        #           le cas echeant,
        #           avec le nombre de tours du parcours precedent,
        #           et garde celui qui a le moins de tours,
        #           puis revient un hub en arriere et poursuit la boucle hub
        #       => si tous testes
        #           => si start_hub et pas de chemins trouves: message d'erreur
        #           => si start_hub et chemin trouve, passe au drone suivant
        #           => sinon: revient au hub precedent
        #                     et continue la boucle hub

        # chaque hub et chaque connection contient le numero des Drones
        #   presents par tour (None lorsqu'aucun drone present)
        # Chaque drone contient ses deplacements par tour
        #   (none lorsque pqs de deplacement)

        if self.drone_list is None or self.drone_list == []:
            raise ValueError("There is no drone in the map")

        print("ALGORYTHM:\n")  # TEMPO

        # Boucle sur tous les Drones un par un:
        for drone in self.drone_list:
            tempo_travel_plan = []
            print(f"Traitement drone D{drone.id}")  # TEMPO
            tempo_travel_plan.append(drone.drone_pos)

            # TEMPO
            while drone.drone_pos.type != "end_hub":
                _, _, hub = self.find_hub_by_name(drone.drone_pos.name)
                drone.drone_pos = hub.neighboring_hubs[0][0].datas
                tempo_travel_plan.append(drone.drone_pos)

            drone.travel_plan = tempo_travel_plan
            if (len(drone.travel_plan)) > self.nb_turn:
                self.nb_turn = len(drone.travel_plan)

            # TEMPO
            print(" Parcours:")
            turn_num = 0
            for hub_datas in drone.travel_plan:
                print(f"        turn: {turn_num} => {hub_datas.name}")
                turn_num += 1

    # Prend chaque Drone dans l'ordre et cherche le chemin le plus cours
    #   en fonction du positionnement des autre drones et des zones

    # Chaque hub contient:
    #   - la liste des hub connectes par ordre de priorite
    #   - la liste des drones present a l'instant t (le tour en cours)
    #
    # Chaque connection contient la liste des drones presents
    #   a l'instant t (le tour en cours)
    #
    # Chaque drone contient:
    #   - parcours definie precedement du depart a l'arrivee,
    #       ou None si aucun effectue
    #   - parcours tempo permettant les retours en arrieres
    #     (generalement une copie du parcours en cours
    #       juste avant de faire un retour en arriere d'un hub)
    #   - etat du parcours en cours
    #       (tous les hub traverse et l'emplacement en cours)
    #
    # Deplacement des Drones:
    # While sur tous les drones:
    #   Examine le type de hub connecte a celui en cours dans l'ordre
    #   (cette boucle est effectue jusqu'a ce que
    #       tous les parcours possible aient ete testes):
    #       => si toutes les destinations de ce hub testees:
    #           => si hub_start, la boucle principale est terminee
    #               (tous les parcours ont ete testes):
    #               => si aucun parcours trouve, les tests sont termine,
    #                   un message d'erreur apparait
    #               => sinon: on passe aux tests sur le drone suivant
    #           => sinon: revient un hub en arriere et continue les tests
    #       => Si hub_end:
    #           - s'y deplace
    #           - compare le nombre de tours effectue
    #               avec celui du parcours precedent:
    #               => si moins de tours ou aucun parcours enregistre
    #                   precedement,
    #                   ce parcours est enregistre a la place de l'autre
    #       => Si deja visite ou blocked, passe au test sur le hub suivant
    #       => Si deja occupe, passe les tours jusqu'a ce qu'il soit libre
    #           et s'y deplace

    def drones_manager(self) -> None:
        """Manage Drones Movements"""

        self.sort_hubs_neighbours()
        self.dijkstra_algorythm()


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
