# File Structure Guide

This document explains the purpose of each file in the viam-dht22-module project.

## Project Root

```
viam-dht22-module/
├── .env                      # Environment variables for Python virtual environment
├── .gitignore               # Git ignore patterns (Python, venv, build artifacts)
├── CHANGELOG.md             # Version history and release notes
├── CONTRIBUTING.md          # Guidelines for contributing to the project
├── LICENSE                  # Apache 2.0 license
├── Makefile                 # Build commands (make module.tar.gz, make clean)
├── PROJECT_SUMMARY.md       # High-level project overview and setup guide
├── QUICKSTART.md            # Step-by-step quick start guide
├── README.md                # Main project documentation
├── config.example.json      # Example Viam robot configuration
├── exec.sh                  # Module execution script (called by Viam)
├── meta.json                # Viam module metadata and configuration
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python package dependencies
├── setup.sh                 # Setup script for installing dependencies
├── test_hardware.py         # Hardware testing script for DHT22 sensor
├── .github/                 # GitHub-specific files
│   └── workflows/
│       └── deploy.yml       # GitHub Actions workflow for automated deployment
└── src/                     # Source code directory
    ├── __init__.py          # Module initialization and registration
    ├── main.py              # Module entry point
    └── humidity_sensor.py   # DHT22 sensor implementation
```

## Detailed File Descriptions

### Configuration Files

#### `.env`
Defines environment variables for the Python virtual environment:
- `VIRTUAL_ENV`: Path to virtual environment directory
- `PYTHON`: Path to Python interpreter in virtual environment

#### `meta.json`
Viam module metadata:
- Module ID and visibility
- GitHub repository URL
- API and model definitions
- Entry point script

#### `config.example.json`
Example robot configuration showing how to add the DHT22 sensor to a Viam robot.

#### `pyproject.toml`
Modern Python project configuration:
- Package metadata
- Dependencies
- Build system configuration
- Development tools configuration (black, mypy)

#### `requirements.txt`
Python package dependencies:
- `viam-sdk`: Viam robotics SDK
- `Adafruit-DHT`: DHT22 sensor library
- `RPi.GPIO`: Raspberry Pi GPIO control

### Scripts

#### `exec.sh` (Executable)
Entry point script called by Viam to start the module:
1. Changes to module directory
2. Sources environment variables
3. Runs setup script
4. Executes main Python module

**Purpose**: Ensures module runs in correct environment with all dependencies.

#### `setup.sh` (Executable)
Dependency installation and environment setup:
1. Checks for and installs system packages (python3-venv, python3-dev)
2. Creates Python virtual environment
3. Installs Python packages from requirements.txt

**Purpose**: Prepares the runtime environment on Raspberry Pi.

#### `test_hardware.py` (Executable)
Hardware testing script:
- Tests DHT22 sensor connectivity
- Takes multiple readings
- Validates reading ranges
- Provides diagnostic information

**Usage**: `python3 test_hardware.py --pin 4`

### Source Code (`src/`)

#### `humidity_sensor.py`
Main sensor implementation:
- `MySensor` class extending Viam `Sensor` base class
- Reads temperature and humidity from DHT22
- Returns formatted readings with error handling
- Supports configurable GPIO pin

**Key methods**:
- `__init__()`: Initialize sensor with pin
- `new()`: Factory method for Viam
- `get_readings()`: Read and return sensor data

#### `__init__.py`
Module initialization:
- Imports sensor class
- Registers sensor with Viam registry

#### `main.py`
Module entry point:
- Registers sensor with Viam
- Runs module from registry when executed

### Documentation

#### `README.md`
Main project documentation:
- Project overview and features
- Hardware requirements and wiring
- Installation instructions
- Configuration guide
- Usage examples (Python and TypeScript)
- Troubleshooting
- Links to resources

#### `QUICKSTART.md`
Step-by-step setup guide:
- Hardware wiring instructions
- Software installation steps
- Viam integration guide
- Testing procedures
- Troubleshooting tips

#### `CONTRIBUTING.md`
Contribution guidelines:
- How to report bugs
- How to suggest enhancements
- Pull request process
- Development setup
- Testing requirements
- Code style guidelines

#### `PROJECT_SUMMARY.md`
High-level project overview:
- What files were created
- Differences from DHT11 module
- Configuration format
- Deployment options
- Next steps

#### `CHANGELOG.md`
Version history:
- Release notes
- Feature additions
- Bug fixes
- Breaking changes

#### `LICENSE`
Apache License 2.0 - open source license allowing commercial use.

### Build Files

#### `Makefile`
Build automation:
- `make module.tar.gz`: Package module for distribution
- `make clean`: Remove build artifacts and virtual environment

### CI/CD

#### `.github/workflows/deploy.yml`
GitHub Actions workflow:
- Triggers on new releases
- Builds module tarball
- Uploads to Viam module registry

**Requires GitHub secrets**:
- `VIAM_API_KEY_ID`
- `VIAM_API_KEY`

### Ignore Files

#### `.gitignore`
Specifies files to exclude from version control:
- Python bytecode (`__pycache__`, `*.pyc`)
- Virtual environments (`.venv/`)
- Build artifacts (`module.tar.gz`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`)
- Sensitive configs (`config.json`)

## File Relationships

```
User runs: ./exec.sh
    ├─> Sources .env (environment variables)
    ├─> Runs ./setup.sh (install dependencies)
    └─> Executes src/main.py
            ├─> Imports src/__init__.py (registration)
            └─> Uses src/humidity_sensor.py (sensor logic)

User builds: make module.tar.gz
    └─> Packages: *.sh, .env, src/, requirements.txt, meta.json

User deploys: GitHub Release
    └─> Triggers .github/workflows/deploy.yml
            ├─> Builds module.tar.gz
            └─> Uploads to Viam
```

## Key Dependencies

### Runtime Dependencies
- **viam-sdk**: Core Viam platform integration
- **Adafruit-DHT**: DHT22 sensor communication
- **RPi.GPIO**: Raspberry Pi GPIO access

### System Dependencies
- **python3-venv**: Virtual environment support
- **python3-dev**: Python development headers (for compiling native extensions)
- **python3-pip**: Python package installer

## File Permissions

Files that should be executable:
- `exec.sh`
- `setup.sh`
- `test_hardware.py`

Set with: `chmod +x exec.sh setup.sh test_hardware.py`

## Customization Points

Before deploying, update these files:

1. **meta.json**: Replace `<your-username>` with your GitHub username
2. **pyproject.toml**: Update project URL with your GitHub username
3. **CHANGELOG.md**: Update URLs with your GitHub username

## Minimal Required Files

For the module to work, you MUST have:
- `src/humidity_sensor.py`
- `src/__init__.py`
- `src/main.py`
- `requirements.txt`
- `meta.json`
- `exec.sh`
- `setup.sh`
- `.env`

All other files are for documentation, testing, or development convenience.
