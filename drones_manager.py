import parsing
from typing import Optional


class DronesManager:
    hub_list: list[parsing.MapParsing.Hub]
    connection_list: list[parsing.MapParsing.Connection]

    def find_hub_by_type(self, type: str) -> tuple[
        Optional["parsing.MapParsing.Hub.HubData"],
        Optional["parsing.MapParsing.Hub.HubMeta"],
        Optional["parsing.MapParsing.Hub"],
    ]:
        raise NotImplementedError

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

    # def recov_next_hub(
    #     self,
    #     drone_pos: parsing.MapParsing.Hub.HubData,
    #     hub_visited: list[parsing.MapParsing.Hub.HubData],
    # ) -> Optional[parsing.MapParsing.Hub]:
    #     """Recovery Drone to Next Hub"""
    #     hub: parsing.MapParsing.Hub
    #     for hub in drone_pos.neighboring_hubs:
    #         if hub not in hub_visited:
    #             return hub
    #     return None

    def find_connect(
        self, hub1: parsing.MapParsing.Hub, hub2: parsing.MapParsing.Hub
    ) -> parsing.MapParsing.Connection:
        """Find Connection Between Two Hubs"""
        connection: parsing.MapParsing.Connection

        for connection in self.connection_list:
            if hub1.datas is connection.hub1 and hub2.datas is connection.hub2:
                return connection
            if hub2.datas is connection.hub1 and hub1.datas is connection.hub2:
                return connection
        raise ValueError(
            f"Invalid Connection between {hub1.datas.name} "
            f"and {hub2.datas.name}"
        )

    def allow_time(
        self,
        start: parsing.MapParsing.Hub,
        desti: parsing.MapParsing.Hub,
        start_time: int,
    ) -> int:
        """Notice Next Time when place is allowed"""
        time_allow: int = start_time
        list_drones: Optional[list[parsing.MapParsing.Drone]]
        connection: parsing.MapParsing.Connection
        
        # check if hub is free
        if time_allow >= len(desti.drones_by_time):
            return time_allow

        connection = self.find_connect(start, desti)
        for time_allow in range(time_allow, len(desti.drones_by_time)):
            list_drones = desti.drones_by_time[time_allow]
            if list_drones is None or list_drones == []:
                return time_allow
            elif len(list_drones) < desti.metas.max_drones:
                if (
                    connection.drones_in_connect is None
                    or connection.drones_in_connect == []
                    or len(connection.drones_in_connect)
                    <= time_allow
                ):
                    return time_allow
        time_allow = time_allow + 1
        return time_allow

    def add_drone_in_hub(
        self,
        drone: parsing.MapParsing.Drone,
        dest: parsing.MapParsing.Hub,
        turn_at_dest: int
        ) -> None:

        """Add drone in hub"""
        if turn_at_dest < len(dest.drones_by_time):
            dest.drones_by_time[turn_at_dest].append(drone)
        else:

            for _ in range(len(dest.drones_by_time), turn_at_dest):
                dest.drones_by_time.append(None)
            dest.drones_by_time.append([])
            dest.drones_by_time[turn_at_dest].append(drone)

    def add_drone_in_connect(
        self,
        drone: parsing.MapParsing.Drone,
        connect: parsing.MapParsing.Connection,
        turn_at_dest: int
        ) -> None:

        """Add drone in hub"""
        if turn_at_dest < len(connect.drones_in_connect):
            connect.drones_in_connect[turn_at_dest].append(drone)
        else:

            for _ in range(len(connect.drones_in_connect), turn_at_dest):
                connect.drones_in_connect.append(None)
            connect.drones_in_connect.append([])
            connect.drones_in_connect[turn_at_dest].append(drone)


    def drone_to_dest(
        self,
        drone: parsing.MapParsing.Drone,
        dest: parsing.MapParsing.Hub | parsing.MapParsing.Connection,
        connect: parsing.MapParsing.Connection,
        turn_at_dest: int
        ) -> None:
        """Move Drone to Next Hub"""

        # Add the move in drone travel plan
        if turn_at_dest < len(drone.travel_plan):
            drone.travel_plan[turn_at_dest] = dest
        else:
            for _ in range(len(drone.travel_plan), turn_at_dest):
                drone.travel_plan.append(None)
            drone.travel_plan.append(dest.datas)

        # Add the move in the hub of destination
        self.add_drone_in_hub(drone, dest, turn_at_dest)

        # Add the move in the connection
        self.add_drone_in_connect(drone, connect, turn_at_dest)
            
    def dijkstra_algorythm(self) -> None:
        drone: parsing.MapParsing.Drone
        travel_plan_test: list[
            Optional[
                parsing.MapParsing.Hub.HubData | parsing.MapParsing.Connection
            ]
        ]

        turn: int
        turn_to_dest: int

        desti_hub: parsing.MapParsing.Hub
        connect: parsing.MapParsing.Connection

        start_hub: Optional[parsing.MapParsing.Hub]
        _, _, start_hub = self.find_hub_by_type("start_hub")
        if start_hub is None:
            raise ValueError("There is not start_hub in this map")
        desti_start_hub: parsing.MapParsing.Hub
        conn_start: parsing.MapParsing.Connection

        # - Boucle sur chaque drones de la map un par un dans variable drone
        for drone in self.drone_list:
            travel_plan_test = []
            travel_plan_test.append(start_hub.datas)
            drone.travel_plan.append(start_hub.datas)

            # -     Boucle sur ce drone tant que tous les chemins en partance
            #       de start_hub n'ont pas ete explores
            for desti_start_hub, conn_start in start_hub.neighboring_hubs:
                turn = 1
                turn_at_dest = 1
                turn_at_dest = self.allow_time(start_hub, desti_start_hub, turn)
                self.drone_to_dest(drone, desti_start_hub, conn_start, turn_at_dest)
                turn = turn_at_dest + 1
                self.nb_turn = turn
                


        # -         passe chaque fois au premier hub voisin qui suit

        # -             Si deja occupe => fait des tours jusqu'a ce qu'il soit
        #                                 libere puis s'y place
        # -             Si deja explore, test le hub voisin suivant
        # -             Si tous les hubs voisin explores,
        #               revient un hub en arriere
        # -             si end_hub atteint => sauvegarde ce chemin
        #                                     si c'est le plus court
        #                                     et revient un hub en arriere
        # -     Si aucun chemin sauvegarder pour ce drone => raise
        # -     drone suivant

        # - Boucle sur chaque drones de la map un par un dans variable drone
        # -     Boucle sur ce drone tant que tous les chemins
        #       en partance de start_hub n'ont pas ete explores
        # -         passe chaque fois au premier hub voisin qui suit
        # -             Si deja occupe => fait des tours jusqu'a
        #                                 ce qu'il soit libere puis s'y place
        # -             Si deja explore, test le hub voisin suivant
        # -             Si tous les hubs voisin explores,
        #               revient un hub en arriere
        # -             si end_hub atteint => sauvegarde ce chemin si c'est
        #                                     le plus court et revient
        #                                     un hub en arriere
        # -     Si aucun chemin sauvegarder pour ce drone => raise
        # -     drone suivant

    # def dijkstra_algorythm(self) -> None:
    #     loop_drone: int
    #     loop_hub: int
    #     drone: parsing.MapParsing.Drone
    #     hub_next: Optional[parsing.MapParsing.Hub]
    #     hub_datas: parsing.MapParsing.Hub.HubData
    #     hub: parsing.MapParsing.Hub

    #     tempo_travel_plan: list[Optional[parsing.MapParsing.Hub.HubData]]

    #     turn_num: int
    #     # Boucle sur tous les Drones un par un:
    #     #   va au hub voisin suivant par ordre de priorite:
    #     #       => si deja occupe, boucle jusqu'a ce qu'il soit libre
    #     #       => si deja emprunte, test le suivant
    #     #       => si suivant end_hub, compare le nombre de tours effectues,
    #     #           le cas echeant,
    #     #           avec le nombre de tours du parcours precedent,
    #     #           et garde celui qui a le moins de tours,
    #     #           puis revient un hub en arriere et poursuit la boucle hub
    #     #       => si tous testes
    #     #           => si start_hub et pas de chemins trouves:
    #                    message d'erreur
    #     #           => si start_hub et chemin trouve, passe au drone suivant
    #     #           => sinon: revient au hub precedent
    #     #                     et continue la boucle hub

    #     # chaque hub et chaque connection contient le numero des Drones
    #     #   presents par tour (None lorsqu'aucun drone present)
    #     # Chaque drone contient ses deplacements par tour
    #     #   (none lorsque pqs de deplacement)

    #     if self.drone_list is None or self.drone_list == []:
    #         raise ValueError("There is no drone in the map")

    #     # Boucle sur tous les Drones un par un:
    #     for drone in self.drone_list:
    #         tempo_travel_plan = []
    #         print(f"Traitement drone D{drone.id}")  # TEMPO
    #         tempo_travel_plan.append(drone.drone_pos)

    #         loop_drone = 1
    #         while loop_drone:
    #             # Recovery next hub
    #             hub_next = self.recov_next_hub(
    #                 drone.drone_pos, tempo_travel_plan
    #             )
    #             if hub_next is None:
    #                 loop_drone = 0

    #         # # TEMPO ALGORYTHM
    #         # while drone.drone_pos.type != "end_hub":
    #         #     _, _, hub = self.find_hub_by_name(drone.drone_pos.name)
    #         #     drone.drone_pos = hub.neighboring_hubs[0][0].datas
    #         #     tempo_travel_plan.append(drone.drone_pos)

    #         drone.travel_plan = tempo_travel_plan
    #         if (len(drone.travel_plan)) > self.nb_turn:
    #             self.nb_turn = len(drone.travel_plan)

    #         # # TEMPO
    #         # print(" Parcours:")
    #         # turn_num = 0
    #         # for hub_datas in drone.travel_plan:
    #         #     print(f"        turn: {turn_num} => {hub_datas.name}")
    #         #     turn_num += 1

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

        print("ALGORYTHM:\n")  # TEMPO

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
