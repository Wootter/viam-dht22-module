# Viam DHT22 Module - Project Summary

## Overview
This is a complete Viam module for the DHT22 (AM2302) temperature and humidity sensor, designed to run on Raspberry Pi 4B. It's based on the viam-dht11-module structure but adapted specifically for the DHT22 sensor.

## What's Been Created

### Core Module Files
- **src/humidity_sensor.py** - Main sensor implementation using Adafruit_DHT library
- **src/__init__.py** - Module registration
- **src/main.py** - Entry point for the Viam module

### Configuration Files
- **.env** - Environment variables for virtual environment
- **requirements.txt** - Python dependencies (viam-sdk, Adafruit-DHT, RPi.GPIO)
- **meta.json** - Viam module metadata and configuration
- **config.example.json** - Example robot configuration

### Setup Scripts
- **exec.sh** - Module execution script (called by Viam)
- **setup.sh** - Dependency installation script
- **Makefile** - Build commands for packaging the module

### Documentation
- **README.md** - Complete project documentation
- **QUICKSTART.md** - Step-by-step setup guide
- **CONTRIBUTING.md** - Contribution guidelines
- **LICENSE** - Apache 2.0 license

### Testing & Deployment
- **test_hardware.py** - Hardware testing script
- **.github/workflows/deploy.yml** - Automated deployment to Viam
- **.gitignore** - Git ignore patterns

## Key Differences from DHT11 Module

1. **Sensor Type**: Uses `Adafruit_DHT.DHT22` instead of custom dht11 library
2. **Better Accuracy**: DHT22 provides ±0.5°C temperature and ±2% humidity accuracy
3. **Wider Range**: -40 to 80°C (vs 0-50°C for DHT11)
4. **Additional Output**: Returns temperature in both Celsius and Fahrenheit
5. **Robust Reading**: Uses `Adafruit_DHT.read_retry()` for reliability

## Module Configuration

The module expects this configuration in your Viam robot:

```json
{
  "name": "my_dht22",
  "type": "sensor",
  "model": "viam:dht22-sensor:linux",
  "attributes": {
    "pin": 4
  }
}
```

**Pin**: GPIO pin number using BCM (Broadcom) numbering

## Sensor Readings Format

The module returns:
```json
{
  "temperature_celsius": 23.5,
  "temperature_fahrenheit": 74.3,
  "humidity_percent": 45.2
}
```

On error:
```json
{
  "error": "Failed to read from DHT22 sensor",
  "pin": 4
}
```

## Before You Deploy

### 1. Update meta.json
Replace `<your-username>` with your GitHub username:
```json
"url": "https://github.com/<your-username>/viam-dht22-module"
```

### 2. Test Hardware
On your Raspberry Pi:
```bash
python3 test_hardware.py --pin 4
```

### 3. Set Up Viam Credentials
For automated deployment, add these GitHub secrets:
- `VIAM_API_KEY_ID`
- `VIAM_API_KEY`

## Deployment Options

### Option 1: Local Module (Development)
```bash
make module.tar.gz
# Upload module.tar.gz through Viam UI
```

### Option 2: GitHub Release (Production)
```bash
git tag v1.0.0
git push origin v1.0.0
# Create GitHub release - automatic deployment via Actions
```

### Option 3: Manual Upload
```bash
viam module upload --version 1.0.0 --platform linux/arm64 module.tar.gz
```

## Hardware Wiring

```
DHT22          Raspberry Pi 4B
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pin 1 (VCC)  → 3.3V or 5V
Pin 2 (Data) → GPIO 4 (or your chosen pin)
Pin 3 (NC)   → Not connected  
Pin 4 (GND)  → Ground

Note: 10kΩ pull-up resistor recommended between VCC and Data
```

## Next Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial DHT22 Viam module"
   git remote add origin https://github.com/<your-username>/viam-dht22-module.git
   git push -u origin main
   ```

2. **Test on Raspberry Pi**
   - Clone the repo on your Pi
   - Run `./setup.sh`
   - Test with `python3 test_hardware.py`

3. **Deploy to Viam**
   - Update `meta.json` with your details
   - Create a GitHub release
   - Module will auto-deploy via GitHub Actions

4. **Configure in Viam**
   - Add module to your robot
   - Configure with your GPIO pin
   - Start reading temperature and humidity!

## Troubleshooting

### Common Issues

**"Failed to read from DHT22"**
- Check wiring
- Verify GPIO pin number
- Ensure pull-up resistor is present
- Wait 2+ seconds between readings

**"Permission denied" on GPIO**
```bash
sudo usermod -a -G gpio $USER
# Log out and log back in
```

**Module not found in Viam**
- Check `meta.json` configuration
- Verify model name: `viam:dht22-sensor:linux`
- Restart Viam agent: `sudo systemctl restart viam-server`

## Support & Resources

- **Viam Docs**: https://docs.viam.com
- **Viam Python SDK**: https://python.viam.dev/
- **DHT22 Datasheet**: https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf
- **Raspberry Pi GPIO**: https://pinout.xyz/

## Project Status

✅ Module structure complete
✅ DHT22 sensor implementation
✅ Viam integration
✅ Documentation complete
✅ Testing script included
✅ CI/CD workflow ready

**Ready for deployment!**
