import parsing

# from pydantic import BaseModel, Field, ValidationError, model_validator
# from typing import Optional
# from enum import Enum


# class Drone_Map(parsing.MapParsing):
#     def __init__(self, file_name: str) -> None:
#         self.file_name = file_name
#         self.map_text: str = None

#     def loading_map(self) -> None:
#         """Loading Map from File"""
#         try:
#             fd: int = open(self.file_name, "r")
#             self.map_text: str = fd.read()
#             fd.close()
#         except FileNotFoundError as e:
#             print(e)
#         except IsADirectoryError as e:
#             print(e)

#     def display_map(self) -> None:
#         """Display Graphical Map from File"""
#         try:
#             if self.map_text is None:
#                 raise AttributeError("No Map Loaded")
#             print(self.map_text)
#         except AttributeError as e:
#             print(e)


class Drone_Map(parsing.MapParsing):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.map_text: str = None
        super().__init__()

    def loading_map(self) -> None:
        """Loading Map from File"""
        fd: int = open(self.file_name, "r")
        self.map_text: str = fd.read()
        fd.close()

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


# Map File Loading
# Map Parsing
# Map Display


class Drones_Fly:
    def __init__(self, qty_drones: int) -> None:
        pass

    class Drone:
        def __init__(self, qty_drones: int) -> None:
            pass


# Creating each Drones From class Drone
# Moving Algorythm
# Memorising Moving of Each turn for each Drone


class Manage_flies:
    def __init__(self) -> None:
        pass


# Manage Drones List Creation
#   (after Loading and Parsing of Map by class Drone_Map)
# Excute Algorythm (by Drone_Fly class)


def main() -> None:
    try:
        # map: Drone_Map = Drone_Map("maps/easy/01_linear_path.txt")
        map: Drone_Map = Drone_Map("maps/hard/01_maze_nightmare.txt")

        map.loading_map()
        map.map_parsing()
        map.display_map_datas()

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()


# Map File Loading      "fly_in.py"
# Map Parsing           "parsyng.py"
# Create Drones         "fly_in.py"
# Exectute Algorythm    "fly_in.py"
# Display               "display.py"

# Programs test
