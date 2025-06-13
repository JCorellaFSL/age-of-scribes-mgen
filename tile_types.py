from enum import Enum
from typing import Tuple

class TileType(Enum):
    DEEP_WATER = "deep_water"
    SHALLOW_WATER = "shallow_water"
    SAND = "sand"
    GRASS = "grass"
    FOREST = "forest"
    MOUNTAIN = "mountain"

    @classmethod
    def get_color(cls, tile_type: 'TileType') -> Tuple[int, int, int]:
        """Returns RGB color tuple for visualization."""
        color_map = {
            cls.DEEP_WATER: (0, 0, 139),
            cls.SHALLOW_WATER: (0, 0, 255),
            cls.SAND: (238, 214, 175),
            cls.GRASS: (34, 139, 34),
            cls.FOREST: (0, 100, 0),
            cls.MOUNTAIN: (139, 137, 137)
        }
        return color_map[tile_type] 