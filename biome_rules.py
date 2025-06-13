from typing import List, Set, Tuple
from collections import Counter
from tile_types import TileType

class BiomeRuleEngine:
    def __init__(self):
        """Initialize the biome rule engine with rule definitions."""
        self.rules = [
            self._rule_mountain_water,
            self._rule_isolated_grass,
            self._rule_isolated_water,
            self._rule_isolated_forest
        ]

    def _get_neighbors(self, terrain_map: List[List[str]], x: int, y: int) -> List[str]:
        """
        Get all 8 neighboring tiles for a given position.
        Returns empty string for out-of-bounds positions.
        """
        height = len(terrain_map)
        width = len(terrain_map[0])
        neighbors = []
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    neighbors.append(terrain_map[ny][nx])
                else:
                    neighbors.append("")
                    
        return neighbors

    def _rule_mountain_water(self, terrain_map: List[List[str]], x: int, y: int) -> str:
        """Rule 1: Convert mountain to forest if adjacent to deep water."""
        if terrain_map[y][x] != TileType.MOUNTAIN.value:
            return terrain_map[y][x]
            
        neighbors = self._get_neighbors(terrain_map, x, y)
        if TileType.DEEP_WATER.value in neighbors:
            return TileType.FOREST.value
            
        return terrain_map[y][x]

    def _rule_isolated_grass(self, terrain_map: List[List[str]], x: int, y: int) -> str:
        """Rule 2: Convert grass to sand if surrounded by mostly sand."""
        if terrain_map[y][x] != TileType.GRASS.value:
            return terrain_map[y][x]
            
        neighbors = self._get_neighbors(terrain_map, x, y)
        sand_count = neighbors.count(TileType.SAND.value)
        
        if sand_count >= 5:
            return TileType.SAND.value
            
        return terrain_map[y][x]

    def _rule_isolated_water(self, terrain_map: List[List[str]], x: int, y: int) -> str:
        """Rule 3: Convert shallow water to pond if surrounded by mostly land."""
        if terrain_map[y][x] != TileType.SHALLOW_WATER.value:
            return terrain_map[y][x]
            
        neighbors = self._get_neighbors(terrain_map, x, y)
        land_count = neighbors.count(TileType.GRASS.value) + neighbors.count(TileType.SAND.value)
        
        if land_count >= 6:
            return TileType.SAND.value  # Using sand as a placeholder for pond
            
        return terrain_map[y][x]

    def _rule_isolated_forest(self, terrain_map: List[List[str]], x: int, y: int) -> str:
        """Rule 4: Convert forest to grass if no adjacent grass or forest."""
        if terrain_map[y][x] != TileType.FOREST.value:
            return terrain_map[y][x]
            
        neighbors = self._get_neighbors(terrain_map, x, y)
        valid_neighbors = {TileType.GRASS.value, TileType.FOREST.value}
        
        if not any(n in valid_neighbors for n in neighbors):
            return TileType.GRASS.value
            
        return terrain_map[y][x]

    def apply_rules(self, terrain_map: List[List[str]]) -> List[List[str]]:
        """
        Apply all biome rules to the terrain map.
        
        Args:
            terrain_map: 2D list of terrain type strings
            
        Returns:
            New 2D list with rules applied
        """
        height = len(terrain_map)
        width = len(terrain_map[0])
        new_map = [row[:] for row in terrain_map]  # Create a deep copy
        
        # Apply each rule to each tile
        for y in range(height):
            for x in range(width):
                current_type = new_map[y][x]
                
                # Apply each rule in sequence
                for rule in self.rules:
                    new_type = rule(new_map, x, y)
                    if new_type != current_type:
                        new_map[y][x] = new_type
                        current_type = new_type
                        break  # Stop applying rules once a change is made
                        
        return new_map 