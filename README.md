# Age of Scribes Map Generator

A procedural 2D tile-based world generator that creates natural-looking terrain and regions. This component is part of the Age of Scribes game project but is designed to be used as a standalone utility for procedural map generation.

## Overview

The Age of Scribes Map Generator is a modular Python library that generates procedural 2D maps suitable for games, simulations, or visualization. It uses a multi-stage generation process:

1. **Biome Generation**: Creates a biome map using Perlin noise and biome rules
2. **Terrain Translation**: Converts biomes into specific terrain types
3. **Region Generation**: Divides the map into regions using biome-weighted Voronoi diagrams
4. **Visualization**: Renders the results with customizable tile sizes and color schemes

## Features

### Core Generation
- Deterministic generation using seed values
- Configurable map dimensions (default 256x256)
- Multiple generation stages for natural-looking results
- Modular design for easy extension

### Biome System
- 7 biome types: Ocean, Swamp, Desert, Grassland, Forest, Mountain, Snow
- Perlin noise-based biome distribution
- Biome transition rules for natural boundaries
- Biome-specific properties and weights

### Terrain System
- 6 terrain types: Deep Water, Shallow Water, Sand, Grass, Forest, Mountain
- Biome-to-terrain translation rules
- Customizable terrain properties
- Support for additional terrain types

### Region System
- Biome-weighted region seeding
- Voronoi-based region expansion
- Region smoothing and post-processing
- Region metadata tracking (size, dominant biome, centroid)

### Visualization
- Color-coded PNG output
- Customizable tile sizes
- Region boundary visualization
- Seed point marking
- Debug overlays

## Requirements

- Python 3.8+
- NumPy
- Pillow (PIL)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JCorellaFSL/age-of-scribes-mgen.git
cd age-of-scribes-mgen
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from biome_generator import BiomeGenerator
from terrain_mapper import TerrainMapper
from region_generator import RegionGenerator

# Generate a biome map
biome_gen = BiomeGenerator(width=256, height=256, seed=1234)
biome_map, _ = biome_gen.generate()

# Convert biomes to terrain
terrain_mapper = TerrainMapper()
terrain_map = terrain_mapper.translate_biomes(biome_map)

# Generate regions
region_gen = RegionGenerator(seed=1234)
region_map, seeds, region_data = region_gen.generate_regions(
    width=256, height=256,
    num_regions=8,
    biome_map=biome_map,
    min_region_size=20
)
```

### Visualization

Each generator includes visualization capabilities:

```python
# Render biome map
biome_gen.render_biome_map(biome_map, "biome_map.png")

# Render terrain map
terrain_mapper.render_terrain_map(terrain_map, "terrain_map.png")

# Render region map
region_gen.render_region_map(region_map, region_data, "region_map.png")
```

### Customization

The generator can be customized in several ways:

```python
# Custom biome weights for region generation
biome_weights = {
    "ocean": 0.1,
    "swamp": 0.4,
    "desert": 0.6,
    "grassland": 1.0,
    "forest": 1.2,
    "mountain": 0.2,
    "snow": 0.4
}

# Custom terrain colors
terrain_colors = {
    "deep_water": (0, 0, 100),
    "shallow_water": (0, 0, 200),
    "sand": (194, 178, 128),
    "grass": (34, 139, 34),
    "forest": (0, 100, 0),
    "mountain": (139, 137, 137)
}
```

## Integration with Age of Scribes

This map generator is designed to be a component of the Age of Scribes game project. In the game, it provides:

- Procedural world generation for new games
- Region-based gameplay mechanics
- Biome-specific features and events
- Terrain-based movement and combat rules

However, the generator is completely independent and can be used in any project that requires procedural map generation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Perlin noise implementation based on [OpenSimplex](https://github.com/lmas/opensimplex)
- Color schemes inspired by various map generation projects
- Region generation algorithm adapted from Voronoi-based approaches 