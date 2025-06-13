from typing import List, Tuple
import numpy as np
from PIL import Image
import random
from biome_rules import BiomeRuleEngine
from tile_types import TileType

class WorldMapGenerator:
    def __init__(self, width: int = 256, height: int = 256, seed: int = None):
        """
        Initialize the world map generator.
        
        Args:
            width: Width of the map in tiles
            height: Height of the map in tiles
            seed: Random seed for deterministic generation
        """
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 2**32 - 1)
        random.seed(self.seed)
        np.random.seed(self.seed)
        self.biome_engine = BiomeRuleEngine()

    def _generate_noise_map(self) -> np.ndarray:
        """Generate a base noise map using Perlin-like noise."""
        # Create a grid of coordinates
        x = np.linspace(0, 4, self.width)
        y = np.linspace(0, 4, self.height)
        X, Y = np.meshgrid(x, y)
        
        # Generate multiple octaves of noise
        noise = np.zeros((self.height, self.width))
        for octave in range(4):
            scale = 2 ** octave
            noise += np.sin(X * scale) * np.cos(Y * scale) / scale
        
        # Normalize to 0-1 range
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        return noise

    def _noise_to_terrain(self, noise_value: float) -> TileType:
        """Convert a noise value to a terrain type."""
        if noise_value < 0.2:
            return TileType.DEEP_WATER
        elif noise_value < 0.3:
            return TileType.SHALLOW_WATER
        elif noise_value < 0.4:
            return TileType.SAND
        elif noise_value < 0.7:
            return TileType.GRASS
        elif noise_value < 0.85:
            return TileType.FOREST
        else:
            return TileType.MOUNTAIN

    def generate(self) -> List[List[str]]:
        """
        Generate the terrain map.
        
        Returns:
            A 2D list of terrain type strings
        """
        noise_map = self._generate_noise_map()
        terrain_map = []
        
        for row in range(self.height):
            terrain_row = []
            for col in range(self.width):
                terrain_type = self._noise_to_terrain(noise_map[row, col])
                terrain_row.append(terrain_type.value)
            terrain_map.append(terrain_row)
        
        # Apply biome rules to smooth transitions
        terrain_map = self.biome_engine.apply_rules(terrain_map)
            
        return terrain_map

    def render_to_image(self, terrain_map: List[List[str]], output_path: str = None) -> None:
        """
        Render the terrain map to an image file.
        
        Args:
            terrain_map: 2D list of terrain type strings
            output_path: Path to save the image (default: world_{seed}.png)
        """
        if output_path is None:
            output_path = f"world_{self.seed}.png"
            
        # Create a new image with RGB mode
        image = Image.new('RGB', (self.width, self.height))
        pixels = image.load()
        
        # Fill the image with terrain colors
        for y in range(self.height):
            for x in range(self.width):
                terrain_type = TileType(terrain_map[y][x])
                pixels[x, y] = TileType.get_color(terrain_type)
        
        # Save the image
        image.save(output_path)

def main():
    # Example usage
    generator = WorldMapGenerator(width=256, height=256, seed=1234)
    terrain_map = generator.generate()
    generator.render_to_image(terrain_map)
    print(f"Generated world map with seed {generator.seed}")

if __name__ == "__main__":
    main() 