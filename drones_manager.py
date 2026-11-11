import parsing
from typing import Optional


class DronesManager:
    nb_turn: int
    hub_list: list[parsing.MapParsing.Hub]
    connection_list: list[parsing.MapParsing.Connection]

    def find_hub_by_type(self, type: str) -> tuple[
        Optional["parsing.MapParsing.Hub.HubData"],
        Optional["parsing.MapParsing.Hub.HubMeta"],
        Optional["parsing.MapParsing.Hub"],
    ]:
        raise NotImplementedError

    def find_hub_by_name(self, name: str) -> tuple[
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

    # def delete_last_drone_move(
    #     self,
    #     drone: parsing.MapParsing.Drone,
    #     connect: parsing.MapParsing.Connection,
    # ) -> None:
    #     """Delete Move of Drone at a turn"""
    #     turn: int = len(drone.travel_plan) - 1
    #     drone_pos: (
    #         parsing.MapParsing.Hub.HubData | parsing.MapParsing.Connection
    #     )
    #     hub: parsing.MapParsing.Hub | None

    #     drone_list: Optional[list[parsing.MapParsing.Drone]]

    #     drone_pos = drone.drone_pos

    #     # Delete of Hub
    #     if isinstance(drone_pos, parsing.MapParsing.Hub.HubData):
    #         _, _, hub = self.find_hub_by_name(drone_pos.name)
    #         # CHECK mypy
    #         if (
    #             isinstance(hub, parsing.MapParsing.Hub)
    #             and len(hub.drones_by_time) > turn
    #         ):
    #             drone_list = hub.drones_by_time[turn]
    #             if isinstance(drone_list, list):

    #                 # TEMPO
    #                 if drone.id == 7 and turn == 5:
    #                     print(f"DELETE D7 - Connection {id(connect)}")
    #                 # drone_list.remove(drone)
    #                 self.safe_remove(
    #                     drone_list, drone, f"Connection, tour {turn}"
    #                 )
    #         # TEMPO
    #         if drone.id == 7 and turn == 5:
    #             print(
    #                 f"PARAMETRE : {id(connect)} | "
    #                 f"POSITION : {id(drone_pos)}"
    #             )
    #     else:

    #         # TEMPO
    #         print(
    #             f"AVANT : {id(connect)} | "
    #             f"APRES : {id(drone_pos)}"
    #         )

    #         connect = drone_pos

    #     # Delete of Connection
    #     if len(connect.drones_in_connect) > turn:
    #         drone_list = connect.drones_in_connect[turn]
    #         if isinstance(drone_list, list):

    #             # TEMPO
    #             if drone.id == 7 and turn == 5:
    #                 print(f"DELETE D7 - Connection {id(connect)}")
    #             # drone_list.remove(drone)
    #             self.safe_remove(drone_list, drone, f"Connection, tour {turn}")

    #     # Delete of travel_plan
    #     drone.travel_plan.remove(drone_pos)

    def delete_last_drone_move(
        self,
        drone: parsing.MapParsing.Drone,
        connect: parsing.MapParsing.Connection,
    ) -> None:
        """Delete Move of Drone at a turn"""
        turn: int = len(drone.travel_plan) - 1
        drone_pos: (
            parsing.MapParsing.Hub.HubData | parsing.MapParsing.Connection
        )
        hub: parsing.MapParsing.Hub | None

        drone_list: Optional[list[parsing.MapParsing.Drone]]

        drone_pos = drone.drone_pos

        # Delete of Hub
        if isinstance(drone_pos, parsing.MapParsing.Hub.HubData):
            _, _, hub = self.find_hub_by_name(drone_pos.name)
            # CHECK mypy
            if (
                isinstance(hub, parsing.MapParsing.Hub)
                and len(hub.drones_by_time) > turn
            ):
                drone_list = hub.drones_by_time[turn]
                if isinstance(drone_list, list):
                    drone_list.remove(drone)
        else:
            connect = drone_pos

        # Delete of Connection
        if len(connect.drones_in_connect) > turn:
            drone_list = connect.drones_in_connect[turn]
            if isinstance(drone_list, list):
                drone_list.remove(drone)

        # Delete of travel_plan
        drone.travel_plan.remove(drone_pos)

    def update_hubs_connections(self, drone: parsing.MapParsing.Drone) -> None:
        """Update Moves Drone in Every Hubs and Connections"""
        turn: int
        hub: parsing.MapParsing.Hub | None
        connection: parsing.MapParsing.Connection
        last_pos: parsing.MapParsing.Hub | None

        dest: (
            parsing.MapParsing.Hub.HubData
            | parsing.MapParsing.Connection
            | None
        )

        _, _, last_pos = self.find_hub_by_type("start_hub")

        for turn in range(1, len(drone.best_travel_plan)):
            dest = drone.best_travel_plan[turn]

            if dest is None and isinstance(last_pos, parsing.MapParsing.Hub):
                # Add Drone in present Hub for Turn without Move
                self.add_drone_in_hub(drone, last_pos, turn)

            elif isinstance(
                dest, parsing.MapParsing.Hub.HubData
            ) and isinstance(last_pos, parsing.MapParsing.Hub):
                _, _, hub = self.find_hub_by_name(dest.name)

                # CHECK mypy
                if isinstance(hub, parsing.MapParsing.Hub):
                    self.add_drone_in_hub(drone, hub, turn)
                    connection = self.find_connect(hub, last_pos)
                last_pos = hub
                self.add_drone_in_connect(drone, connection, turn)

            elif isinstance(dest, parsing.MapParsing.Connection):
                connection = dest
                self.add_drone_in_connect(drone, connection, turn)

    def allow_time(
        self,
        connect: parsing.MapParsing.Connection,
        desti: parsing.MapParsing.Hub,
        start_time: int,
    ) -> int:
        """Notice Next Time when place is allowed"""
        turn_at_dest: int = start_time
        turn_at_connect: int
        list_drones: Optional[list[parsing.MapParsing.Drone]]
        # Calcul l'instant ou desti est libre:

        if desti.metas.zone_type == "restricted":
            turn_at_dest = turn_at_dest + 1

        # Check if turn_at_dest is already exist
        if len(desti.drones_by_time) > turn_at_dest:
            for turn_at_dest in range(
                turn_at_dest, (len(desti.drones_by_time))
            ):
                list_drones = desti.drones_by_time[turn_at_dest]
                if (
                    list_drones is not None
                    and list_drones != []
                    and len(list_drones) == desti.metas.max_drones
                ):
                    continue

                if desti.metas.zone_type == "restricted":
                    turn_at_connect = turn_at_dest - 1
                else:
                    turn_at_connect = turn_at_dest

                # Check if drones_in_connect is already exist
                if len(connect.drones_in_connect) > turn_at_connect:
                    list_drones = connect.drones_in_connect[turn_at_connect]
                    if (
                        list_drones is not None
                        and list_drones != []
                        and len(list_drones) == desti.metas.max_drones
                    ):
                        continue

                return turn_at_dest

            return turn_at_dest + 1

        return turn_at_dest

        # si desti est de type restricted
        #   => turn_at_dest = turn_at_dest + 1

        # si len(desti.drones_by_time) > turn_at_dest
        # si la destination compte au moins le meme nombre de tour qu'au start_time:
        #   - incremente turn_at_dest jusqu'a trouver un tour ou desti est libre:
        #           - si place restante suffisente pour placer un nouveau drone
        #           - si connection libre a cet instant ou a l'instant d'avant si desti est restricted

    def add_drone_in_connect(
        self,
        drone: parsing.MapParsing.Drone,
        connect: parsing.MapParsing.Connection,
        turn_at_connect: int,
    ) -> None:
        """Add Drone in Drone list of the Connection"""
        last_turn: int = len(connect.drones_in_connect) - 1
        drone_list: list[parsing.MapParsing.Drone] | None

        # Init connect
        if last_turn < turn_at_connect:
            for _ in range(last_turn, turn_at_connect):
                connect.drones_in_connect.append(None)

        if connect.drones_in_connect[turn_at_connect] is None:
            connect.drones_in_connect[turn_at_connect] = []

        drone_list = connect.drones_in_connect[turn_at_connect]
        # CHECK mypy
        if isinstance(drone_list, list):
            drone_list.append(drone)

    def add_drone_in_hub(
        self,
        drone: parsing.MapParsing.Drone,
        hub_dest: parsing.MapParsing.Hub,
        turn_at_dest: int,
        turn_at_start: int,
    ) -> None:
        """Add Drone In Hubs concerning by a Move"""

        hub_start: parsing.MapParsing.Hub
        last_turn: int
        turn_update: int
        count: int

        turn_update = turn_at_dest
        if hub_dest.metas.zone_type == "restricted":
            turn_update -= 1

        # Update Drone list in hub_start before moving
        if isinstance(drone.drone_pos, parsing.MapParsing.Hub.HubData):
            _, _, hub_start = self.find_hub_by_name(drone.drone_pos.name)
            last_turn = len(hub_start.drones_by_time) - 1
            if last_turn < (turn_at_dest - 1):
                for _ in range(last_turn, (turn_at_dest - 1)):
                    hub_start.drones_by_time.append([])
            for count in range((turn_at_start + 1), turn_update):
                hub_start.drones_by_time[count].append(drone)

        # Update Drone list in hub_dest
        last_turn = len(hub_dest.drones_by_time) - 1
        if last_turn < (turn_at_dest):
            for _ in range(last_turn, turn_at_dest):
                hub_dest.drones_by_time.append([])
        hub_dest.drones_by_time[turn_at_dest].append(drone)

        # - Mettre a jour la presence du drone dans le hub actuel
        #   entre turn actuel et turn_at_dest
        # - Mettre le drone dans dest a turn_at_dest

    def drone_to_dest(
        self,
        drone: parsing.MapParsing.Drone,
        dest: parsing.MapParsing.Hub,
        connect: parsing.MapParsing.Connection,
        turn_at_dest: int,
    ) -> None:
        """Move Drone to Next Hub"""
        last_turn_plan: int = len(drone.travel_plan) - 1
        turn_at_connect: int = turn_at_dest

        # Init best_travel_plan
        if last_turn_plan < turn_at_dest:
            for _ in range(last_turn_plan, turn_at_dest):
                drone.travel_plan.append(None)

        if dest.metas.zone_type == "restricted":
            turn_at_connect -= 1
            drone.travel_plan[turn_at_connect] = connect

        drone.travel_plan[turn_at_dest] = dest.datas

        self.add_drone_in_connect(
            drone,
            connect,
            turn_at_connect,
        )

        self.add_drone_in_hub(
            drone,
            dest,
            turn_at_dest,
            last_turn_plan,
        )

        drone.drone_pos = dest.datas

        # Uploaded drone.best_travel
        last_turn = len(drone.travel_plan)
        if last_turn < turn_at_dest:
            for _ in range(last_turn, turn_at_dest):
                drone.travel_plan.append(None)
        drone.travel_plan[turn_at_dest] = dest.datas

        # Mettre des None dans drone.best_travel_plan entre
        # le tour actuel et le turn_at_dest inculs

        # Si dest est restricted zone:
        #   => turn_at_connect = turn_at_dest - 1
        #   => Mettre connect dans drone.travel_plan a turn_at_connect

        # Mettre le drone dans connect a turn_at_connect

        # Mettre le dronnes dans les hubs: add_drone_in_hub

        # Mettre dest.datas dans drone.travel_plan a turn_at_dest

    def delete_drone_presence(
        self,
        drone: parsing.MapParsing.Drone,
        hub: parsing.MapParsing.Hub,
        connect: parsing.MapParsing.Connection | None,
        turn_start: int,
    ) -> None:
        """Delete presence of Drone in hub and connect from turn_at_start"""
        turn_end: int
        count: int

        # Delete from hub
        if isinstance(hub, parsing.MapParsing.Hub):
            turn_end = len(hub.drones_by_time)
            for count in range(turn_start, turn_end):
                if (
                    isinstance(hub.drones_by_time[count], list)
                    and drone in hub.drones_by_time[count]
                ):
                    hub.drones_by_time[count].remove(drone)

        # Delete from Connection
        if isinstance(connect, parsing.MapParsing.Connection):
            turn_end = len(connect.drones_in_connect)
            for count in range(turn_start, turn_end):
                if (
                    isinstance(connect.drones_in_connect[count], list)
                    and drone in connect.drones_in_connect[count]
                ):
                    connect.drones_in_connect[count].remove(drone)

    #TEMPO
    def state_of_hubs(self):
        for hub in self.hub_list:
            print(f"{hub.datas.name}:")
            for drone in hub.drones_by_time:
                if isinstance(drone, list):
                    for dronedrone in drone:
                        print(f"    D{dronedrone.id}")

    def find_best_path(self, drone: parsing.MapParsing.Drone) -> bool:
        #     """Find Best Path for One Drone Recursivly"""
        travel_plan: list[
            parsing.MapParsing.Hub.HubData
            | parsing.MapParsing.Connection
            | None
        ]
        neighboring_hubs: list[
            tuple[parsing.MapParsing.Hub, parsing.MapParsing.Connection]
        ] = []

        drone_pos: parsing.MapParsing.Hub | None
        hubs_visited: list[
            Optional[
                parsing.MapParsing.Hub.HubData | parsing.MapParsing.Connection
            ]
        ] = list(drone.travel_plan)

        end_hub: parsing.MapParsing.Hub | None
        dest: parsing.MapParsing.Hub
        connection: parsing.MapParsing.Connection
        turn: int
        turn_at_dest: int

        # Save state
        turn = len(drone.travel_plan)
        turn_at_dest = len(drone.travel_plan)
        # check mypy
        if isinstance(drone.drone_pos, parsing.MapParsing.Hub.HubData):
            _, _, drone_pos = self.find_hub_by_name(drone.drone_pos.name)
        travel_plan = list(drone.travel_plan)

        # check mypy
        if isinstance(drone_pos, parsing.MapParsing.Hub):
            neighboring_hubs = drone_pos.neighboring_hubs

        _, _, end_hub = self.find_hub_by_type("end_hub")

        if drone_pos is end_hub:

            if (
                drone.best_travel_plan is None
                or drone.best_travel_plan == []
                or len(drone.best_travel_plan) == 0
                or len(drone.travel_plan) < len(drone.best_travel_plan)
            ):
                drone.best_travel_plan = list(drone.travel_plan)
        else:
            for dest, connection in neighboring_hubs:

                # Check if Hub already visited
                if dest.datas in hubs_visited:
                    continue

                hubs_visited.append(dest.datas)

                turn_at_dest = self.allow_time(connection, dest, turn)

                self.drone_to_dest(drone, dest, connection, turn_at_dest)

                self.find_best_path(drone)

                self.delete_drone_presence(
                    drone, drone_pos, connection, (len(travel_plan))
                )
                self.delete_drone_presence(drone, dest, None, len(travel_plan))
                drone.drone_pos = drone_pos.datas
                drone.travel_plan = list(travel_plan)

        # GERER LES MISES A JOURS LORS DU RETOUR EN ARRIERE DES DRONES
        # GERER LA PRESENCE DANS UN HUB D'UN DRONE QUI NE BOUGE PAS

        #       - Sauvegarde etat actuel en local:
        #               - nbr de tours
        #               - position
        #               - travel plan

        # Si pos Drone == end_hub:
        #   => si drone.best_travel_plan vide ou plus grand que drone.travel_plan
        #           => copie drone.travel_plan dans drone.best_travel_plan
        #      Replace drone un hub en arriere

        # Sinon:
        #   => Boucle jusqu'a exploration de tous les voisins:
        #       - Determine le prochain hub en examinant
        #         tout ce qui a deja ete exploré depuis cette recusivitee
        #       - Sauvegarde ce nouveau deplacement en local dans la liste des hubs visites
        #       - Compte le nombre de tour jusqu'a ce que le hub soit libre
        #         (en prenant en compte si c'est une restricted zone)
        #       - Deplace le drone sur le nouveau hub (en prenant en compte si c'est une restricted zone)
        #       - find_best_path sur la prochaine destination
        #       - retablie l'etat de depart de la boucle au niveau:
        #               - nbr de tours
        #               - position
        #               - travel plan
        #
        if drone.best_travel_plan is None or drone.best_travel_plan == []:
            return False

        # self.update_datas_drone_travel(drone)

        return True

    def update_datas_drone_travel(
        self, drone: parsing.MapParsing.Drone
    ) -> None:
        """Update datas of Hubs and Connects by Drone Travel"""
        area: (
            parsing.MapParsing.Hub.HubData
            | parsing.MapParsing.Connection
            | None
        )

        hub_before: parsing.MapParsing.Hub | None
        hub: parsing.MapParsing.Hub | None
        connect: parsing.MapParsing.Connection
        n: int = 0

        _, _, hub_before = self.find_hub_by_type("start_hub")
        for area in drone.best_travel_plan:
            if isinstance(area, parsing.MapParsing.Hub.HubData):
                _, _, hub = self.find_hub_by_name(area.name)
                while len(hub.drones_by_time) < (n + 1):
                    hub.drones_by_time.append(None)
                if hub.drones_by_time[n] is None:
                    hub.drones_by_time[n] = []
                hub.drones_by_time[n].append(drone)
                if (
                    hub.metas.zone_type != "restricted"
                    and hub.datas.type != "start_hub"
                ):
                    connect = self.find_connect(hub_before, hub)
                    self.add_drone_in_connect(drone, connect, n)
                hub_before = hub

            elif hub is not None:
                while len(hub.drones_by_time) < (n + 1):
                    hub.drones_by_time.append(None)
                if hub.drones_by_time[n] is None:
                    hub.drones_by_time[n] = []
                hub.drones_by_time[n].append(drone)

            elif isinstance(area, parsing.MapParsing.Connection):
                self.add_drone_in_connect(drone, area, n)
                hub = None

            n += 1

    def backtracking_algo(self) -> None:
        """Define Best travel for Every Drone of the Map"""
        drone: parsing.MapParsing.Drone
        start_hub: parsing.MapParsing.Hub | None

        _, _, start_hub = self.find_hub_by_type("start_hub")
        # Test tous les chemins possibles de start a end en conservant
        # le meilleurs a chaque fois

        # Boucle sur tous les drones
        for drone in self.drone_list:
            #   Boucle sur tous les itineraires recursivement
            #   en sauvegardant toujours le plus court

            # check mypy
            # Initialising travel_plan of Drone
            if isinstance(start_hub, parsing.MapParsing.Hub):
                drone.travel_plan.append(start_hub.datas)

            if self.find_best_path(drone) is False:
                raise ValueError("There is not path to end_hub")

            # Mise a jour du nombre de tour:
            #   => si taille de drone.best_travel_plan > self.nb_turn
            #       self.nb_turn = drone.travel_plan
            if len(drone.best_travel_plan) > self.nb_turn:
                self.nb_turn = len(drone.best_travel_plan)

            # self.update_hubs_connections(drone)
            # self.update_datas_drone_travel(drone)
            self.update_datas_drone_travel(drone)

    def drones_manager(self) -> None:
        """Manage Drones Movements"""

        self.sort_hubs_neighbours()

        print("ALGORYTHM:\n")  # TEMPO

        # self.dijkstra_algorythm()

        self.backtracking_algo()


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
