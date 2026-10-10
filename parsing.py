from pydantic import BaseModel, Field, model_validator  # , ValidationError
from typing import Optional
from enum import Enum


class MapParsing:
    def __init__(self) -> None:
        # For check
        self.map_clean: list[str] = []
        self.types_used: list[str] = []
        self.name_used: list[str] = []
        self.coord_list: list[tuple[int, int]] = []
        self.connection_check_list: list[tuple[str, str]] = []
        self.connection_name_list: list[tuple[tuple[str, str], int]] = []

        # Definitive Datas
        self.hub_list: list[tuple[MapParsing.HubData, MapParsing.HubMeta]] = []
        self.connection_list: list[
            tuple[tuple[MapParsing.HubData, MapParsing.HubData], int]
        ] = []
        self.nb_drones: int = 0
        super().__init__()

    def clean_map(self) -> None:
        """Clean Map Datas"""
        if self.map_text is None or self.map_text == []:
            raise ValueError("No datas read")
        map_list: list[str] = self.map_text.split("\n")
        for one_line in map_list:
            tuple_tempo = one_line.split("#")
            if len(tuple_tempo[0]) > 1:
                self.map_clean.append(tuple_tempo[0])
        if len(self.map_clean) < 6:
            self.map_clean = []
            raise ValueError("Not enough values in the map definition")

    class DatasType(str, Enum):
        nb_drones = "nb_drones"
        start_hub = "start_hub"
        end_hub = "end_hub"
        hub = "hub"
        connection = "connection"

    class HubMetaZone(str, Enum):
        normal = "normal"
        blocked = "blocked"
        restricted = "restricted"
        priority = "priority"

    # Tester conformiter d'une couleur (couleur existente,
    # definition de la couleur en un seul mot)
    class HubMeta(BaseModel):
        zone_type: Optional[str] = Field(default="normal")
        color: Optional[str] = Field(default=None)
        max_drones: int = Field(default=1, ge=0)

        @model_validator(mode="after")
        def hub_meta_validation(self) -> "MapParsing.HubData":
            if self.zone_type not in [e.value for e in MapParsing.HubMetaZone]:
                raise ValueError(
                    f"{self.zone_type} " "is not a conform type of zone"
                )
            return self

    class HubData(BaseModel):
        name: str = Field(min_length=1)
        coordX: int
        coordY: int
        type: str
        nb_drones: int = Field(default=0, ge=0)

        @model_validator(mode="after")
        def hub_datas_validation(self) -> "MapParsing.HubData":
            if "-" in self.name or " " in self.name:
                raise ValueError("The name must not countain: '-', '_' or ' '")
            return self

    def check_type(self, line: str) -> str:
        """Check and Return type or a raise"""
        if line is None:
            raise ValueError("There is no line in argument")
        type_tuple: tuple[str, str] = line.split(":")
        if len(type_tuple) != 2:
            raise ValueError("There is no type argument identifiable")
        if type_tuple[0] not in [c.value for c in self.DatasType]:
            raise ValueError(f"'{type_tuple[0]}' is not correct type")
        if type_tuple[0] in self.types_used:
            raise ValueError(f"'{type_tuple[0]}' is used several times")

        if (
            type_tuple[0] == "nb_drones"
            or type_tuple[0] == "start_hub"
            or type_tuple[0] == "end_hub"
        ):
            self.types_used.append(type_tuple[0])

        return type_tuple[0]

    def recup_datas_only(self, string: str) -> str:
        """Return Datas String of a String"""
        tuple_tempo: tuple

        if string is None:
            raise ValueError("There is no string in argument")
        tuple_tempo = string.split(" [")
        tuple_tempo = tuple_tempo[0].split(": ")
        if not len(tuple_tempo) == 2:
            raise ValueError("String not conform")

        return tuple_tempo[1]

    def recup_meta_only(self, string: str) -> str:
        """Return Metadata String of a String"""
        tuple_tempo: tuple
        meta: str = "[]"

        if string is not None and not len(string) == 0:
            tuple_tempo = string.split("[")
            if len(tuple_tempo) > 2:
                raise ValueError("Too many MetaDatas")
            elif len(tuple_tempo) == 2:
                tuple_tempo = tuple_tempo[1].split("]")
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
        tuple_tempo: tuple[str, str]
        number: int

        if meta is None or len(meta) == 0:
            raise ValueError("No metadata given for checking")
        tuple_tempo = meta.split("=")
        if not len(tuple_tempo) == 2:
            raise ValueError(f"{meta} don't have good quantites of datas")
        elif not tuple_tempo[0] == "max_link_capacity":
            raise ValueError(
                f"{tuple_tempo[0]} " "if not a conform metadata for connection"
            )
        number = int(tuple_tempo[1])
        if number < 1:
            raise ValueError(
                f"Connection {tuple_tempo[0]} "
                "cant't be have {number} of capacity"
            )
        return number

    def check_connection_datas(self, line: str) -> None:
        """Check Datas of Connections"""
        tuple_tempo: tuple[str, str]
        datas: str
        meta: str

        qty_connections: int

        if line is None:
            raise ValueError("There is no line in argument")

        datas, meta = self.normalise_connection(line)
        qty_connections = self.check_connection_meta(meta)

        # Check if Valid Datas and Doublons
        tuple_tempo = tuple(datas.split("-"))
        if not len(tuple_tempo) == 2:
            raise ValueError("Connection Datas are not valid")
        if tuple_tempo in self.connection_check_list:
            raise ValueError(f"{tuple_tempo} is a doublon in Connection Datas")
        self.connection_check_list.append(tuple_tempo)
        self.connection_check_list.append((tuple_tempo[1], tuple_tempo[0]))
        self.connection_name_list.append((tuple_tempo, qty_connections))

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

    def find_hub(self, name: str) -> Optional["MapParsing.HubData"]:
        """Return hub with name"""
        for hub in self.hub_list:
            if hub[0].name == name:
                return hub

    def create_connection_list(self) -> None:
        """Create list of connection by hub"""
        hub1: MapParsing.HubData
        hub2: MapParsing.HubData

        if self.connection_name_list == [] or self.connection_name_list is None:
            raise ValueError("There is not connection defined")

        for connection in self.connection_name_list:
            hub1 = self.find_hub(connection[0][0])
            hub2 = self.find_hub(connection[0][1])
            if hub1 is None or hub2 is None:
                raise ValueError("Connections list is not conform")
            self.connection_list.append([[hub1, hub2], connection[1]])
        
        # Parcours self.connection_name_list
        #   trouve chaque hub de la connection a l'aide de self.hub_list
        #   rajoute chaque hub et qty correspondant dans self.connection_list
        pass

    def check_hub_meta(self, string: str) -> "MapParsing.HubMeta":
        """Check if hub Meta is Conform"""
        tuple_tempo: tuple
        metas_str: str = self.recup_meta_only(string)
        metas: MapParsing.HubMeta

        zone_type_str: str = "normal"
        color_str: str = None
        max_drones_str: str = "1"
        zone_type_check: bool = False
        color_check: bool = False
        max_drones_check: bool = False

        if not metas_str == "[]":
            metas_separate: tuple = metas_str.split(" ")

            if len(metas_separate) > 3:
                raise ValueError(
                    f"{metas_separate} is not conform, "
                    "it must be countain 3 metadatas maximum"
                )
            for e in metas_separate:
                tuple_tempo = e.split("=")
                if not len(tuple_tempo) == 2:
                    raise ValueError(f"{e} is not conform metadata for hub")
                if tuple_tempo[0] == "zone" and zone_type_check is False:
                    zone_type_str = tuple_tempo[1]
                    zone_type_check: bool = True

                elif tuple_tempo[0] == "color" and color_check is False:
                    color_str = tuple_tempo[1]
                    color_check = True

                elif (
                    tuple_tempo[0] == "max_drones"
                    and max_drones_check is False
                ):
                    max_drones_str = tuple_tempo[1]
                    max_drones_check = True

                elif tuple_tempo[0] is not None:
                    raise ValueError(f"{e} is not conform metadata for hub")
        if max_drones_str is None:
            max_drones_str = "1"
        metas = MapParsing.HubMeta(
            zone_type=zone_type_str,
            color=color_str,
            max_drones=int(max_drones_str),
        )

        return metas

    def check_hub_datas(self, string: str, type: str) -> "MapParsing.HubData":
        """Check if hub Datas are Conform"""
        datas_str: str = self.recup_datas_only(string)
        datas: MapParsing.HubData

        datas_separate: tuple[str, str, str] = datas_str.split(" ")

        if not len(datas_separate) == 3:
            raise ValueError(
                f"{datas_separate} is not conform"
                ", it must be countain 3 datas"
            )
        datas = MapParsing.HubData(
            name=datas_separate[0],
            coordX=int(datas_separate[1]),
            coordY=int(datas_separate[2]),
            type=type,
        )
        if datas.name in self.name_used:
            raise ValueError(f"This name: {datas.name} is already used")
        if (datas.coordX, datas.coordY) in self.coord_list:
            raise ValueError(
                f"Coordinates: {datas.coordX}, "
                f"{datas.coordY} is already used"
            )

        self.name_used.append(datas.name)
        self.coord_list.append((datas.coordX, datas.coordY))

        return datas

    def check_hub(self, line: str, type: str) -> None:
        """Check hub"""
        datas: MapParsing.HubData = self.check_hub_datas(line, type)
        metas: MapParsing.HubMeta = self.check_hub_meta(line)
        if type == "start_hub":
            datas.nb_drones = self.nb_drones
        self.hub_list.append((datas, metas))

    def map_parsing(self) -> None:
        """Parsing of All the Map"""
        tuple_tempo: tuple
        type: str = None

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
                tuple_tempo = tuple(self.map_clean[i].split(":"))
                # if not len(tuple_tempo) == 2:
                #     raise ValueError(f"Definition of {type} is not valid")
                self.nb_drones = int(tuple_tempo[1])
                if self.nb_drones < 1:
                    raise ValueError(
                        f"{self.nb_drones} is not "
                        "a valid quantite of drones"
                    )

                continue

            elif type == "connection":
                self.check_connection_datas(self.map_clean[i])
            else:
                self.check_hub(self.map_clean[i], type)

        self.check_connections_list()
        self.create_connection_list()


# self.hub_list: list[tuple[MapParsing.HubData, MapParsing.HubMeta]] = []
#
# Transformer:  self.connection_list: list[tuple[tuple[str, str], int]] = []
# En:           self.connection_list: list[tuple[tuple[MapParsing.HubData, MapParsing.HubData], int]] = []

# Voir dans fonction check_connection_datas

# Modifier affichage des donnees dans le terminal pour etre conforme au sujet
