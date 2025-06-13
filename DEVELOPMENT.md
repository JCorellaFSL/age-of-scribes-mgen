# Development Guide

## Development Environment Setup

1. **Clone the Repository**
```bash
git clone https://github.com/JCorellaFSL/age-of-scribes-mgen.git
cd age-of-scribes-mgen
```

2. **Create a Virtual Environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

4. **Install Pre-commit Hooks**
```bash
pre-commit install
```

## Project Structure

```
age-of-scribes-mgen/
├── biome_generator.py    # Biome generation using Perlin noise
├── biome_types.py        # Biome type definitions and colors
├── region_generator.py   # Region generation with Voronoi
├── terrain_mapper.py     # Biome to terrain translation
├── terrain_renderer.py   # Terrain visualization
├── tile_types.py         # Terrain type definitions
├── tests/               # Test suite
│   ├── test_biome.py
│   ├── test_region.py
│   └── test_terrain.py
├── examples/            # Example scripts
│   ├── basic_usage.py
│   └── custom_generation.py
└── docs/               # Documentation
    ├── API_Documentation.md
    └── DEVELOPMENT.md
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use 4 spaces for indentation
- Use double quotes for strings

### Naming Conventions

- Classes: `CamelCase`
- Functions/Methods: `snake_case`
- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_leading_underscore`

### Documentation

- Use Google-style docstrings
- Document all public classes, methods, and functions
- Include type hints in docstrings
- Add examples for complex functionality

Example:
```python
def generate_biome_map(width: int, height: int, seed: int = None) -> List[List[str]]:
    """Generate a biome map using Perlin noise.
    
    Args:
        width: Map width in tiles
        height: Map height in tiles
        seed: Random seed for deterministic generation
        
    Returns:
        2D list of biome strings
        
    Example:
        >>> map = generate_biome_map(64, 64, seed=1234)
        >>> len(map)
        64
        >>> len(map[0])
        64
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_biome.py

# Run with coverage
pytest --cov=.
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use pytest fixtures for common setup
- Aim for high test coverage

Example:
```python
def test_biome_generation():
    generator = BiomeGenerator(width=64, height=64, seed=1234)
    biome_map, _ = generator.generate()
    
    assert len(biome_map) == 64
    assert len(biome_map[0]) == 64
    assert all(biome in BiomeType.__dict__.values() 
              for row in biome_map for biome in row)
```

## Contributing

### Workflow

1. Create a new branch for your feature/fix
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Run tests and ensure they pass
4. Update documentation if needed
5. Commit your changes
```bash
git commit -m "feat: add new feature"
```

6. Push to your branch
```bash
git push origin feature/your-feature-name
```

7. Create a Pull Request

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Maintenance tasks

### Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Performance Optimization

### Profiling

```bash
# Run with profiling
python -m cProfile -o output.prof your_script.py

# Analyze results
python -m pstats output.prof
```

### Memory Usage

```bash
# Monitor memory usage
python -m memory_profiler your_script.py
```

### Optimization Tips

1. Use numpy for array operations
2. Cache expensive computations
3. Use sets for membership testing
4. Minimize object creation in loops
5. Use generators for large datasets

## Debugging

### Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debug Tools

- Use `pdb` for interactive debugging
- Use `logging` for runtime information
- Use `pytest --pdb` for test debugging

## Release Process

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Create GitHub release
6. Tag release
7. Deploy to PyPI (if applicable)

## Common Issues

### Circular Imports

If you encounter circular imports:
1. Move shared code to a separate module
2. Use lazy imports
3. Restructure the code to avoid cycles

### Memory Issues

If you encounter memory issues:
1. Use generators instead of lists
2. Clear large objects when done
3. Use `__slots__` for classes with many instances
4. Profile memory usage

### Performance Issues

If you encounter performance issues:
1. Profile the code
2. Use numpy for array operations
3. Cache expensive computations
4. Optimize loops and data structures 