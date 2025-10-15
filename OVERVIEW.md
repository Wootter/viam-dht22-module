# 🎯 Viam DHT22 Module - Complete Package

## 📦 What You Have

A **production-ready Viam module** for the DHT22 temperature and humidity sensor, designed specifically for Raspberry Pi 4B.

### ✨ Key Features

- ✅ **Temperature readings** in Celsius and Fahrenheit
- ✅ **Humidity readings** in percentage
- ✅ **Configurable GPIO pin** selection
- ✅ **Robust error handling** with retry logic
- ✅ **Complete documentation** and guides
- ✅ **Automated deployment** via GitHub Actions
- ✅ **Hardware testing** script included
- ✅ **Production-ready** code structure

## 📂 Complete File List (21 files)

### Core Module Files (8)
```
✅ src/humidity_sensor.py    - DHT22 sensor implementation
✅ src/__init__.py            - Module registration
✅ src/main.py                - Entry point
✅ requirements.txt           - Python dependencies
✅ meta.json                  - Viam module config
✅ exec.sh                    - Execution script
✅ setup.sh                   - Setup script
✅ .env                       - Environment variables
```

### Documentation (8)
```
📖 README.md                  - Main documentation
📖 QUICKSTART.md              - Quick start guide
📖 CONTRIBUTING.md            - Contribution guidelines
📖 PROJECT_SUMMARY.md         - Project overview
📖 FILE_STRUCTURE.md          - File structure guide
📖 DEPLOYMENT_CHECKLIST.md    - Pre-deployment checklist
📖 CHANGELOG.md               - Version history
📖 LICENSE                    - Apache 2.0 license
```

### Configuration & Build (5)
```
⚙️ config.example.json        - Example robot config
⚙️ pyproject.toml             - Python project config
⚙️ Makefile                   - Build commands
⚙️ .gitignore                 - Git ignore patterns
⚙️ .github/workflows/deploy.yml - GitHub Actions
```

### Testing & Development (1)
```
🧪 test_hardware.py           - Hardware testing script
```

## 🔌 Hardware Setup

```
┌─────────────────────────────────────────────────┐
│         DHT22                 Raspberry Pi 4B   │
│  ┌────────────┐                                 │
│  │ 1 2 3 4    │                                 │
│  └─┬─┬─┬─┬────┘                                 │
│    │ │ │ │                                      │
│    │ │ │ └────────────────────────> GND        │
│    │ │ └── NC (not connected)                  │
│    │ └──────────────┬──────────────> GPIO 4    │
│    │          10kΩ  │                           │
│    │          Pull-up                           │
│    └────────────────┴──────────────> 3.3V/5V   │
│                                                 │
└─────────────────────────────────────────────────┘

Pin Configuration (BCM numbering):
• VCC → 3.3V or 5V
• Data → GPIO 4 (configurable)
• GND → Ground
```

## 📊 Data Format

### Successful Reading
```json
{
  "temperature_celsius": 23.5,
  "temperature_fahrenheit": 74.3,
  "humidity_percent": 45.2
}
```

### Error Response
```json
{
  "error": "Failed to read from DHT22 sensor",
  "pin": 4
}
```

## 🚀 Quick Deployment Guide

### 1️⃣ Customize
```bash
# Update these files with your GitHub username:
• meta.json (line 3)
• pyproject.toml (line 30-33)
• CHANGELOG.md (bottom URLs)
```

### 2️⃣ Test Hardware
```bash
python3 test_hardware.py --pin 4
```

### 3️⃣ Deploy
```bash
git add .
git commit -m "Initial release"
git tag v1.0.0
git push origin main --tags
```

### 4️⃣ GitHub Release
- Create release on GitHub
- GitHub Actions auto-deploys to Viam

## 🔧 Viam Configuration

Add to your robot config:
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

## 💻 Code Examples

### Python
```python
from viam.robot.client import RobotClient
from viam.components.sensor import Sensor

robot = await RobotClient.at_address('ADDRESS')
dht22 = Sensor.from_robot(robot, "my_dht22")
readings = await dht22.get_readings()
print(f"Temp: {readings['temperature_celsius']}°C")
```

### TypeScript
```typescript
const robot = await createRobotClient({...});
const dht22 = robot.getComponent('my_dht22');
const readings = await dht22.getReadings();
console.log(`Temp: ${readings.temperature_celsius}°C`);
```

## 📈 Specifications

| Feature | DHT22 (AM2302) |
|---------|----------------|
| Temperature Range | -40°C to 80°C |
| Humidity Range | 0% to 100% |
| Temperature Accuracy | ±0.5°C |
| Humidity Accuracy | ±2% |
| Reading Interval | 2 seconds minimum |
| Operating Voltage | 3.3V - 5V |

## 🎓 Learning Resources

### Viam
- [Viam Docs](https://docs.viam.com)
- [Python SDK](https://python.viam.dev/)
- [Discord Community](https://discord.gg/viam)

### DHT22
- [Datasheet](https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf)
- [Adafruit Tutorial](https://learn.adafruit.com/dht)

### Raspberry Pi
- [GPIO Pinout](https://pinout.xyz/)
- [RPi.GPIO Docs](https://sourceforge.net/p/raspberry-gpio-python/wiki/)

## ⚠️ Common Issues & Solutions

### "Failed to read from DHT22"
```bash
# Check wiring
# Verify GPIO pin number
# Ensure 10kΩ pull-up resistor
# Wait 2+ seconds between readings
```

### "Permission denied" on GPIO
```bash
sudo usermod -a -G gpio $USER
# Log out and back in
```

### Module not found in Viam
```bash
# Check model name: viam:dht22-sensor:linux
sudo systemctl restart viam-server
```

## 🎯 Next Steps

1. ✅ **Test on hardware** - Run `test_hardware.py`
2. ✅ **Update configs** - Add your GitHub username
3. ✅ **Push to GitHub** - Commit and push
4. ✅ **Create release** - Tag and release on GitHub
5. ✅ **Deploy to robot** - Add module in Viam UI
6. ✅ **Start monitoring** - View data in Viam dashboard

## 🏆 You're Ready!

This module is **production-ready** and includes:
- ✅ Complete implementation
- ✅ Comprehensive documentation
- ✅ Testing utilities
- ✅ Automated deployment
- ✅ Example configurations
- ✅ Troubleshooting guides

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/<your-username>/viam-dht22-module/issues)
- **Viam Help**: [Discord](https://discord.gg/viam)
- **Documentation**: All included in this repo!

---

**Made with ❤️ for the Viam community**

*Based on the DHT11 module by Gaurang-1402, adapted for DHT22*
