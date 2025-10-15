# 🔍 Deployment Verification Guide

## ✅ Current Status

**Organization ID:** `0cac329d-21db-487a-a4aa-75b9a8308030`  
**Organization Name:** Wootter  
**Module Namespace:** `wootter:dht22-sensor` ✅ CORRECT

All files are properly configured with the `wootter` namespace.

---

## 📋 Pre-Deployment Checklist

### 1. ✅ Code Configuration
- [x] meta.json uses `wootter:dht22-sensor`
- [x] src/humidity_sensor.py uses `wootter`
- [x] Code committed and pushed to GitHub
- [x] Git tag v1.0.0 created and pushed

### 2. 🔐 GitHub Secrets (VERIFY NOW!)

Go to: https://github.com/Wootter/viam-dht22-module/settings/secrets/actions

**You should have TWO secrets:**

#### Secret #1: VIAM_API_KEY_ID
- **Name:** `VIAM_API_KEY_ID`
- **Value:** The Key ID from your Viam API key (shorter string)
- Example format: `abc123def456` or similar

#### Secret #2: VIAM_API_KEY
- **Name:** `VIAM_API_KEY`
- **Value:** The full API key from Viam (long string)
- Example format: Starts with something like `viam_api_key_...`

**How to verify:**
1. Click the link above
2. You should see both secrets listed
3. If missing, add them now!

**To get these values:**
1. Go to https://app.viam.com
2. Profile → Settings → API Keys
3. You should see "GitHub Actions Deploy" key
4. Click to reveal the Key ID and Key

---

## 🚀 Deployment Steps

### Step 1: Verify GitHub Secrets
**DO THIS NOW:**
```
1. Go to: https://github.com/Wootter/viam-dht22-module/settings/secrets/actions
2. Verify you see:
   ✓ VIAM_API_KEY_ID
   ✓ VIAM_API_KEY
```

### Step 2: Create GitHub Release
**Once secrets are verified:**

1. Go to: https://github.com/Wootter/viam-dht22-module/releases/new
2. **Choose tag:** v1.0.0
3. **Release title:** `v1.0.0 - DHT22 Sensor Module`
4. **Description:**
   ```
   Initial release of DHT22 temperature and humidity sensor module for Raspberry Pi 4B
   
   🌡️ Features:
   - Temperature readings in Celsius and Fahrenheit
   - Relative humidity percentage
   - Configurable GPIO pin
   - Raspberry Pi 4B compatible
   - Built on Adafruit_DHT library
   
   📦 Installation:
   Search for "wootter/dht22-sensor" in Viam module registry
   
   🔧 Configuration:
   Model: wootter:dht22-sensor:linux
   Attributes: {"pin": 4}
   ```
5. Click **"Publish release"**

### Step 3: Monitor GitHub Actions

**Immediately after publishing:**

1. Go to: https://github.com/Wootter/viam-dht22-module/actions
2. You should see "Deploy Viam Module" workflow running
3. Click on it to watch progress
4. **Expected duration:** 2-5 minutes

**What happens:**
- ✓ Checks out code
- ✓ Sets up Python
- ✓ Installs Viam CLI
- ✓ Builds module.tar.gz
- ✓ Authenticates with Viam
- ✓ Uploads module to Viam registry

**Success indicators:**
- All steps show green checkmarks ✅
- Last step says "Upload module to Viam" completes
- No red X marks

**If it fails:**
- Click on the failed step to see error logs
- Common issues:
  - Missing GitHub secrets
  - Wrong API key
  - Network timeout (just re-run)

### Step 4: Wait for Registry Sync

**After GitHub Actions succeeds:**
- Wait **5 minutes** for Viam to sync the module
- The module needs to propagate through Viam's registry

### Step 5: Find Module in Viam

