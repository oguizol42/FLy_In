import parsing
import displaying
import drones_manager
from typing import TextIO, Optional


class Drone_Map(
    parsing.MapParsing, drones_manager.DronesManager, displaying.Displaying
):
    def __init__(self, file_name: str) -> None:
        super().__init__()
        self.file_name = file_name
        self.map_text: Optional[str] = None

    def loading_map(self) -> None:
        """Loading Map from File"""
        fd: TextIO = open(self.file_name, "r")
        self.map_text = fd.read()
        fd.close()


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
        # map: Drone_Map = Drone_Map("maps_test/01_linear_path.txt")
        # map: Drone_Map = Drone_Map("maps_test/01_linear_path_8_drones.txt")
        # map: Drone_Map = Drone_Map("maps_test/02_simple_fork.txt")

        # map: Drone_Map = Drone_Map("maps/easy/01_linear_path.txt")
        map: Drone_Map = Drone_Map("maps/easy/02_simple_fork.txt")
        # map: Drone_Map = Drone_Map("maps/easy/03_basic_capacity.txt")

        # map: Drone_Map = Drone_Map("maps/medium/01_dead_end_trap.txt")
        # map: Drone_Map = Drone_Map("maps/medium/02_circular_loop.txt")
        # map: Drone_Map = Drone_Map("maps/medium/03_priority_puzzle.txt")

        # map: Drone_Map = Drone_Map("maps/hard/01_maze_nightmare.txt")
        # map: Drone_Map = Drone_Map("maps/hard/02_capacity_hell.txt")
        # map: Drone_Map = Drone_Map("maps/hard/03_ultimate_challenge.txt")

        # map: Drone_Map = Drone_Map(
        #     "maps/challenger/01_the_impossible_dream.txt"
        # )

        map.loading_map()
        map.map_parsing()
        # map.display_map_datas()
        map.drones_manager()
        # map.display_main_datas()

        print(f"Nombre de drones: {len(map.drone_list)}")

        map.displaying_simulation()
        map.calcul_map_size()
        map.displaying_map()
    except ValueError as e:
        print(e)

    # map: Drone_Map = Drone_Map("maps/hard/01_maze_nightmare.txt")

    # map.loading_map()
    # map.map_parsing()

    # # map.display_map_datas()

    # map.display_main_datas()
    # map.drones_manager()
    # map.calcul_map_size()
    # map.displaying_map()


if __name__ == "__main__":
    main()


# Map File Loading      "fly_in.py"
# Map Parsing           "parsyng.py"
# Create Drones         "fly_in.py"
# Exectute Algorythm    "fly_in.py"
# Display               "display.py"

# Programs test
