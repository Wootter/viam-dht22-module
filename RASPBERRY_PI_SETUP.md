# 🚀 Deployment Steps - From Windows Laptop to Raspberry Pi

You've completed the configuration on your Windows laptop. Here's what to do next:

## Step 1: Push Code to GitHub (Do this on your laptop NOW)

### Initialize Git Repository (if not already done)
```powershell
# Open PowerShell in your project directory
cd "C:\Users\WoutDeelen\Desktop\github\Github Respitories\DHT22"

# Initialize git (if needed)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial DHT22 Viam module for Raspberry Pi 4B"

# Create GitHub repository (do this on github.com first!)
# Then link it:
git remote add origin https://github.com/<YOUR-USERNAME>/viam-dht22-module.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Set Up Your Raspberry Pi 4B

### Connect to Your Raspberry Pi
```bash
# SSH into your Pi from your laptop
ssh pi@<your-pi-ip-address>
# Default password is usually 'raspberry' if not changed
```

### Install Prerequisites on Raspberry Pi
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
sudo apt-get install -y python3 python3-pip python3-venv python3-dev git

# Install GPIO libraries
sudo apt-get install -y python3-rpi.gpio
```

## Step 3: Clone Repository on Raspberry Pi

```bash
# On your Raspberry Pi, clone the repo
cd ~
git clone https://github.com/<YOUR-USERNAME>/viam-dht22-module.git
cd viam-dht22-module
```

## Step 4: Wire Your DHT22 Sensor

Before testing, connect your DHT22 to the Raspberry Pi:

```
DHT22 Pin 1 (VCC)  → Pi Pin 1 (3.3V) or Pin 2 (5V)
DHT22 Pin 2 (Data) → Pi Pin 7 (GPIO 4)
DHT22 Pin 3 (NC)   → Not connected
DHT22 Pin 4 (GND)  → Pi Pin 6 (Ground)

Optional: 10kΩ resistor between VCC and Data pin
```

## Step 5: Test Hardware on Raspberry Pi

```bash
# Make scripts executable
chmod +x exec.sh setup.sh test_hardware.py

# Run setup to install Python dependencies
./setup.sh

# Test the sensor
python3 test_hardware.py --pin 4
```

**Expected output:**
```
============================================================
DHT22 Sensor Test Script
============================================================
Testing DHT22 on GPIO pin 4 (BCM numbering)
Taking 5 readings with 3-second intervals...

Reading 1/5...
  ✓ Temperature: 23.5°C (74.3°F)
  ✓ Humidity: 45.2%
...
```

If you see errors, check:
- Wiring connections
- GPIO pin number (change with `--pin` flag)
- Power supply to sensor

## Step 6: Install Viam on Raspberry Pi

### Install Viam Agent
```bash
# Download Viam server for ARM64 (Raspberry Pi 4B)
sudo curl -o /usr/local/bin/viam-server \
  https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-aarch64.AppImage

# Make it executable
sudo chmod 755 /usr/local/bin/viam-server

# Install as a service
sudo viam-server --install
```

### Configure Viam Robot

1. Go to https://app.viam.com
2. Create account or sign in
3. Create a new robot (or use existing)
4. Copy the robot setup command
5. Run it on your Pi:
   ```bash
   # The command will look like:
   sudo viam-server --config /path/to/config
   ```

## Step 7: Add DHT22 Module to Viam

### Option A: Upload as Local Module (Recommended for Testing)

1. **On Raspberry Pi**, package the module:
   ```bash
   cd ~/viam-dht22-module
   make module.tar.gz
   ```

2. **Copy to your laptop** (from laptop PowerShell):
   ```powershell
   scp pi@<your-pi-ip>:~/viam-dht22-module/module.tar.gz ./module.tar.gz
   ```

3. **In Viam web app**:
   - Go to your robot's page
   - Click "Config" tab
   - Click "Modules" → "Add Module" → "Local Module"
   - Upload `module.tar.gz`
   - Click "Add Module"

