# Upload DHT22 Module to Viam

This guide shows how to upload your DHT22 module to Viam registry.

## Prerequisites

1. **Viam CLI installed** on your Raspberry Pi or development machine
2. **Viam API key** (get from https://app.viam.com)

## Installation

### Install Viam CLI

On your Raspberry Pi:

```bash
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-arm64
sudo chmod +x /usr/local/bin/viam
```

Or on Linux/Mac:

```bash
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod +x /usr/local/bin/viam
```

## Upload Module

### 1. Login to Viam

```bash
viam login
```

Or with API key:

```bash
viam login api-key --key-id="YOUR_KEY_ID" --key="YOUR_KEY"
```

### 2. Create Module (First Time Only)

```bash
viam module create --name sensor --public-namespace wootter
```

### 3. Upload Module

From the DHT22 directory:

```bash
cd /path/to/DHT22
viam module upload --version 1.0.0 --platform linux/arm64
```

Or upload from tarball:

```bash
tar -czf dht22-module.tar.gz src/ run.sh requirements.txt meta.json
viam module upload --version 1.0.0 --platform linux/arm64 --module dht22-module.tar.gz
```

## Using the Module

### In Viam App

1. Go to https://app.viam.com
2. Navigate to your robot's **Config** tab
3. Click **Create component** → **sensor**
4. Select model: `wootter:sensor:dht22`
5. Configure:

```json
{
  "pin": 4
}
```

### Configuration

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
      }
    }
  ]
}
```

## Testing Locally

Test the module on your Raspberry Pi:

```bash
cd /path/to/DHT22
./run.sh
```

## Readings

The sensor returns:

```json
{
  "temperature_celsius": 22.5,
  "humidity_percent": 45.2,
  "temperature_fahrenheit": 72.5
}
```

## Troubleshooting

### Module Not Found
- Ensure you're logged in: `viam whoami`
- Check module exists: `viam module list`

### Permission Errors
- Make sure `run.sh` is executable: `chmod +x run.sh`
- Check GPIO permissions

### Sensor Errors
- Verify wiring
- Check GPIO pin number
- Wait 2-3 seconds between readings
