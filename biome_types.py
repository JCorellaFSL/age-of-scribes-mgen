from typing import Tuple

class BiomeType:
    """Enum-like class for biome types with associated colors."""
    OCEAN = "ocean"
    DESERT = "desert"
    SWAMP = "swamp"
    GRASSLAND = "grassland"
    FOREST = "forest"
    STEPPE = "steppe"
    MOUNTAIN = "mountain"
    SNOW = "snow"

    @classmethod
    def get_color(cls, biome_type: str) -> Tuple[int, int, int]:
        """Returns RGB color tuple for visualization."""
        color_map = {
            cls.OCEAN: (0, 0, 139),      # Dark blue
            cls.DESERT: (238, 214, 175),  # Sand color
            cls.SWAMP: (0, 100, 0),      # Dark green
            cls.GRASSLAND: (34, 139, 34), # Forest green
            cls.FOREST: (0, 100, 0),     # Dark green
            cls.STEPPE: (152, 251, 152),  # Pale green
            cls.MOUNTAIN: (139, 137, 137), # Gray
            cls.SNOW: (255, 250, 250)     # Snow white
        }
        return color_map[biome_type] 