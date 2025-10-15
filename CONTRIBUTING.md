# Contributing to viam-dht22-module

Thank you for your interest in contributing to the Viam DHT22 sensor module! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your hardware setup (Raspberry Pi model, DHT22 sensor type)
- Software versions (Python, viam-sdk, etc.)
- Any relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, commented code
3. **Test your changes** on actual hardware (Raspberry Pi + DHT22)
4. **Update documentation** if you've changed functionality
5. **Submit a pull request** with a clear description of changes

## Development Setup

### Prerequisites
- Raspberry Pi (4B or compatible) with Raspberry Pi OS
- DHT22 sensor properly wired
- Python 3.7 or higher
- Git

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/viam-dht22-module.git
cd viam-dht22-module

# Create a development branch
git checkout -b feature/my-new-feature

# Set up the development environment
./setup.sh

# Activate the virtual environment
source .venv/bin/activate

# Make your changes...
```

### Testing Your Changes

#### Local Testing
```bash
# Test the sensor directly
python3 src/humidity_sensor.py

# Test with Viam SDK (requires Viam robot configuration)
python3 -m src.main
```

#### Hardware Testing Checklist
- [ ] Sensor reads temperature correctly
- [ ] Sensor reads humidity correctly
- [ ] Error handling works when sensor is disconnected
- [ ] Configuration changes are applied correctly
- [ ] Module works with different GPIO pins
- [ ] Module integrates properly with Viam platform

### Code Style

- Follow PEP 8 style guidelines for Python code
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and small
- Comment complex logic

Example:
```python
async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:
    """
    Read the humidity and temperature from the DHT22 sensor.
    
    Args:
        extra: Optional extra parameters
        **kwargs: Additional keyword arguments
        
    Returns:
        A dictionary containing temperature and humidity,
        or an error message if reading fails
    """
    # Implementation...
```

### Documentation

If your changes affect how users interact with the module:
- Update README.md
- Update QUICKSTART.md if relevant
- Update code comments and docstrings
- Add examples if introducing new features

## Project Structure

```
viam-dht22-module/
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI/CD workflow
├── src/
│   ├── __init__.py          # Module initialization
│   ├── main.py              # Entry point
│   └── humidity_sensor.py   # Main sensor implementation
├── .env                     # Environment configuration
├── .gitignore              # Git ignore rules
├── config.example.json     # Example configuration
├── exec.sh                 # Module execution script
├── LICENSE                 # Apache 2.0 license
├── Makefile               # Build commands
├── meta.json              # Viam module metadata
├── README.md              # Main documentation
├── QUICKSTART.md          # Quick start guide
├── requirements.txt       # Python dependencies
└── setup.sh              # Setup script
```

## Release Process

Releases are automated via GitHub Actions:

1. Update version number in `meta.json`
2. Create a Git tag: `git tag v1.0.0`
3. Push the tag: `git push origin v1.0.0`
4. Create a GitHub release
5. GitHub Actions will automatically build and upload to Viam

## Testing on Hardware

### Required Hardware Setup
- Raspberry Pi 4B (or compatible)
- DHT22 sensor
- Proper wiring as described in QUICKSTART.md

### Test Scenarios

1. **Basic Functionality**
   - Sensor returns valid temperature readings
   - Sensor returns valid humidity readings
   - Readings are within expected ranges

2. **Error Handling**
   - Graceful handling when sensor is disconnected
   - Proper error messages
   - Recovery after temporary failures

3. **Configuration**
   - Different GPIO pins work correctly
   - Invalid configurations are rejected

4. **Integration**
   - Module loads in Viam platform
   - Readings appear in Viam UI
   - SDK can access sensor data

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Reach out on the Viam Discord community
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
