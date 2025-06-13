# Age of Scribes Map Generator

A procedural 2D tile-based world generator that creates natural-looking terrain and regions.

## Features

- Biome generation with Perlin noise
- Biome-to-terrain translation
- Region generation with biome-weighted seeding
- Region smoothing and post-processing
- Visual debugging with customizable tile sizes

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

## License

MIT License 