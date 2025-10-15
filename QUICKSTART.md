# Quick Start Guide

This guide will help you get your DHT22 sensor module up and running quickly on your Raspberry Pi 4B.

## Hardware Setup

### What You Need
- Raspberry Pi 4B (or compatible)
- DHT22 (AM2302) sensor
- 3 jumper wires (Female-to-Female or Female-to-Male depending on your setup)
- Optional: 10kΩ resistor (if your DHT22 module doesn't have a built-in pull-up resistor)

### Wiring the DHT22

The DHT22 has 4 pins (left to right when facing the front):

```
DHT22 Pin    →    Raspberry Pi Pin
─────────────────────────────────────
Pin 1 (VCC)  →    Pin 1 (3.3V) or Pin 2 (5V)
Pin 2 (Data) →    Pin 7 (GPIO 4) - configurable
Pin 3 (NC)   →    Not connected
Pin 4 (GND)  →    Pin 6 (Ground)
```

**GPIO Pin Numbering:** This module uses BCM (Broadcom) pin numbering, not physical pin numbers. GPIO 4 is the default, but you can use any available GPIO pin.

### Popular GPIO Pins for DHT22

| Physical Pin | BCM/GPIO Number | Notes |
|--------------|-----------------|-------|
| Pin 7        | GPIO 4          | Default in examples |
| Pin 11       | GPIO 17         | Common alternative |
| Pin 12       | GPIO 18         | Common alternative |
| Pin 15       | GPIO 22         | Common alternative |

## Software Setup on Raspberry Pi

### Step 1: Install Viam Agent

```bash
sudo curl -o /usr/local/bin/viam-server https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage
sudo chmod 755 /usr/local/bin/viam-server
```

### Step 2: Clone and Setup This Module

```bash
cd ~
git clone https://github.com/<your-username>/viam-dht22-module.git
cd viam-dht22-module
```

### Step 3: Test the Sensor Locally (Optional)

Before integrating with Viam, test that your sensor works:

```bash
# Install dependencies
./setup.sh

# Run the test
.venv/bin/python src/humidity_sensor.py
```

You should see output like:
```
DHT22 Sensor Readings:
{'temperature_celsius': 23.5, 'humidity_percent': 45.2, 'temperature_fahrenheit': 74.3}
```

If you see an error, check your wiring and GPIO pin number.

## Viam Integration

### Step 1: Set Up Viam Robot

1. Go to [app.viam.com](https://app.viam.com)
2. Create a new robot or select an existing one
3. Follow the setup instructions to install the Viam agent on your Pi

### Step 2: Add the DHT22 Module

#### Option A: Upload as Local Module (Development)

1. On your Raspberry Pi, package the module:
   ```bash
   cd ~/viam-dht22-module
   make module.tar.gz
   ```

2. In the Viam app, go to your robot's config
3. Click "Modules" → "Add module" → "Local module"
4. Upload the `module.tar.gz` file

#### Option B: Use from Viam Registry (After Publishing)

1. In the Viam app, go to your robot's config
2. Click "Modules" → "Add module"
3. Search for "dht22-sensor"
4. Click "Add"

### Step 3: Configure the Sensor Component

Add this to your robot configuration (or use the UI):

```json
{
  "components": [
    {
      "name": "my_dht22",
      "namespace": "rdk",
      "type": "sensor",
      "model": "viam:dht22-sensor:linux",
      "attributes": {
        "pin": 4
      }
    }
  ]
}
```

**Important:** Change `"pin": 4` to match your actual GPIO pin number.

### Step 4: Test the Sensor

1. In the Viam app, navigate to your robot
2. Go to the "Control" tab
3. Find your DHT22 sensor component
4. Click "Get Readings"

You should see:
```json
{
  "temperature_celsius": 23.5,
  "temperature_fahrenheit": 74.3,
  "humidity_percent": 45.2
}
```

## Using the Sensor in Your Code

### Python SDK Example

```python
import asyncio
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions
from viam.components.sensor import Sensor

async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key='YOUR_API_KEY',
        api_key_id='YOUR_API_KEY_ID'
    )
    return await RobotClient.at_address('YOUR_ROBOT_ADDRESS', opts)

async def main():
    robot = await connect()
    
    # Get the DHT22 sensor
    dht22 = Sensor.from_robot(robot, "my_dht22")
    
    # Read sensor data
    readings = await dht22.get_readings()
    
    print(f"Temperature: {readings['temperature_celsius']:.1f}°C")
    print(f"Humidity: {readings['humidity_percent']:.1f}%")
    
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

### TypeScript SDK Example

```typescript
import { createRobotClient } from '@viamrobotics/sdk';

async function main() {
  const robot = await createRobotClient({
    host: 'YOUR_ROBOT_ADDRESS',
    credentials: {
      type: 'api-key',
      payload: 'YOUR_API_KEY',
    },
  });

  const dht22 = robot.getComponent('my_dht22');
  const readings = await dht22.getReadings();
  
  console.log(`Temperature: ${readings.temperature_celsius}°C`);
  console.log(`Humidity: ${readings.humidity_percent}%`);
}

main();
```

## Troubleshooting

### Sensor Returns "Failed to read" Error

**Possible causes:**
1. **Incorrect wiring** - Double-check all connections
2. **Wrong GPIO pin** - Verify the pin number in your config matches your wiring
3. **Power issues** - Ensure the sensor is getting 3.3V or 5V
4. **Missing pull-up resistor** - Some DHT22 modules need an external 10kΩ resistor
5. **Reading too frequently** - DHT22 needs 2 seconds between readings

**Solutions:**
```bash
# Check GPIO permissions
sudo usermod -a -G gpio $USER
# Then log out and log back in

# Test with a simple Python script
python3 -c "import Adafruit_DHT; print(Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4))"
```

### Module Not Found in Viam

1. Check that the module uploaded successfully
2. Verify the model name: `viam:dht22-sensor:linux`
3. Restart the Viam agent: `sudo systemctl restart viam-server`

### Permission Denied Errors

```bash
# Add your user to the gpio group
sudo usermod -a -G gpio $USER

# Or run viam-server with sudo (not recommended for production)
sudo systemctl edit viam-server
# Add: User=root
```

## Next Steps

- **Data Logging**: Use Viam's data management to log temperature/humidity over time
- **Automation**: Create triggers based on temperature/humidity thresholds
- **Visualization**: Build dashboards to monitor your environment
- **Multiple Sensors**: Add more DHT22 sensors on different GPIO pins

## Resources

- [Viam Documentation](https://docs.viam.com)
- [Viam Python SDK Docs](https://python.viam.dev/)
- [DHT22 Datasheet](https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)

## Support

- **Module Issues**: [GitHub Issues](https://github.com/<your-username>/viam-dht22-module/issues)
- **Viam Support**: [Discord](https://discord.gg/viam) or [Forum](https://support.viam.com)
