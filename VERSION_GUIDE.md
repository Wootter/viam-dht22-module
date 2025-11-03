# Using DHT22 Module Versions in Viam

## 📌 Version Overview

You have **two versions** of the DHT22 module available:

### Version 1.x (Old Structure)
- **Model**: `wootter:dht22-sensor:linux`
- **Versions**: v1.0.0 through v1.0.6
- **Structure**: Complex with GitHub Actions, build scripts
- **Status**: Legacy (still works)

### Version 2.0.0 (New Structure - CURRENT)
- **Model**: `wootter:sensor:dht22`
- **Versions**: v2.0.0
- **Structure**: Simple TEMT6000-style
- **Status**: Recommended ✅

## 🚀 Using Version 2.0.0 (Recommended)

### Step 1: Upload to Viam (One Time)

On your Raspberry Pi or Linux machine:

```bash
# Install Viam CLI (if not already installed)
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-arm64
sudo chmod +x /usr/local/bin/viam

# Login to Viam
viam login

# Navigate to your DHT22 directory
cd /path/to/DHT22

# Upload version 2.0.0
viam module upload --version 2.0.0 --platform linux/arm64
```

### Step 2: Add to Your Robot

#### Option A: Using Viam Web App (Easiest)

1. Go to https://app.viam.com
2. Select your robot
3. Go to **Config** tab
4. Click **Create component**
5. Select:
   - **Type**: `sensor`
   - **Model**: `wootter:sensor:dht22`
   - **Name**: `dht22` (or any name you want)
6. In **Attributes**, add:
   ```json
   {
     "pin": 4
   }
   ```
7. (Optional) In **Advanced** → **Module version**: Enter `2.0.0`
8. Click **Create**

#### Option B: Using JSON Config

In your robot's Config tab, switch to JSON mode and add:

```json
{
  "components": [
    {
      "name": "dht22",
      "model": "wootter:sensor:dht22",
      "type": "sensor",
      "namespace": "rdk",
      "attributes": {
        "pin": 4
      },
      "version": "2.0.0"
    }
  ]
}
```

### Step 3: Test It

1. Go to **Control** tab in Viam app
2. Find your `dht22` sensor
3. Click **Get Readings**
4. You should see:
   ```json
   {
     "temperature_celsius": 22.5,
     "humidity_percent": 45.2,
     "temperature_fahrenheit": 72.5
   }
   ```

## 🔄 Switching Between Versions

### From v1.x to v2.0.0

**Important**: These are **different models** with different names!

**Old Config (v1.x):**
```json
{
  "name": "dht22",
  "model": "wootter:dht22-sensor:linux",
  "type": "sensor",
  "namespace": "rdk",
  "attributes": {
    "pin": 4
  }
}
```

**New Config (v2.0.0):**
```json
{
  "name": "dht22",
  "model": "wootter:sensor:dht22",
  "type": "sensor",
  "namespace": "rdk",
  "attributes": {
    "pin": 4
  },
  "version": "2.0.0"
}
```

**To Switch:**
1. Delete the old component in Viam app
2. Create new component with model `wootter:sensor:dht22`
3. Same attributes work (just `pin` number)

## 📋 Comparison Table

| Feature | Version 1.x | Version 2.0.0 |
|---------|-------------|---------------|
| **Model Name** | `wootter:dht22-sensor:linux` | `wootter:sensor:dht22` |
| **Config** | Same attributes | Same attributes |
| **Structure** | Complex | Simple |
| **Upload Method** | GitHub Actions | Viam CLI |
| **Recommended** | ❌ Legacy | ✅ Current |

## 🎯 Which Version Should I Use?

### Use Version 2.0.0 if:
- ✅ Starting fresh
- ✅ Want simpler maintenance
- ✅ Following latest Viam patterns
- ✅ Easy to update

### Stay on Version 1.x if:
- ⚠️ Already deployed and working
- ⚠️ Don't want to reconfigure robots
- ⚠️ Will upgrade later at your convenience

## 🔍 Checking Your Current Version

### In Viam App

1. Go to your robot's **Config** tab
2. Find your DHT22 component
3. Look at the **model** field:
   - `wootter:dht22-sensor:linux` = Version 1.x
   - `wootter:sensor:dht22` = Version 2.0.0

### Via Viam CLI

```bash
# See what versions are available
viam module get wootter:sensor:dht22

# See what's on the registry
viam module list | grep dht22
```

## 📦 Uploading Future Updates

When you make changes:

```bash
# Commit changes
git add .
git commit -m "Your changes"
git push

# Tag new version
git tag v2.0.1 -m "Bug fixes"
git push origin v2.0.1

# Upload to Viam
viam module upload --version 2.0.1 --platform linux/arm64
```

## 🆘 Troubleshooting

### "Module not found"
- Make sure you uploaded it: `viam module list`
- Check you're logged in: `viam whoami`
- Upload it: `viam module upload --version 2.0.0 --platform linux/arm64`

### "Model not available"
- You might be looking for the old model name
- Use `wootter:sensor:dht22` (not `wootter:dht22-sensor:linux`)

### Sensor not reading
- Check GPIO pin number
- Verify wiring (VCC, GND, DATA)
- Check logs in Viam app
- Try `gpio readall` on Raspberry Pi

## ✅ Quick Start Checklist

- [ ] DHT22 sensor connected to GPIO pin
- [ ] Viam CLI installed on Raspberry Pi
- [ ] Logged into Viam: `viam login`
- [ ] Module uploaded: `viam module upload --version 2.0.0 --platform linux/arm64`
- [ ] Component added to robot config
- [ ] Model set to: `wootter:sensor:dht22`
- [ ] Pin configured in attributes
- [ ] Tested with "Get Readings"

---

**Need help?** Check the logs in your robot's **Logs** tab in the Viam app!
