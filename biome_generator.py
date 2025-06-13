from typing import List, Tuple, Dict
import numpy as np
from PIL import Image
import random
from tile_types import TileType
from terrain_mapper import TerrainMapper
from biome_types import BiomeType

class BiomeGenerator:
    def __init__(self, width: int = 256, height: int = 256, seed: int = None):
        """
        Initialize the biome generator.
        
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
        self.terrain_mapper = TerrainMapper()

    def _generate_noise_map(self, scale: float = 4.0, octaves: int = 4) -> np.ndarray:
        """
        Generate a noise map using multiple octaves of sine/cosine waves.
        
        Args:
            scale: Base scale for the noise
            octaves: Number of noise octaves to combine
            
        Returns:
            2D numpy array of noise values in range [0, 1]
        """
        x = np.linspace(0, scale, self.width)
        y = np.linspace(0, scale, self.height)
        X, Y = np.meshgrid(x, y)
        
        noise = np.zeros((self.height, self.width))
        for octave in range(octaves):
            current_scale = 2 ** octave
            noise += np.sin(X * current_scale) * np.cos(Y * current_scale) / current_scale
        
        # Normalize to 0-1 range
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        return noise

    def _get_biome(self, elevation: float, moisture: float) -> str:
        """
        Determine biome type based on elevation and moisture values.
        
        Args:
            elevation: Elevation value in range [0, 1]
            moisture: Moisture value in range [0, 1]
            
        Returns:
            Biome type string
        """
        # Very low elevation is always ocean
        if elevation < 0.2:
            return BiomeType.OCEAN
            
        # High elevation logic
        if elevation > 0.8:
            return BiomeType.SNOW if moisture > 0.5 else BiomeType.MOUNTAIN
            
        # Mid elevation logic
        if elevation > 0.5:
            if moisture > 0.7:
                return BiomeType.FOREST
            elif moisture > 0.4:
                return BiomeType.GRASSLAND
            else:
                return BiomeType.STEPPE
                
        # Low elevation logic
        if moisture > 0.7:
            return BiomeType.SWAMP
        elif moisture > 0.4:
            return BiomeType.GRASSLAND
        else:
            return BiomeType.DESERT

    def generate(self) -> Tuple[List[List[str]], List[List[str]]]:
        """
        Generate biome and terrain maps.
        
        Returns:
            Tuple of (biome_map, terrain_map) where each is a 2D list of strings
        """
        # Generate elevation and moisture maps
        elevation_map = self._generate_noise_map(scale=4.0, octaves=4)
        moisture_map = self._generate_noise_map(scale=3.0, octaves=3)  # Different scale for variety
        
        # Initialize biome map
        biome_map = []
        
        # Generate biomes
        for y in range(self.height):
            biome_row = []
            for x in range(self.width):
                elevation = elevation_map[y, x]
                moisture = moisture_map[y, x]
                biome = self._get_biome(elevation, moisture)
                biome_row.append(biome)
            biome_map.append(biome_row)
        
        # Convert biomes to terrain
        terrain_map = self.terrain_mapper.translate_biomes(biome_map)
            
        return biome_map, terrain_map

    def render_to_image(self, biome_map: List[List[str]], output_path: str = None) -> None:
        """
        Render the biome map to an image file.
        
        Args:
            biome_map: 2D list of biome type strings
            output_path: Path to save the image (default: biomes_{seed}.png)
        """
        if output_path is None:
            output_path = f"biomes_{self.seed}.png"
            
        # Create a new image with RGB mode
        image = Image.new('RGB', (self.width, self.height))
        pixels = image.load()
        
        # Fill the image with biome colors
        for y in range(self.height):
            for x in range(self.width):
                pixels[x, y] = BiomeType.get_color(biome_map[y][x])
        
        # Save the image
        image.save(output_path)

def main():
    # Example usage
    generator = BiomeGenerator(width=256, height=256, seed=1234)
    biome_map, terrain_map = generator.generate()
    generator.render_to_image(biome_map)
    print(f"Generated biome map with seed {generator.seed}")

if __name__ == "__main__":
    main() 