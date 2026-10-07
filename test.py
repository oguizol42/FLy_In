from fly_in import Drone_Map  # , Drones_Fly, Manage_flies
from pydantic import ValidationError


def parsing_tests() -> None:
    """Test Functions Parsing"""
    pass


def displaying_map_settup_test(test_map: Drone_Map) -> None:
    """Test Displayong Map"""
    if test_map.map_text is None:
        print("No Map Loaded")
    else:
        print(test_map.map_text)
    if test_map.map_clean is None or test_map.map_clean == []:
        print("Map is not Cleaned")
    try:
        test_map.clean_map()
    except ValueError as e:
        print(e)
    if test_map.map_clean is not None and test_map.map_clean != []:
        print(test_map.map_clean)

    print("\n\nFinal Map Parsed:\n")
    print(f"Hubs list:\n{test_map.hub_list}\n")
    print(f"Connections list:\n{test_map.connection_list}\n")


def loading_test(test_file: Drone_Map) -> None:
    """Test Loading of Map File"""
    try:
        test_file.loading_map()
    except FileNotFoundError as e:
        print(e)
    except IsADirectoryError as e:
        print(e)


def main() -> None:
    """Test every functions"""
    # test_map: Drone_Map = Drone_Map("maps_test/02_linear_path.txt")
    test_map: Drone_Map = Drone_Map("maps/hard/01_maze_nightmare.txt")
    test_map2: Drone_Map = Drone_Map("maps/easy/01_linear_path2")
    test_map3: Drone_Map = Drone_Map("maps/easy")

    print("TESTING WITHOUT FILE LOADED:")
    displaying_map_settup_test(test_map)

    print("\nTESTING WITH GOOD MAP LOADED:")
    loading_test(test_map)
    try:
        test_map.map_parsing()
        test_map.display_map()
    except ValueError as e:
        print(e)
    except ValidationError as e:
        print(e)
    print()

    print("\nTESTING BY LOADED A FILE THAT NOT EXIST:")
    loading_test(test_map2)

    print("\nTESTING BY LOADED A REPERTORY:")
    loading_test(test_map3)


if __name__ == "__main__":
    main()
