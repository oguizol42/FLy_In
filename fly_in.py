import parsing
import displaying
import drones_manager
from typing import TextIO, Optional
import os


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


def main() -> None:
    choice: int
    map: Drone_Map

    try:
        print(
            "\n\n"
            "Choose your map :\n\n"
            "EASY MAPS\n"
            "   1/ linear_path\n"
            "   2/ simple_fork\n"
            "   3/ basic_capacity\n"
            "\nMEDIUM MAPS\n"
            "   4/ dead_end_trap\n"
            "   5/ circular_loop\n"
            "   6/ priority_puzzle\n"
            "\nHARD MAPS\n"
            "   7/ maze_nightmare\n"
            "   8/ capacity_hell\n"
            "   9/ ultimate_challenge\n"
            "\nCHALLENGER MAP\n"
            "   10/ the_impossible_dream\n"
            )
        choice = int(input("\nyour choice: "))
        if (
            not isinstance(choice, int)
            or choice < 1
            or choice > 10
        ):
            raise ValueError(f"Choice: {choice} is incorrect")

        if choice == 1:
            map = Drone_Map("maps/easy/01_linear_path.txt")

        elif choice == 2:
            map = Drone_Map("maps/easy/02_simple_fork.txt")

        elif choice == 3:
            map = Drone_Map("maps/easy/03_basic_capacity.txt")

        if choice == 4:
            map = Drone_Map("maps/medium/01_dead_end_trap.txt")

        if choice == 5:
            map = Drone_Map("maps/medium/02_circular_loop.txt")

        if choice == 6:
            map = Drone_Map("maps/medium/03_priority_puzzle.txt")

        if choice == 7:
            map = Drone_Map("maps/hard/01_maze_nightmare.txt")

        if choice == 8:
            map = Drone_Map("maps/hard/02_capacity_hell.txt")

        if choice == 9:
            map = Drone_Map("maps/hard/03_ultimate_challenge.txt")

        if choice == 10:
            map = Drone_Map(
                "maps/challenger/01_the_impossible_dream.txt"
            )

        os.system("clear")

        map.loading_map()
        map.map_parsing()
        map.drones_manager()
        map.displaying_simulation()
        map.calcul_map_size()
        map.displaying_map()
    except ValueError as e:
        print(e)

    except (FileNotFoundError, PermissionError, FileExistsError) as e:
        print(e)


if __name__ == "__main__":
    main()


# Map File Loading      "fly_in.py"
# Map Parsing           "parsyng.py"
# Create Drones         "fly_in.py"
# Exectute Algorythm    "fly_in.py"
# Display               "display.py"

# Programs test
