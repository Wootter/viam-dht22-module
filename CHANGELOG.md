# Changelog

All notable changes to the viam-dht22-module will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-10-15

### Added
- Initial release of DHT22 sensor module for Viam
- Support for DHT22 (AM2302) temperature and humidity sensor
- Temperature readings in both Celsius and Fahrenheit
- Humidity readings in percentage
- Configurable GPIO pin selection
- Robust error handling and retry logic
- Comprehensive documentation (README, QUICKSTART, CONTRIBUTING)
- Hardware testing script
- Automated deployment via GitHub Actions
- Example configuration file
- Apache 2.0 license

### Features
- Compatible with Raspberry Pi 4B and other GPIO-enabled Pi models
- Uses Adafruit_DHT library for reliable sensor communication
- Returns properly formatted readings for Viam platform
- Graceful error handling when sensor is disconnected
- Support for BCM GPIO pin numbering

### Documentation
- Complete README with installation and usage instructions
- Quick start guide for rapid deployment
- Contributing guidelines
- Hardware wiring diagrams
- Troubleshooting section
- Python and TypeScript SDK examples

### Infrastructure
- GitHub Actions workflow for automated module deployment
- Makefile for easy module packaging
- Virtual environment setup scripts
- Comprehensive .gitignore

## Development Guidelines

### Version Numbering
- **Major version (X.0.0)**: Incompatible API changes
- **Minor version (0.X.0)**: New functionality, backwards compatible
- **Patch version (0.0.X)**: Bug fixes, backwards compatible

### Release Process
1. Update version in `meta.json`
2. Update this CHANGELOG.md
3. Update version in `pyproject.toml`
4. Commit changes: `git commit -m "Release vX.X.X"`
5. Create tag: `git tag vX.X.X`
6. Push: `git push && git push --tags`
7. Create GitHub release
8. Automated deployment via GitHub Actions

[Unreleased]: https://github.com/Wootter/viam-dht22-module/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Wootter/viam-dht22-module/releases/tag/v1.0.0
