# API Documentation

## Core Classes

### BiomeGenerator

```python
class BiomeGenerator:
    def __init__(self, width: int = 256, height: int = 256, seed: int = None):
        """
        Initialize the biome generator.
        
        Args:
            width: Map width in tiles (default: 256)
            height: Map height in tiles (default: 256)
            seed: Random seed for deterministic generation
        """
    
    def generate(self) -> Tuple[List[List[str]], Dict[str, Any]]:
        """
        Generate a biome map using Perlin noise.
        
        Returns:
            Tuple of (biome_map, metadata)
            - biome_map: 2D list of biome strings
            - metadata: Dictionary containing generation parameters
        """
    
    def render_biome_map(self, biome_map: List[List[str]], output_path: str = "biome_map.png") -> None:
        """
        Render the biome map to an image file.
        
        Args:
            biome_map: 2D list of biome strings
            output_path: Path to save the image
        """
```

### TerrainMapper

```python
class TerrainMapper:
    def __init__(self):
        """Initialize the terrain mapper with default biome-to-terrain mappings."""
    
    def translate_biomes(self, biome_map: List[List[str]]) -> List[List[str]]:
        """
        Convert a biome map to a terrain map.
        
        Args:
            biome_map: 2D list of biome strings
            
        Returns:
            2D list of terrain strings
        """
    
    def get_terrain_for_biome(self, biome: str) -> str:
        """
        Get the terrain type for a single biome.
        
        Args:
            biome: Biome string
            
        Returns:
            Terrain string
        """
```

### RegionGenerator

```python
class RegionGenerator:
    def __init__(self, seed: int = None):
        """
        Initialize the region generator.
        
        Args:
            seed: Random seed for deterministic generation
        """
    
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
            - region_map: 2D list of region IDs
            - region_seeds: List of (x, y) seed coordinates
            - region_data: Dictionary of region metadata
        """
    
    def render_region_map(self, region_map: List[List[int]], region_data: Dict[int, Any], 
                         output_path: str = "region_preview.png") -> None:
        """
        Render the region map to an image file.
        
        Args:
            region_map: 2D list of region IDs
            region_data: Dictionary of region metadata
            output_path: Path to save the image
        """
```

## Data Types

### BiomeType

```python
class BiomeType:
    # Biome type constants
    OCEAN = "ocean"
    SWAMP = "swamp"
    DESERT = "desert"
    GRASSLAND = "grassland"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    SNOW = "snow"
    
    @classmethod
    def get_color(cls, biome: str) -> Tuple[int, int, int]:
        """
        Get the RGB color for a biome type.
        
        Args:
            biome: Biome string
            
        Returns:
            RGB color tuple
        """
```

### TileType

```python
class TileType:
    # Terrain type constants
    DEEP_WATER = "deep_water"
    SHALLOW_WATER = "shallow_water"
    SAND = "sand"
    GRASS = "grass"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    
    @classmethod
    def get_color(cls, terrain: str) -> Tuple[int, int, int]:
        """
        Get the RGB color for a terrain type.
        
        Args:
            terrain: Terrain string
            
        Returns:
            RGB color tuple
        """
```

## Region Data Structure

The `region_data` dictionary returned by `RegionGenerator.generate_regions()` has the following structure:

```python
{
    region_id: {
        'id': int,                    # Region ID
        'seed': Tuple[int, int],      # (x, y) coordinates of region seed
        'area': int,                  # Number of tiles in region
        'tiles': Set[Tuple[int, int]], # Set of (x, y) coordinates of region tiles
        'biome_counts': Counter,      # Count of each biome type in region
        'dominant_biome': str,        # Most common biome in region
        'centroid': Tuple[int, int]   # (x, y) coordinates of region center
    }
}
```

## Customization

### Biome Weights

```python
biome_weights = {
    "ocean": 0.1,      # Low weight - less likely to be chosen as region seed
    "swamp": 0.4,      # Medium-low weight
    "desert": 0.6,     # Medium weight
    "grassland": 1.0,  # Base weight
    "forest": 1.2,     # Medium-high weight
    "mountain": 0.2,   # Low weight
    "snow": 0.4        # Medium-low weight
}
```

### Terrain Colors

```python
terrain_colors = {
    "deep_water": (0, 0, 100),        # Dark blue
    "shallow_water": (0, 0, 200),     # Light blue
    "sand": (194, 178, 128),          # Beige
    "grass": (34, 139, 34),           # Forest green
    "forest": (0, 100, 0),            # Dark green
    "mountain": (139, 137, 137)       # Gray
}
```

## Error Handling

All classes handle errors gracefully:

- Invalid biome/terrain types default to "grassland"/"grass"
- Invalid coordinates are clamped to map boundaries
- Invalid region sizes are adjusted to valid ranges
- File I/O errors are caught and reported

## Performance Considerations

- Biome generation uses numpy for efficient array operations
- Region generation uses sets for fast tile membership testing
- Rendering uses PIL for efficient image manipulation
- Memory usage scales linearly with map size 