1. Go to https://app.viam.com
2. Select your robot (or create one if you haven't)
3. Click **"Config"** tab
4. Click **"Modules"** → **"+ Create module"**
5. Select **"Registry module"**
6. In the search box, type: **"wootter"** or **"dht22"**
7. You should see: **wootter/dht22-sensor**
8. Click **"Add module"**

### Step 6: Add Sensor Component

1. Still in Config tab
2. Click **"Components"** → **"+ Create component"**
3. **Type:** sensor
4. **Model:** Type `wootter:dht22-sensor:linux` 
   - It should appear in the dropdown
5. **Name:** `my_dht22` (or any name you prefer)
6. Click **"Create"**
7. In the configuration panel, ensure attributes show:
   ```json
   {
     "pin": 4
   }
   ```
   (Change 4 to your actual GPIO pin)
8. Click **"Save config"** (top right)

### Step 7: Test Your Sensor! 🎉

**Prerequisites for testing:**
- DHT22 sensor must be connected to your Raspberry Pi
- Raspberry Pi must be running and connected to Viam
- Viam agent must be installed on Pi

**To test:**
1. Go to **"Control"** tab in Viam
2. Find **"my_dht22"** in the components list
3. Expand it
4. Click **"Get Readings"** button

**Expected output:**
```json
{
  "temperature_celsius": 23.5,
  "temperature_fahrenheit": 74.3,
  "humidity_percent": 45.2
}
```

**If you get an error:**
- Check sensor wiring
- Verify GPIO pin number
- Ensure Raspberry Pi has module installed
- Check Viam logs on Pi: `sudo journalctl -u viam-server -f`

---

## 🔧 Troubleshooting

### "Module not found in registry"

**Possible causes:**
1. GitHub Actions didn't complete successfully
   - Check: https://github.com/Wootter/viam-dht22-module/actions
2. Not enough time passed (wait 5-10 minutes)
3. Wrong namespace used
   - Verify `wootter` matches your org name

**Solutions:**
- Wait longer (up to 10 minutes)
- Check GitHub Actions for errors
- Verify secrets are set correctly

### "GitHub Actions failed"

**Common errors and fixes:**

**Error: "viam: command not found"**
- The workflow should install it automatically
- Check the "Install Viam CLI" step

**Error: "Authentication failed"**
- Check GitHub secrets are set:
  - VIAM_API_KEY_ID
  - VIAM_API_KEY
- Verify API key is still valid in Viam

**Error: "Permission denied"**
- API key might not have upload permissions
- Regenerate API key in Viam with full permissions

### "Sensor readings fail"

**On Raspberry Pi, test hardware:**
```bash
cd ~/viam-dht22-module
python3 test_hardware.py --pin 4
```

**If that works but Viam doesn't:**
- Check Viam logs: `sudo journalctl -u viam-server -f`
- Verify module uploaded correctly
- Try restarting Viam: `sudo systemctl restart viam-server`

---

## 📊 Deployment Timeline

| Step | Duration | Action Required |
|------|----------|-----------------|
| Verify GitHub secrets | 1 min | ✋ YOU |
| Create GitHub release | 1 min | ✋ YOU |
| GitHub Actions run | 2-5 min | ⏳ Wait |
| Registry sync | 5-10 min | ⏳ Wait |
| Add module in Viam | 2 min | ✋ YOU |
| Configure component | 1 min | ✋ YOU |
| Test readings | 30 sec | ✋ YOU |
| **TOTAL** | **~15-20 min** | |

---

## ✅ Quick Verification Commands

**Check if GitHub Actions ran:**
```
Visit: https://github.com/Wootter/viam-dht22-module/actions
Look for: Green checkmark on "Deploy Viam Module"
```

**Check if module is in registry:**
```
1. Go to https://app.viam.com
2. Any robot → Config → Modules → + Create module → Registry module
3. Search: "wootter"
4. Should appear: wootter/dht22-sensor
```

**Check component works:**
```
Control tab → my_dht22 → Get Readings
Should return: temperature and humidity values
```

---

## 🎯 Summary: What You Need to Do NOW

1. ✅ **Verify GitHub Secrets** (2 minutes)
   - https://github.com/Wootter/viam-dht22-module/settings/secrets/actions
   - Must have: VIAM_API_KEY_ID and VIAM_API_KEY

2. ✅ **Create GitHub Release** (2 minutes)
   - https://github.com/Wootter/viam-dht22-module/releases/new
   - Tag: v1.0.0
   - Click Publish

3. ⏳ **Wait for Actions** (5 minutes)
   - https://github.com/Wootter/viam-dht22-module/actions
   - Watch for green checkmark

4. ⏳ **Wait for Registry** (5 minutes)
   - Just wait, nothing to do

5. ✅ **Add Module** (5 minutes)
   - app.viam.com → Config → Modules → Add
   - Search "wootter"

6. ✅ **Test** (1 minute)
   - Control → my_dht22 → Get Readings

**START HERE:** Verify your GitHub secrets are set!
