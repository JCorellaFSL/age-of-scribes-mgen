from typing import List, Dict, Tuple
from PIL import Image

class TerrainRenderer:
    def __init__(self):
        self.terrain_colors: Dict[str, Tuple[int, int, int]] = {
            "deep_water": (0, 0, 128),
            "shallow_water": (0, 128, 192),
            "sand": (237, 201, 175),
            "grass": (34, 139, 34),
            "forest": (0, 100, 0),
            "dirt": (139, 69, 19),
            "mountain": (169, 169, 169),
            "snow": (255, 250, 250)
        }

    def render(self, terrain_map: List[List[str]], tile_size: int, output_path: str) -> None:
        """
        Render a terrain map to an image file with adjustable tile size.
        Args:
            terrain_map: 2D list of terrain type strings
            tile_size: Size (in pixels) of each tile
            output_path: Path to save the image
        """
        height = len(terrain_map)
        width = len(terrain_map[0])
        img_width = width * tile_size
        img_height = height * tile_size
        image = Image.new('RGB', (img_width, img_height))
        pixels = image.load()

        for y in range(height):
            for x in range(width):
                color = self.terrain_colors.get(terrain_map[y][x], (255, 0, 255))  # Magenta for unknown
                for dy in range(tile_size):
                    for dx in range(tile_size):
                        px = x * tile_size + dx
                        py = y * tile_size + dy
                        pixels[px, py] = color
        image.save(output_path)


def main():
    # Example usage
    from biome_generator import BiomeGenerator
    from terrain_mapper import TerrainMapper
    generator = BiomeGenerator(width=32, height=32, seed=1234)
    biome_map, terrain_map = generator.generate()
    renderer = TerrainRenderer()
    renderer.render(terrain_map, tile_size=32, output_path="terrain_map.png")
    print("Saved terrain_map.png")

if __name__ == "__main__":
    main() 