from typing import List, Tuple, Dict, Any, Set, Counter
import random
import numpy as np
from PIL import Image
from collections import defaultdict, Counter

class RegionGenerator:
    def __init__(self, seed: int = None):
        """
        Initialize the region generator.
        
        Args:
            seed: Random seed for deterministic generation
        """
        self.seed = seed if seed is not None else random.randint(0, 2**32 - 1)
        random.seed(self.seed)
        np.random.seed(self.seed)
        
        # Biome weights for seed selection
        self.biome_weights = {
            "ocean": 0.1,
            "swamp": 0.4,
            "desert": 0.6,
            "grassland": 1.0,
            "forest": 1.2,
            "mountain": 0.2,
            "snow": 0.4
        }

    def _manhattan_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate Manhattan distance between two points."""
        return abs(x1 - x2) + abs(y1 - y2)

    def _get_biome_weight(self, biome: str) -> float:
        """Get the weight for a given biome."""
        return self.biome_weights.get(biome, 0.5)  # Default weight for unknown biomes

    def _generate_seed_points(self, width: int, height: int, num_regions: int, 
                            biome_map: List[List[str]], min_region_size: int = 20) -> List[Tuple[int, int]]:
        """
        Generate seed points for regions using biome-weighted selection.
        
        Args:
            width: Map width in tiles
            height: Map height in tiles
            num_regions: Number of regions to generate
            biome_map: 2D list of biome strings
            min_region_size: Minimum size for a valid region
            
        Returns:
            List of (x, y) tuples representing seed points
        """
        # Calculate minimum distance between seeds based on map size and desired regions
        min_distance = int(np.sqrt((width * height) / (num_regions * 2)))
        seeds = []
        attempts = 0
        max_attempts = num_regions * 100  # Prevent infinite loops
        
        # Create a list of all valid positions with their biome weights
        valid_positions = []
        for y in range(height):
            for x in range(width):
                biome = biome_map[y][x]
                weight = self._get_biome_weight(biome)
                valid_positions.append((x, y, weight))
        
        # Sort positions by weight (descending)
        valid_positions.sort(key=lambda x: x[2], reverse=True)
        
        while len(seeds) < num_regions and attempts < max_attempts:
            # Select a position with probability proportional to its weight
            total_weight = sum(w for _, _, w in valid_positions)
            r = random.uniform(0, total_weight)
            current_weight = 0
            
            for x, y, weight in valid_positions:
                current_weight += weight
                if current_weight >= r:
                    # Check distance to existing seeds
                    too_close = False
                    for sx, sy in seeds:
                        if self._manhattan_distance(x, y, sx, sy) < min_distance:
                            too_close = True
                            break
                    
                    if not too_close:
                        seeds.append((x, y))
                        # Remove this position and nearby positions from valid_positions
                        valid_positions = [(px, py, w) for px, py, w in valid_positions 
                                         if self._manhattan_distance(px, py, x, y) >= min_distance]
                    break
            
            attempts += 1
            
        return seeds

    def _assign_tiles_to_regions(self, width: int, height: int, seeds: List[Tuple[int, int]], 
                               biome_map: List[List[str]]) -> Tuple[List[List[int]], Dict[int, Any]]:
        """
        Assign each tile to its nearest region seed and collect region metadata.
        
        Args:
            width: Map width in tiles
            height: Map height in tiles
            seeds: List of (x, y) tuples representing seed points
            biome_map: 2D list of biome strings
            
        Returns:
            Tuple of (region_map, region_data)
        """
        region_map = [[-1 for _ in range(width)] for _ in range(height)]
        region_data = defaultdict(lambda: {
            'id': -1,
            'seed': (0, 0),
            'area': 0,
            'tiles': set(),
            'biome_counts': Counter(),
            'dominant_biome': None,
            'centroid': (0, 0)
        })
        
        # Initialize region data
        for i, (x, y) in enumerate(seeds):
            region_data[i].update({
                'id': i,
                'seed': (x, y),
                'area': 0,
                'tiles': set(),
                'biome_counts': Counter(),
                'dominant_biome': None,
                'centroid': (x, y)
            })
        
        # Assign tiles to regions
        for y in range(height):
            for x in range(width):
                min_dist = float('inf')
                nearest_region = -1
                
                # Find nearest seed
                for i, (sx, sy) in enumerate(seeds):
                    dist = self._manhattan_distance(x, y, sx, sy)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_region = i
                
                # Assign tile to region
                region_map[y][x] = nearest_region
                region_data[nearest_region]['area'] += 1
                region_data[nearest_region]['tiles'].add((x, y))
                region_data[nearest_region]['biome_counts'][biome_map[y][x]] += 1
        
        # Calculate dominant biomes and centroids
        for region_id, data in region_data.items():
            if data['biome_counts']:
                data['dominant_biome'] = data['biome_counts'].most_common(1)[0][0]
            
            # Calculate centroid
            if data['tiles']:
                x_sum = sum(x for x, _ in data['tiles'])
                y_sum = sum(y for _, y in data['tiles'])
                data['centroid'] = (x_sum // data['area'], y_sum // data['area'])
        
        return region_map, dict(region_data)

    def _smooth_regions(self, region_map: List[List[int]], iterations: int = 2) -> List[List[int]]:
        """
        Smooth region boundaries by majority voting.
        
        Args:
            region_map: 2D list of region IDs
            iterations: Number of smoothing passes
            
        Returns:
            Smoothed region map
        """
        height = len(region_map)
        width = len(region_map[0])
        smoothed = [row[:] for row in region_map]
        
        for _ in range(iterations):
            new_map = [row[:] for row in smoothed]
            for y in range(height):
                for x in range(width):
                    # Get neighboring regions
                    neighbors = []
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                neighbors.append(smoothed[ny][nx])
                    
                    if neighbors:
                        # Use most common neighbor
                        new_map[y][x] = Counter(neighbors).most_common(1)[0][0]
            
            smoothed = new_map
        
        return smoothed

    def generate_regions(self, width: int, height: int, num_regions: int, 
                        biome_map: List[List[str]], min_region_size: int = 20) -> Tuple[List[List[int]], List[Tuple[int, int]], Dict[int, Any]]:
        """
        Generate regions using biome-weighted Voronoi-style seeding.
        
        Args:
            width: Map width in tiles
            height: Map height in tiles
            num_regions: Number of regions to generate
            biome_map: 2D list of biome strings
            min_region_size: Minimum size for a valid region
            
        Returns:
            Tuple of (region_map, region_seeds, region_data)
        """
        # Generate seed points
        seeds = self._generate_seed_points(width, height, num_regions, biome_map, min_region_size)
        
        # Assign tiles to regions
        region_map, region_data = self._assign_tiles_to_regions(width, height, seeds, biome_map)
        
        # Smooth region boundaries
        region_map = self._smooth_regions(region_map)
        
        return region_map, seeds, region_data

    def render_region_map(self, region_map: List[List[int]], region_data: Dict[int, Any], 
                         output_path: str = "region_preview.png") -> None:
        """
        Render the region map to an image file with region boundaries and seeds.
        
        Args:
            region_map: 2D list of region IDs
            region_data: Dictionary of region metadata
            output_path: Path to save the image
        """
        height = len(region_map)
        width = len(region_map[0])
        
        # Generate unique colors for each region
        num_regions = max(max(row) for row in region_map) + 1
        colors = []
        for i in range(num_regions):
            # Generate a random but deterministic color
            random.seed(self.seed + i)
            r = random.randint(50, 200)
            g = random.randint(50, 200)
            b = random.randint(50, 200)
            colors.append((r, g, b))
        
        # Create and save image
        image = Image.new('RGB', (width, height))
        pixels = image.load()
        
        # Fill regions with colors
        for y in range(height):
            for x in range(width):
                region_id = region_map[y][x]
                pixels[x, y] = colors[region_id]
        
        # Draw region boundaries
        for y in range(height):
            for x in range(width):
                current_region = region_map[y][x]
                # Check if this is a boundary tile
                is_boundary = False
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if region_map[ny][nx] != current_region:
                                is_boundary = True
                                break
                    if is_boundary:
                        break
                
                if is_boundary:
                    pixels[x, y] = (0, 0, 0)  # Black boundaries
        
        # Draw seed points
        for region_id, data in region_data.items():
            x, y = data['seed']
            # Draw a 3x3 cross at seed points
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 or dy == 0:  # Only draw cross, not corners
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            pixels[nx, ny] = (255, 255, 255)  # White seeds
        
        image.save(output_path)

def main():
    # Example usage
    from biome_generator import BiomeGenerator
    
    # Generate a biome map
    biome_gen = BiomeGenerator(width=64, height=64, seed=1234)
    biome_map, _ = biome_gen.generate()
    
    # Generate regions
    region_gen = RegionGenerator(seed=1234)
    region_map, seeds, region_data = region_gen.generate_regions(
        width=64, height=64, num_regions=8, 
        biome_map=biome_map, min_region_size=20
    )
    
    # Render the result
    region_gen.render_region_map(region_map, region_data)
    
    print(f"Generated {len(seeds)} regions")
    print(f"Region sizes: {[data['area'] for data in region_data.values()]}")
    print(f"Dominant biomes: {[data['dominant_biome'] for data in region_data.values()]}")
    print(f"Saved region_preview.png")

if __name__ == "__main__":
    main() 