### Option B: Publish to Viam Registry (For Production)

1. **Set up GitHub Secrets** (on github.com):
   - Go to your repo → Settings → Secrets and variables → Actions
   - Add secrets:
     - `VIAM_API_KEY_ID` (from app.viam.com → Settings → API Keys)
     - `VIAM_API_KEY` (from app.viam.com → Settings → API Keys)

2. **Create GitHub Release**:
   ```powershell
   # On your laptop
   git tag v1.0.0
   git push origin v1.0.0
   ```
   - Go to GitHub → Releases → Create new release
   - Select tag v1.0.0
   - Publish release
   - GitHub Actions will auto-deploy

## Step 8: Configure DHT22 Component in Viam

In Viam web app:

1. Go to your robot → Config tab
2. Click "Components" → "Create Component"
3. Select type: "Sensor"
4. Select model: `viam:dht22-sensor:linux`
5. Name it: `my_dht22`
6. In JSON editor, add:
   ```json
   {
     "pin": 4
   }
   ```
7. Click "Save Config"

## Step 9: Test in Viam

1. Go to "Control" tab
2. Find your `my_dht22` sensor
3. Click "Get Readings"
4. You should see:
   ```json
   {
     "temperature_celsius": 23.5,
     "temperature_fahrenheit": 74.3,
     "humidity_percent": 45.2
   }
   ```

## 🎉 Success! Next Steps

### Use the Data

**Python SDK Example:**
```python
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
    dht22 = Sensor.from_robot(robot, "my_dht22")
    readings = await dht22.get_readings()
    print(f"Temperature: {readings['temperature_celsius']:.1f}°C")
    print(f"Humidity: {readings['humidity_percent']:.1f}%")
    await robot.close()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

### Enable Data Capture

In Viam config, add data capture:
```json
{
  "name": "my_dht22",
  "type": "sensor",
  "model": "viam:dht22-sensor:linux",
  "attributes": {
    "pin": 4
  },
  "service_configs": [
    {
      "type": "data_manager",
      "attributes": {
        "capture_methods": [
          {
            "method": "Readings",
            "frequency_hz": 0.1
          }
        ]
      }
    }
  ]
}
```

This captures data every 10 seconds!

## 🔧 Troubleshooting

### "Module not found"
```bash
# Check module uploaded correctly
ls ~/viam-dht22-module/module.tar.gz

# Rebuild if needed
cd ~/viam-dht22-module
make clean
make module.tar.gz
```

### "Failed to read sensor"
```bash
# Test hardware again
python3 test_hardware.py --pin 4

# Check permissions
sudo usermod -a -G gpio $USER
sudo reboot
```

### "Import errors"
```bash
# Reinstall dependencies
cd ~/viam-dht22-module
rm -rf .venv
./setup.sh
```

## 📋 Quick Reference Commands

### On Laptop (Windows)
```powershell
# Push changes
git add .
git commit -m "Update"
git push

# SSH to Pi
ssh pi@<pi-ip>
```

### On Raspberry Pi
```bash
# Update code
cd ~/viam-dht22-module
git pull

# Test hardware
python3 test_hardware.py --pin 4

# Rebuild module
make module.tar.gz

# Check Viam logs
sudo journalctl -u viam-server -f
```

## 🎯 Summary Checklist

- [ ] Git repository created on GitHub
- [ ] Code pushed from laptop
- [ ] Raspberry Pi connected and updated
- [ ] Repository cloned on Pi
- [ ] DHT22 sensor wired correctly
- [ ] Hardware test passes
- [ ] Viam agent installed on Pi
- [ ] Module uploaded to Viam
- [ ] Component configured in Viam
- [ ] Readings working in Viam UI

---

**You're all set!** Your DHT22 module is now running on your Raspberry Pi 4B with Viam! 🎉
