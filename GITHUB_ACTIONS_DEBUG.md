# 🔧 GitHub Actions Troubleshooting

## ❌ Your workflows failed - here's how to fix it

Both workflow runs failed after 8-10 seconds. This is usually caused by one of these issues:

---

## 🔍 Step 1: Check the Error Log

**Do this NOW:**

1. Go to: https://github.com/Wootter/viam-dht22-module/actions
2. Click on the **most recent** failed run (the top one)
3. Click on the **"publish"** job
4. Look at which step failed (will have a red X)
5. Click on that step to see the error message

**Tell me what the error says!** Common errors:

### Error: "VIAM_API_KEY_ID: not set" or "VIAM_API_KEY: not set"
**Cause:** GitHub secrets are missing  
**Fix:** See Step 2 below

### Error: "viam: command not found"
**Cause:** Viam CLI installation failed  
**Fix:** Already fixed in latest commit

### Error: "make: command not found" or "tar: command not found"
**Cause:** Build tools missing  
**Fix:** Workflow should have these, but let me know

### Error: "authentication failed" or "401 Unauthorized"
**Cause:** Wrong API key or expired  
**Fix:** Regenerate API key (see Step 3)

---

## 🔐 Step 2: Verify GitHub Secrets

**CRITICAL - Do this:**

1. Go to: https://github.com/Wootter/viam-dht22-module/settings/secrets/actions

2. You should see **exactly 2 secrets**:
   ```
   VIAM_API_KEY_ID
   VIAM_API_KEY
   ```

3. **If you DON'T see both secrets:**

   **Add them now:**
   
   a) Get your API key from Viam:
      - Go to: https://app.viam.com
      - Click profile → Settings → API Keys
      - Find "GitHub Actions Deploy" (or create new)
      - Copy the **Key ID** and **Key**

   b) Add to GitHub:
      - Click "New repository secret"
      - Name: `VIAM_API_KEY_ID`
      - Value: (paste the Key ID)
      - Click "Add secret"
      
      - Click "New repository secret" again
      - Name: `VIAM_API_KEY`
      - Value: (paste the full Key - starts with something like `viam_api_key_...`)
      - Click "Add secret"

---

## 🔄 Step 3: Regenerate API Key (if needed)

**If secrets exist but authentication fails:**

1. Go to: https://app.viam.com
2. Click profile → Settings → API Keys
3. Find your existing "GitHub Actions Deploy" key
4. Click **"Delete"** or create a new one
5. Click **"Generate API Key"**
   - Name: `GitHub Actions Deploy`
   - Organization: Wootter
   - Permissions: Leave default (full access)
6. **COPY BOTH:**
   - Key ID (shorter)
   - Key (long string starting with `viam_api_key_...`)
7. Update GitHub secrets with new values

---

## ♻️ Step 4: Re-run the Workflow

**After fixing secrets:**

### Option A: Re-run Existing Workflow
1. Go to: https://github.com/Wootter/viam-dht22-module/actions
2. Click on the failed run
3. Click **"Re-run all jobs"** button (top right)
4. Wait for it to complete

### Option B: Delete and Recreate Release

1. **Delete old release:**
   - Go to: https://github.com/Wootter/viam-dht22-module/releases
   - Click on v1.0.0
   - Click "Delete" button
   - Confirm deletion

2. **Update tag:**
   ```powershell
   cd "C:\Users\WoutDeelen\Desktop\github\Github Respitories\DHT22"
   git tag -d v1.0.0
   git push origin :refs/tags/v1.0.0
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Create new release:**
   - Go to: https://github.com/Wootter/viam-dht22-module/releases/new
   - Choose tag: v1.0.0
   - Title: `v1.0.0 - DHT22 Sensor Module`
   - Description: (same as before)
   - Click "Publish release"

---

## ✅ Step 5: Verify Success

**After re-running:**

1. Go to: https://github.com/Wootter/viam-dht22-module/actions
2. Watch the new workflow run
3. **All steps should show green checkmarks ✅**
4. Should take 2-5 minutes total

**Success indicators:**
- ✓ Checkout code
- ✓ Set up Python
- ✓ Install Viam CLI
- ✓ Build module
- ✓ Upload module to Viam (shows version number)

---

## 🎯 Quick Diagnosis

**Based on 8-10 second failure time, most likely:**

1. **Secrets missing** (80% likely)
   - Fix: Add VIAM_API_KEY_ID and VIAM_API_KEY to GitHub

2. **Wrong API key** (15% likely)
   - Fix: Regenerate API key in Viam

3. **Workflow syntax error** (5% likely)
   - Fix: Already fixed in latest commit

---

## 📞 What to Do NOW

1. ✅ **Check the error log** (see Step 1)
   - Click on failed run
   - See what step failed
   - Read error message

2. ✅ **Verify GitHub secrets** (see Step 2)
   - Go to repository settings
   - Check secrets exist
   - Add if missing

3. ✅ **Re-run workflow** (see Step 4)
   - Click "Re-run all jobs"
   - OR delete and recreate release

4. ✅ **Watch it succeed!**
   - Should take 2-5 minutes
   - All green checkmarks

---

## 💬 Tell Me:

**After checking the error log, tell me:**
1. Which step failed? (e.g., "Install Viam CLI", "Upload module", etc.)
2. What's the exact error message?
3. Do you have both GitHub secrets set?

Then I can help you fix the specific issue!
