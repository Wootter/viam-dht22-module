# Pre-Deployment Checklist

Use this checklist before deploying your DHT22 Viam module.

## ✅ Code Review

- [ ] All Python files have proper docstrings
- [ ] Error handling is in place
- [ ] Code follows PEP 8 style guidelines
- [ ] No hardcoded credentials or sensitive data
- [ ] GPIO pin is configurable via attributes

## ✅ Configuration

- [ ] `meta.json` updated with your GitHub username
- [ ] `pyproject.toml` updated with your GitHub username
- [ ] `CHANGELOG.md` updated with your GitHub username
- [ ] Module version number is set correctly
- [ ] Model name is correct: `viam:dht22-sensor:linux`

## ✅ Documentation

- [ ] README.md is complete and accurate
- [ ] QUICKSTART.md has correct instructions
- [ ] Wiring diagram is correct for DHT22
- [ ] Example code is tested and working
- [ ] Troubleshooting section covers common issues

## ✅ Hardware Testing

- [ ] DHT22 sensor is properly wired
- [ ] Tested on actual Raspberry Pi 4B
- [ ] `test_hardware.py` passes successfully
- [ ] Readings are accurate and consistent
- [ ] Tested with different GPIO pins
- [ ] Error handling works when sensor is disconnected

## ✅ Dependencies

- [ ] All required packages in `requirements.txt`
- [ ] System dependencies documented
- [ ] Virtual environment setup works
- [ ] `setup.sh` runs without errors
- [ ] No missing imports

## ✅ Module Functionality

- [ ] Module loads in Viam platform
- [ ] Sensor appears in Viam UI
- [ ] `get_readings()` returns correct format
- [ ] Temperature in both C and F
- [ ] Humidity percentage is accurate
- [ ] Error messages are helpful

## ✅ Build & Package

- [ ] `make module.tar.gz` creates tarball successfully
- [ ] Tarball contains all necessary files
- [ ] Tarball size is reasonable (< 10MB typically)
- [ ] No unnecessary files included

## ✅ Git & GitHub

- [ ] All files are committed
- [ ] `.gitignore` excludes sensitive files
- [ ] No large binary files committed
- [ ] Git repository is clean (`git status`)
- [ ] Remote repository is set up
- [ ] Branch is pushed to GitHub

## ✅ GitHub Actions

- [ ] `.github/workflows/deploy.yml` is present
- [ ] GitHub secrets are configured:
  - [ ] `VIAM_API_KEY_ID`
  - [ ] `VIAM_API_KEY`
- [ ] Workflow syntax is valid
- [ ] Deployment platform is correct (`linux/arm64`)

## ✅ Viam Integration

- [ ] Viam account is set up
- [ ] Robot is configured in Viam
- [ ] Viam agent is running on Raspberry Pi
- [ ] API keys have correct permissions
- [ ] Module namespace is available

## ✅ Testing Checklist

### Local Testing
- [ ] Run `python3 test_hardware.py`
- [ ] Run `python3 src/humidity_sensor.py`
- [ ] Check readings are reasonable:
  - [ ] Temperature: -40°C to 80°C
  - [ ] Humidity: 0% to 100%

### Integration Testing
- [ ] Module uploads to Viam successfully
- [ ] Module appears in robot configuration
- [ ] Sensor reads data through Viam UI
- [ ] SDK can access sensor data
- [ ] Multiple readings work consistently

### Error Testing
- [ ] Disconnect sensor - error message appears
- [ ] Invalid pin number - error is caught
- [ ] Missing configuration - helpful error message

## ✅ Documentation Review

- [ ] README has correct GitHub URLs
- [ ] All example code is tested
- [ ] Screenshots/images are up to date (if any)
- [ ] Links are not broken
- [ ] Grammar and spelling checked

## ✅ License & Legal

- [ ] LICENSE file is present (Apache 2.0)
- [ ] Copyright notices are correct
- [ ] No code copied without attribution
- [ ] All dependencies have compatible licenses

## ✅ Performance

- [ ] Sensor reads within 3 seconds
- [ ] No memory leaks during extended use
- [ ] CPU usage is reasonable
- [ ] Module starts quickly

## ✅ Security

- [ ] No hardcoded passwords or keys
- [ ] Input validation on pin number
- [ ] No SQL injection risks (not applicable)
- [ ] Dependencies are up to date

## 🚀 Deployment Steps

Once all checks pass:

1. **Final Commit**
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   ```

2. **Create Tag**
   ```bash
   git tag v1.0.0
   ```

3. **Push to GitHub**
   ```bash
   git push origin main
   git push origin v1.0.0
   ```

4. **Create GitHub Release**
   - Go to GitHub → Releases → New Release
   - Select tag v1.0.0
   - Title: "v1.0.0 - Initial Release"
   - Description: Copy from CHANGELOG.md
   - Publish release

5. **Verify Deployment**
   - Check GitHub Actions workflow
   - Verify module appears in Viam registry
   - Test module on a robot

## 📋 Post-Deployment

- [ ] GitHub release is created
- [ ] Module appears in Viam registry
- [ ] Test installation on a fresh robot
- [ ] Update documentation if needed
- [ ] Announce release (if applicable)
- [ ] Monitor for issues

## 🐛 Rollback Plan

If deployment fails:

1. Delete the GitHub release
2. Delete the Git tag: `git tag -d v1.0.0 && git push origin :refs/tags/v1.0.0`
3. Fix issues
4. Re-test everything
5. Try again with incremented version

## 📞 Support Contacts

- **Viam Discord**: https://discord.gg/viam
- **Viam Support**: https://support.viam.com
- **GitHub Issues**: https://github.com/<your-username>/viam-dht22-module/issues

---

**Remember**: Always test on actual hardware before deploying to production!
