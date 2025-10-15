# DHT22 Sensor Module for Raspberry Pi

This repository contains a Viam-compatible module that enables a Raspberry Pi to read temperature and humidity data from a DHT22 (AM2302) sensor. This module integrates seamlessly with Viam's platform, making it easy to include environmental data in your robotics projects.

## Features

- Reads temperature in Celsius and Fahrenheit
- Reads relative humidity percentage
- Compatible with Raspberry Pi 4B (and other Raspberry Pi models with GPIO)
- Easy integration with Viam robotics platform
- Robust error handling and retry logic

## Hardware Requirements

- Raspberry Pi 4B (or compatible model with GPIO pins)
- DHT22 (AM2302) Temperature and Humidity Sensor
- Jumper wires for connections
- 10kΩ pull-up resistor (recommended, though many DHT22 modules have this built-in)

## Wiring

Connect the DHT22 sensor to your Raspberry Pi:

- **VCC (Pin 1)** → 3.3V or 5V on Raspberry Pi
- **Data (Pin 2)** → GPIO pin (default: GPIO 4, but configurable)
- **NC (Pin 3)** → Not connected
- **GND (Pin 4)** → Ground on Raspberry Pi

**Note:** Add a 10kΩ pull-up resistor between VCC and the Data pin if your DHT22 module doesn't have one built-in.

## Getting Started

### Prerequisites

- Raspberry Pi running Raspberry Pi OS (or compatible Linux distribution)
- DHT22 Temperature and Humidity Sensor
- Viam account and Viam agent installed on your Raspberry Pi
- Git installed on your Raspberry Pi

### Installation

1. Clone the repository to your Raspberry Pi:
   ```bash
   git clone https://github.com/<your-username>/viam-dht22-module.git
   cd viam-dht22-module
   ```

2. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Module Contents

- **src/**: Folder with Python code
  - `humidity_sensor.py`: Main sensor implementation
  - `__init__.py`: Module initialization
  - `main.py`: Module entry point
- **exec.sh**: Entrypoint script for when this runs as a module on a robot
- **setup.sh**: Dependencies setup script
- **Makefile**: Bundles your module into a tarball for distribution
- **.github/workflows/**: GitHub Actions workflow for automated deployment
- **meta.json**: Viam module configuration file
- **requirements.txt**: Python dependencies
- **.env**: Environment configuration for virtual environment

## Configuration

To use this module with Viam, add it to your robot configuration:

```json
{
  "components": [
    {
      "name": "my_dht22",
      "type": "sensor",
      "model": "viam:dht22-sensor:linux",
      "attributes": {
        "pin": 4
      },
      "depends_on": []
    }
  ]
}
```

**Configuration Options:**
- **pin** (required): The GPIO pin number where the DHT22 data pin is connected (using BCM numbering)

## Usage

After uploading and configuring the module in Viam, you can read sensor data from your robot dashboard or via the Viam SDK.

### Example Reading

The sensor returns the following data:

```json
{
  "temperature_celsius": 23.5,
  "temperature_fahrenheit": 74.3,
  "humidity_percent": 45.2
}
```

### Using the Viam Python SDK

```python
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor

async def main():
    # Connect to your robot
    robot = await RobotClient.at_address('<your-robot-address>')
    
    # Get the DHT22 sensor
    dht22 = Sensor.from_robot(robot, "my_dht22")
    
    # Get readings
    readings = await dht22.get_readings()
    print(f"Temperature: {readings['temperature_celsius']}°C")
    print(f"Humidity: {readings['humidity_percent']}%")
    
    await robot.close()
```

## Development

### Local Testing

You can test the sensor locally without Viam:

```bash
python3 src/humidity_sensor.py
```

Make sure to update the GPIO pin number in the test code if needed.

### Building the Module

To package the module for distribution:

```bash
make module.tar.gz
```

This creates a tarball that can be uploaded to the Viam registry.

## Uploading to Viam

1. Update the `meta.json` file with your GitHub username and module information
2. Create a GitHub release
3. The GitHub Actions workflow will automatically build and upload the module to Viam

Alternatively, you can manually upload using the Viam CLI:

```bash
viam module upload --version <version> --platform linux/arm64 module.tar.gz
```

## Troubleshooting

### Sensor Returns Errors

- Check wiring connections
- Verify the GPIO pin number in the configuration
- Ensure the DHT22 sensor is receiving proper power (3.3V or 5V)
- Check if a pull-up resistor is in place
- The DHT22 has a 2-second minimum interval between readings

### Permission Issues

If you encounter GPIO permission issues, ensure the Viam agent is running with appropriate permissions or add your user to the `gpio` group:

```bash
sudo usermod -a -G gpio $USER
```

## DHT22 vs DHT11

This module is specifically for the DHT22 sensor. The DHT22 offers:
- Higher precision (±0.5°C for temperature, ±2% for humidity)
- Wider range (-40 to 80°C vs 0 to 50°C)
- Better accuracy compared to the DHT11

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Based on the Viam module structure
- Uses the Adafruit_DHT library for sensor communication
- Inspired by the viam-dht11-module by Gaurang-1402

## Support

For issues related to:
- **This module**: Open an issue in this repository
- **Viam platform**: Visit [Viam documentation](https://docs.viam.com) or [Viam Discord](https://discord.gg/viam)
- **DHT22 sensor**: Refer to the [Adafruit DHT22 guide](https://learn.adafruit.com/dht)

## Links

- [Viam Documentation](https://docs.viam.com)
- [Viam Python SDK](https://python.viam.dev/)
- [Adafruit DHT Library](https://github.com/adafruit/Adafruit_Python_DHT)
