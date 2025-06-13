from typing import List, Dict
from tile_types import TileType
from biome_types import BiomeType

class TerrainMapper:
    def __init__(self):
        """Initialize the terrain mapper with biome-to-terrain mappings."""
        self.biome_to_terrain: Dict[str, str] = {
            BiomeType.OCEAN: TileType.DEEP_WATER.value,
            BiomeType.SWAMP: TileType.SHALLOW_WATER.value,
            BiomeType.DESERT: TileType.SAND.value,
            BiomeType.FOREST: TileType.FOREST.value,
            BiomeType.GRASSLAND: TileType.GRASS.value,
            BiomeType.STEPPE: TileType.GRASS.value,  # Using grass as base for steppe
            BiomeType.MOUNTAIN: TileType.MOUNTAIN.value,
            BiomeType.SNOW: TileType.MOUNTAIN.value  # Using mountain as base for snow
        }

    def translate_biomes(self, biome_map: List[List[str]]) -> List[List[str]]:
        """
        Convert a biome map to a terrain map.
        
        Args:
            biome_map: 2D list of biome type strings
            
        Returns:
            2D list of terrain type strings
        """
        height = len(biome_map)
        width = len(biome_map[0])
        terrain_map = []
        
        for y in range(height):
            terrain_row = []
            for x in range(width):
                biome = biome_map[y][x]
                terrain = self.biome_to_terrain.get(biome, TileType.GRASS.value)  # Default to grass if unknown
                terrain_row.append(terrain)
            terrain_map.append(terrain_row)
            
        return terrain_map

    def get_terrain_for_biome(self, biome: str) -> str:
        """
        Get the terrain type for a single biome.
        
        Args:
            biome: Biome type string
            
        Returns:
            Terrain type string
        """
        return self.biome_to_terrain.get(biome, TileType.GRASS.value)

def main():
    # Example usage
    from biome_generator import BiomeGenerator
    
    # Generate a biome map
    generator = BiomeGenerator(width=256, height=256, seed=1234)
    biome_map, _ = generator.generate()
    
    # Convert to terrain map
    mapper = TerrainMapper()
    terrain_map = mapper.translate_biomes(biome_map)
    
    print(f"Converted {len(biome_map)}x{len(biome_map[0])} biome map to terrain map")
    print(f"Sample terrain types: {set(tile for row in terrain_map[:5] for tile in row)}")

if __name__ == "__main__":
    main() 