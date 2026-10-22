from pydantic import BaseModel, Field, model_validator  # , ValidationError
from typing import Optional
from enum import Enum


class MapParsing:
    def __init__(self) -> None:
        # For check
        self.nb_connections: int = 0
        self.map_clean: list[str] = []
        self.types_used: list[str] = []
        self.name_used: list[str] = []
        self.coord_list: list[tuple[int, int]] = []
        self.connection_check_list: list[list[str]] = []
        self.connection_name_list: list[tuple[list[str], int]] = []

        # Definitive Datas
        self.hub_list: list[MapParsing.Hub] = []
        self.connection_list: list[MapParsing.Connection] = []
        self.drone_list: list[MapParsing.Drone] = []
        self.nb_drones: int = 0
        super().__init__()

    def clean_map(self) -> None:
        """Clean Map Datas"""
        split_tempo: list[str]

        if self.map_text is None or self.map_text == []:
            raise ValueError("No datas read")
        map_list: list[str] = self.map_text.split("\n")
        for one_line in map_list:
            split_tempo = one_line.split("#")
            if len(split_tempo[0]) > 1:
                self.map_clean.append(split_tempo[0])
        if len(self.map_clean) < 6:
            self.map_clean = []
            raise ValueError("Not enough values in the map definition")

    class DatasType(str, Enum):
        nb_drones = "nb_drones"
        start_hub = "start_hub"
        end_hub = "end_hub"
        hub = "hub"
        connection = "connection"

    class Hub:
        def __init__(self, self_map: "MapParsing") -> None:
            self.map: MapParsing = self_map
            self.datas: MapParsing.Hub.HubData
            self.metas: MapParsing.Hub.HubMeta
            self.neighboring_hubs: list[
                tuple["MapParsing.Hub", "MapParsing.Connection"]
            ] = []

        class HubMetaZone(str, Enum):
            normal = "normal"
            blocked = "blocked"
            restricted = "restricted"
            priority = "priority"

        class HubData(BaseModel):
            name: str = Field(min_length=1)
            coordX: int
            coordY: int
            type: str
            drones_in_hub: list["MapParsing.Drone"] = Field(
                default_factory=list
            )
            nb_drones: int = Field(default=0, ge=0)

            @model_validator(mode="after")
            def hub_datas_validation(self) -> "MapParsing.Hub.HubData":
                if "-" in self.name or " " in self.name:
                    raise ValueError(
                        "The name must not countain: '-', '_' or ' '"
                    )
                return self

        class HubMeta(BaseModel):
            zone_type: str = Field(default="normal")
            color: Optional[str] = Field(default=None)
            max_drones: int = Field(default=1, ge=0)

            @model_validator(mode="after")
            def hub_meta_validation(self) -> "MapParsing.Hub.HubMeta":
                if self.zone_type not in [
                    e.value for e in MapParsing.Hub.HubMetaZone
                ]:
                    raise ValueError(
                        f"{self.zone_type} " "is not a conform type of zone"
                    )
                return self

        def check_hub_datas(
            self, string: str, type: str
        ) -> "MapParsing.Hub.HubData":
            """Check if hub Datas are Conform"""
            datas_str: str = self.map.recup_datas_only(string)
            datas: MapParsing.Hub.HubData

            datas_separate: list[str] = datas_str.split(" ")

            if not len(datas_separate) == 3:
                raise ValueError(
                    f"{datas_separate} is not conform"
                    ", it must be countain 3 datas"
                )
            datas = self.HubData(
                name=datas_separate[0],
                coordX=int(datas_separate[1]),
                coordY=int(datas_separate[2]),
                type=type,
            )
            if datas.name in self.map.name_used:
                raise ValueError(f"This name: {datas.name} is already used")
            if (datas.coordX, datas.coordY) in self.map.coord_list:
                raise ValueError(
                    f"Coordinates: {datas.coordX}, "
                    f"{datas.coordY} is already used"
                )

            self.map.name_used.append(datas.name)
            self.map.coord_list.append((datas.coordX, datas.coordY))

            return datas

        def check_hub_metas(self, string: str) -> "MapParsing.Hub.HubMeta":
            """Check if hub Meta is Conform"""
            split_tempo: list[str]
            metas_str: str = self.map.recup_meta_only(string)
            metas: MapParsing.Hub.HubMeta

            zone_type_str: str = "normal"
            color_str: str | None = None
            max_drones_str: str = "1"
            zone_type_check: bool = False
            color_check: bool = False
            max_drones_check: bool = False

            if not metas_str == "[]":
                metas_separate: list[str] = metas_str.split(" ")

                if len(metas_separate) > 3:
                    raise ValueError(
                        f"{metas_separate} is not conform, "
                        "it must be countain 3 metadatas maximum"
                    )
                for e in metas_separate:
                    split_tempo = e.split("=")
                    if not len(split_tempo) == 2:
                        raise ValueError(
                            f"{e} is not conform metadata for hub"
                        )
                    if split_tempo[0] == "zone" and zone_type_check is False:
                        zone_type_str = split_tempo[1]
                        zone_type_check = True

                    elif split_tempo[0] == "color" and color_check is False:
                        color_str = split_tempo[1]
                        color_check = True

                    elif (
                        split_tempo[0] == "max_drones"
                        and max_drones_check is False
                    ):
                        max_drones_str = split_tempo[1]
                        max_drones_check = True

                    elif split_tempo[0] is not None:
                        raise ValueError(
                            f"{e} is not conform metadata for hub"
                        )
            if max_drones_str is None:
                max_drones_str = "1"
            metas = MapParsing.Hub.HubMeta(
                zone_type=zone_type_str,
                color=color_str,
                max_drones=int(max_drones_str),
            )

            return metas

        def check_hub(self, line: str, type: str) -> None:
            """Check hub and create list of hubs"""
            self.datas = self.check_hub_datas(line, type)
            self.metas = self.check_hub_metas(line)
            if type == "start_hub":
                self.datas.nb_drones = self.map.nb_drones
            self.map.hub_list.append(self)

    class Drone(BaseModel):
        id: int
        hub_pos: "MapParsing.Hub.HubData | MapParsing.Connection"
        positioning_log: list["MapParsing.Hub.HubData | MapParsing.Connection"]

    class Connection(BaseModel):
        id: int
        hub1: "MapParsing.Hub.HubData"
        hub2: "MapParsing.Hub.HubData"
        nb_drones_in: int = Field(default=0, ge=0)
        drones_in_connect: list["MapParsing.Drone"] = Field(
            default_factory=list
        )
        max_drones_allow: int = Field(default=1, ge=0)

        @model_validator(mode="after")
        def Connection(self) -> "MapParsing.Connection":
            if self.nb_drones_in > self.max_drones_allow:
                raise ValueError(
                    f"{self.nb_drones_in} drones is too high, "
                    f"you can have more than {self.max_drones_allow}"
                    "in this connection"
                )
            return self

    def check_type(self, line: str) -> str:
        """Check and Return type or a raise"""
        type_split: list[str]

        if line is None:
            raise ValueError("There is no line in argument")
        type_split = line.split(":")
        if len(type_split) != 2:
            raise ValueError("There is no type argument identifiable")
        if type_split[0] not in [c.value for c in self.DatasType]:
            raise ValueError(f"'{type_split[0]}' is not correct type")
        if type_split[0] in self.types_used:
            raise ValueError(f"'{type_split[0]}' is used several times")

        if (
            type_split[0] == "nb_drones"
            or type_split[0] == "start_hub"
            or type_split[0] == "end_hub"
        ):
            self.types_used.append(type_split[0])

        return type_split[0]

    def recup_datas_only(self, string: str) -> str:
        """Return Datas String of a String"""
        split_tempo: list[str]

        if string is None:
            raise ValueError("There is no string in argument")
        split_tempo = string.split(" [")
        split_tempo = split_tempo[0].split(": ")
        if not len(split_tempo) == 2:
            raise ValueError("String not conform")

        return split_tempo[1]

    def recup_meta_only(self, string: str) -> str:
        """Return Metadata String of a String"""
        split_tempo: list[str]
        meta: str = "[]"

        if string is not None and not len(string) == 0:
            split_tempo = string.split("[")
            if len(split_tempo) > 2:
                raise ValueError("Too many MetaDatas")
            elif len(split_tempo) == 2:
                tuple_tempo = split_tempo[1].split("]")
                if len(tuple_tempo) != 2:
                    raise ValueError("Definition of MetaDatas is not conform")
                meta = tuple_tempo[0]

        return meta

    def normalise_connection(self, line: str) -> tuple[str, str]:
        """Separate Datas and Metadatas in 2 Strings"""
        datas: str
        meta: str

        meta = self.recup_meta_only(line)
        if meta == "[]":
            meta = "max_link_capacity=1"
        datas = self.recup_datas_only(line)

        return datas, meta

    def check_connection_meta(self, meta: str) -> int:
        """Check Meta Datas"""
        split_tempo: list[str]
        number: int

        if meta is None or len(meta) == 0:
            raise ValueError("No metadata given for checking")
        split_tempo = meta.split("=")
        if not len(split_tempo) == 2:
            raise ValueError(f"{meta} don't have good quantites of datas")
        elif not split_tempo[0] == "max_link_capacity":
            raise ValueError(
                f"{split_tempo[0]} " "if not a conform metadata for connection"
            )
        number = int(split_tempo[1])
        if number < 1:
            raise ValueError(
                f"Connection {split_tempo[0]} "
                "cant't be have {number} of capacity"
            )
        return number

    def check_connection_datas(self, line: str) -> None:
        """Check Datas of Connections"""
        split_tempo: list[str]
        datas: str
        meta: str

        qty_connections: int

        if line is None:
            raise ValueError("There is no line in argument")

        datas, meta = self.normalise_connection(line)
        qty_connections = self.check_connection_meta(meta)

        # Check if Valid Datas and Doublons
        split_tempo = datas.split("-")
        if not len(split_tempo) == 2:
            raise ValueError("Connection Datas are not valid")
        if split_tempo in self.connection_check_list:
            raise ValueError(f"{split_tempo} is a doublon in Connection Datas")
        self.connection_check_list.append(split_tempo)
        self.connection_check_list.append([split_tempo[1], split_tempo[0]])
        self.connection_name_list.append((split_tempo, qty_connections))

    def check_connections_list(self) -> None:
        """Check if Each Connection Exist"""
        for connection in self.connection_check_list:
            if (
                not connection[0] in self.name_used
                and not connection[1] in self.name_used
            ):
                raise ValueError(f"Connection {connection} does not exist")
            elif not connection[0] in self.name_used:
                raise ValueError(
                    f"In connection {connection}: "
                    f"{connection[0]} does not exist"
                )
            elif not connection[1] in self.name_used:
                raise ValueError(
                    f"In connection {connection}: "
                    f"{connection[1]} does not exist"
                )

    def find_hub_by_name(self, name: str) -> tuple[
        Optional["MapParsing.Hub.HubData"],
        Optional["MapParsing.Hub.HubMeta"],
        Optional["MapParsing.Hub"],
    ]:
        """Return hub with name"""
        for hub in self.hub_list:
            if hub.datas.name == name:
                return hub.datas, hub.metas, hub
        return (None, None, None)

    def find_hub_by_type(self, type: str) -> tuple[
        Optional["MapParsing.Hub.HubData"],
        Optional["MapParsing.Hub.HubMeta"],
        Optional["MapParsing.Hub"],
    ]:
        """Return hub with name"""
        for hub in self.hub_list:
            if hub.datas.type == type:
                return hub.datas, hub.metas, hub
        return (None, None, None)

    def find_hub_by_name2(self, name: str) -> Optional["MapParsing.Hub"]:
        """Return hub with name"""
        for hub in self.hub_list:
            if hub.datas.name == name:
                return hub
        return None

    def find_hub_by_type2(self, type: str) -> Optional["MapParsing.Hub"]:
        """Return hub with name"""
        for hub in self.hub_list:
            if hub.datas.type == type:
                return hub
        return None

    def create_connection_list(self) -> None:
        """Create list of connection by hub"""
        huba: Optional[MapParsing.Hub.HubData]
        hubb: Optional[MapParsing.Hub.HubData]
        connect: MapParsing.Connection

        if (
            self.connection_name_list == []
            or self.connection_name_list is None
        ):
            raise ValueError("There is not connection defined")

        for connection in self.connection_name_list:
            huba, _, _ = self.find_hub_by_name(connection[0][0])
            hubb, _, _ = self.find_hub_by_name(connection[0][1])
            if huba is None or hubb is None:
                raise ValueError("Connections list is not conform")
            self.nb_connections += 1
            connect = self.Connection(
                id=self.nb_connections,
                hub1=huba,
                hub2=hubb,
                max_drones_allow=connection[1],
            )
            self.connection_list.append(connect)

    def create_drone_list(self) -> None:
        """Create list of drones"""
        hub_start: Optional[MapParsing.Hub.HubData]
        new_drone: MapParsing.Drone

        hub_start, _, _ = self.find_hub_by_type("start_hub")
        for n in range(self.nb_drones):
            new_drone = self.Drone(
                id=n + 1, hub_pos=hub_start, positioning_log=[hub_start]
            )
            self.drone_list.append(new_drone)
            hub_start.drones_in_hub.append(new_drone)

    def init_neighboring_hubs(self) -> None:
        """Init List of Neighbors"""
        connection: MapParsing.Connection

        # 1/ parcours la liste de connection et place chaque connection
        #   et hub correspondand dans neighboring_hubs
        for connection in self.connection_list:
            pass
        # 2/ parcours tous les hubs et trie neighboring_hubs,
        #   par priorite de zone a parcourir
        pass

    def map_parsing(self) -> None:
        """Parsing of All the Map"""
        split_tempo: list[str]
        type: Optional[str] = None

        self.clean_map()
        for i in range(len(self.map_clean)):
            type = self.check_type(self.map_clean[i])

            if i == 0:
                # CHeck first line
                if not type == "nb_drones":
                    raise ValueError(
                        f"The first type is '{type}' "
                        "but it should have been 'nb_drones'"
                    )
                split_tempo = self.map_clean[i].split(":")
                # if not len(tuple_tempo) == 2:
                #     raise ValueError(f"Definition of {type} is not valid")
                self.nb_drones = int(split_tempo[1])
                if self.nb_drones < 1:
                    raise ValueError(
                        f"{self.nb_drones} is not "
                        "a valid quantite of drones"
                    )

                continue

            elif type == "connection":
                self.check_connection_datas(self.map_clean[i])
            else:
                hub: MapParsing.Hub = self.Hub(self)
                hub.check_hub(self.map_clean[i], type)

        self.check_connections_list()
        self.create_connection_list()
        self.create_drone_list()
        self.init_neighboring_hubs()


# Modifier affichage des donnees dans le terminal pour etre conforme au sujet
