# Testing Guide

## Overview

This document provides comprehensive testing procedures for validating the Nothing Phone (3a) LineageOS build. Follow these tests before releasing builds to ensure device functionality and stability.

## Pre-Testing Setup

### Requirements
- Nothing Phone (3a) device with unlocked bootloader
- USB cable for ADB/Fastboot
- SIM card (for cellular testing)
- SD card reader (if testing external storage)
- Known good Wi-Fi network
- Bluetooth device for pairing
- NFC-enabled card/device (for NFC testing)

### Initial Setup
```bash
# Enable ADB
adb root
adb remount

# Check SELinux status (should be Enforcing)
adb shell getenforce

# Check device info
adb shell getprop ro.build.fingerprint
adb shell getprop ro.product.device
adb shell getprop ro.lineage.version
```

## Core Functionality Tests

### 1. Boot & System

#### Boot Time Test
```bash
# Measure boot time
adb shell dmesg | grep "init: Starting service"
adb logcat -d | grep "boot_progress"
```

**Expected**: 
- ✅ Boot completes in under 60 seconds
- ✅ No kernel panics or crashes
- ✅ All essential services start

**Test Steps**:
1. Power on device from off state
2. Observe boot animation
3. Verify home screen loads successfully
4. Check no boot loops occur

#### SELinux Enforcement
```bash
# Verify enforcing mode
adb shell getenforce

# Check for denials
adb shell dmesg | grep "avc.*denied"
```

**Expected**: 
- ✅ Output: "Enforcing"
- ⚠️ No critical SELinux denials

### 2. Display & Touch

#### Display Test
**Test Steps**:
1. Check display brightness adjustment
2. Verify auto-brightness works
3. Test 120Hz refresh rate toggle (Settings → Display → Refresh rate)
4. Check always-on display (AOD)
5. Verify screen timeout works
6. Test rotation in all orientations

**Expected**:
- ✅ Brightness smoothly adjustable
- ✅ Display renders correctly at 120Hz
- ✅ AOD displays with low power consumption
- ✅ Touch responsive across entire screen

#### Touch Test
**Test Steps**:
1. Open Settings → Display → Touchscreen test (if available)
2. Draw patterns across screen
3. Test multi-touch (pinch zoom in Gallery/Browser)
4. Test edge gestures
5. Test tap, long press, swipe

**Expected**:
- ✅ All touch zones responsive
- ✅ Multi-touch works (10-point minimum)
- ✅ No phantom touches
- ✅ Gestures register accurately

### 3. Audio

#### Speaker Test
```bash
# Test speakers
adb shell tinymix
adb shell tinycap /sdcard/test.wav -r 48000 -c 2
adb shell tinyplay /sdcard/test.wav
```

**Test Steps**:
1. Play music through bottom speaker
2. Play music through earpiece speaker
3. Test volume levels (0-100%)
4. Test different audio sources (YouTube, Spotify, local files)
5. Test audio with headphones (USB-C or Bluetooth)

**Expected**:
- ✅ Clear audio output from all speakers
- ✅ No distortion at high volume
- ✅ Stereo sound works
- ✅ Volume controls responsive

#### Microphone Test
**Test Steps**:
1. Record voice memo
2. Play back recording
3. Test video recording with audio
4. Make phone call and test mic
5. Test noise cancellation in call

**Expected**:
- ✅ Clear voice capture
- ✅ No background static
- ✅ All microphones functional (primary, secondary)

### 4. Camera

#### Rear Camera Test
**Test Steps**:
1. Open Camera app
2. Capture photo (50MP main sensor)
3. Capture photo (50MP telephoto)
4. Test video recording (4K @ 30fps)
5. Test zoom (1x, 2x, 5x, 10x)
6. Test flash (auto, on, off)
7. Test HDR mode
8. Test night mode

**Expected**:
- ✅ Photos save successfully
- ✅ No lag in viewfinder
- ✅ Videos record smoothly
- ✅ Flash works correctly
- ✅ All camera modes functional

#### Front Camera Test
**Test Steps**:
1. Switch to front camera
2. Capture selfie (32MP)
3. Record video
4. Test portrait mode
5. Test screen flash

**Expected**:
- ✅ Front camera captures clearly
- ✅ Video calls work
- ✅ Portrait mode functions

### 5. Fingerprint Scanner (UDFPS)

#### Fingerprint Test
```bash
# Check fingerprint HAL
adb shell ps -A | grep fingerprint
adb shell dumpsys fingerprint
```

**Test Steps**:
1. Settings → Security → Fingerprint
2. Enroll new fingerprint
3. Lock device
4. Unlock with fingerprint (10 attempts)
5. Test fingerprint in different apps (banking, password manager)

**Expected**:
- ✅ Enrollment completes successfully
- ✅ 9/10 or better unlock success rate
- ✅ Fast unlock (< 500ms)
- ✅ UDFPS icon displays correctly on AOD

### 6. Wi-Fi

#### Wi-Fi Test
```bash
# Check Wi-Fi status
adb shell dumpsys wifi
adb shell iw dev wlan0 link
```

**Test Steps**:
1. Enable Wi-Fi
2. Scan for networks
3. Connect to 2.4GHz network
4. Connect to 5GHz network
5. Test Wi-Fi 6 (if supported by AP)
6. Test Wi-Fi hotspot
7. Test Wi-Fi Direct
8. Test Wi-Fi Aware (if applicable)

**Expected**:
- ✅ Networks detected quickly
- ✅ Stable connection
- ✅ Good signal strength
- ✅ Speed test shows expected throughput
- ✅ Hotspot works for other devices

### 7. Bluetooth

#### Bluetooth Test
```bash
# Check Bluetooth status
adb shell dumpsys bluetooth_manager
```

**Test Steps**:
1. Enable Bluetooth
2. Pair with headphones
3. Play music via Bluetooth
4. Test Bluetooth call
5. Pair with smartwatch
6. Test file transfer
7. Test multiple device connections

**Expected**:
- ✅ Devices pair successfully
- ✅ Audio quality good
- ✅ No disconnections
- ✅ Multiple devices connect simultaneously

### 8. Cellular Network (RIL)

#### Network Test
```bash
# Check RIL status
adb shell dumpsys telephony.registry
adb shell getprop | grep "gsm"
```

**Test Steps**:
1. Insert SIM card
2. Verify network registration
3. Make outgoing call
4. Receive incoming call
5. Send SMS
6. Receive SMS
7. Test mobile data (4G/5G)
8. Test VoLTE
9. Test VoWiFi (Wi-Fi Calling)
10. Test dual SIM (if applicable)

**Expected**:
- ✅ Network registers automatically
- ✅ Calls connect successfully
- ✅ SMS sends/receives
- ✅ Mobile data works
- ✅ VoLTE/VoWiFi functional

### 9. GPS & Location

#### GPS Test
```bash
# Check GPS status
adb shell dumpsys location
```

**Test Steps**:
1. Enable location services
2. Open Maps app
3. Wait for GPS fix
4. Navigate to destination
5. Test indoor location (if Wi-Fi scanning enabled)
6. Test high-accuracy mode

**Expected**:
- ✅ GPS fix in < 30 seconds (cold start)
- ✅ Accuracy within 10 meters
- ✅ Navigation works smoothly
- ✅ Location updates regularly

### 10. NFC

#### NFC Test
```bash
# Check NFC HAL
adb shell ps -A | grep nfc
adb shell dumpsys nfc
```

**Test Steps**:
1. Enable NFC
2. Tap NFC tag
3. Test Android Beam (if available)
4. Test contactless payment (if set up)
5. For JPN SKU: Test FeliCa

**Expected**:
- ✅ NFC tags read successfully
- ✅ Payment terminals detect device
- ✅ Fast tap response

### 11. Sensors

#### Sensor Test
```bash
# List sensors
adb shell dumpsys sensorservice

# Monitor sensor data
adb shell dumpsys sensorservice | grep -A 20 "Active sensors"
```

**Test Steps**:
1. Test accelerometer (tilt device)
2. Test gyroscope (rotate device)
3. Test magnetometer (compass)
4. Test proximity sensor (during call)
5. Test light sensor (auto-brightness)
6. Test step counter (walk with device)

**Expected**:
- ✅ All sensors report data
- ✅ Sensor values update in real-time
- ✅ Sensor accuracy acceptable

### 12. Charging & Battery

#### Charging Test
```bash
# Check charging status
adb shell dumpsys battery
adb shell cat /sys/class/power_supply/battery/status
adb shell cat /sys/class/power_supply/battery/capacity
```

**Test Steps**:
1. Plug in USB-C charger
2. Verify charging starts
3. Check charging speed
4. Test fast charging (if supported)
5. Test wireless charging (if supported)
6. Test charging control (Settings → Battery → Charging control)
7. Monitor battery temperature

**Expected**:
- ✅ Charging detected immediately
- ✅ Fast charging works
- ✅ Battery temperature stays safe (< 45°C)
- ✅ Charging control limits work

#### Battery Drain Test
```bash
# Monitor battery stats
adb shell dumpsys batterystats
adb shell dumpsys batterystats --reset (to reset stats)
```

**Test Steps**:
1. Fully charge battery
2. Use device normally for 4 hours
3. Check battery usage
4. Standby test: Leave device idle overnight

**Expected**:
- ✅ Reasonable battery consumption
- ✅ Standby drain < 2% per hour
- ✅ Screen-on time meets expectations (6+ hours)

### 13. Storage

#### Internal Storage Test
```bash
# Check storage
adb shell df -h
adb shell ls -la /data/media/0/
```

**Test Steps**:
1. Copy large file to internal storage
2. Verify file integrity
3. Delete file
4. Check available space

**Expected**:
- ✅ Read/write speeds acceptable
- ✅ No storage corruption
- ✅ Files accessible in file manager

### 14. USB

#### USB Test
**Test Steps**:
1. Connect to PC
2. Test MTP (file transfer)
3. Test PTP (photo transfer)
4. Test USB tethering
5. Test USB debugging (ADB)
6. Test USB OTG (flash drive)

**Expected**:
- ✅ All USB modes work
- ✅ File transfers successful
- ✅ USB OTG devices recognized

### 15. Glyph Interface

#### Glyph LED Test
```bash
# Check Glyph service
adb shell ps -A | grep glyph
```

**Test Steps**:
1. Settings → Glyph Interface
2. Test all LED zones
3. Test notification patterns
4. Test ringtone patterns
5. Test charging patterns
6. Adjust brightness levels

**Expected**:
- ✅ All LED zones light up
- ✅ Patterns play correctly
- ✅ Brightness adjustable
- ✅ No LED zones stuck on

## Performance Tests

### CPU Performance
```bash
# Check CPU frequencies
adb shell cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq

# Run benchmark
# Use Geekbench, AnTuTu, or 3DMark
```

### GPU Performance
```bash
# Check GPU frequency
adb shell cat /sys/class/kgsl/kgsl-3d0/devfreq/cur_freq

# Run graphics benchmark
# Use 3DMark, GFXBench
```

### Memory Performance
```bash
# Check memory info
adb shell cat /proc/meminfo
adb shell dumpsys meminfo
```

**Expected**:
- ✅ Performance scores comparable to other SD 7s Gen 3 devices
- ✅ No thermal throttling under normal use
- ✅ Smooth UI (60/120fps)

## Advanced Tests

### Kernel Module Loading
```bash
# List loaded modules
adb shell lsmod

# Check for module errors
adb shell dmesg | grep -i "module"
```

**Expected**:
- ✅ All required modules loaded
- ✅ No module loading failures

### A/B OTA Update
**Test Steps**:
1. Build second ROM version
2. Flash as OTA update
3. Reboot to new slot
4. Verify update successful
5. Test rollback if needed

**Expected**:
- ✅ Update installs successfully
- ✅ Device boots to new version
- ✅ No data loss
- ✅ Rollback works if needed

## Automated Testing

### CTS (Compatibility Test Suite)
```bash
# Run CTS tests (requires CTS package)
./cts-tradefed run cts --plan CTS
```

### VTS (Vendor Test Suite)
```bash
# Run VTS tests
./vts-tradefed run vts
```

## Reporting Issues

When reporting test failures, include:
1. Device variant (Base/Pro, region)
2. Build number/date
3. Exact steps to reproduce
4. Expected vs actual behavior
5. Relevant logs (logcat, dmesg)
6. Screenshots/screen recordings

### Log Collection
```bash
# Full logcat
adb logcat -d > logcat.txt

# Kernel log
adb shell dmesg > dmesg.txt

# Bug report
adb bugreport bugreport.zip
```

## Test Checklist Summary

### Critical (Must Pass)
- [ ] Device boots successfully
- [ ] SELinux enforcing
- [ ] Display & touch functional
- [ ] Audio playback/recording works
- [ ] Cameras capture photos/videos
- [ ] Fingerprint unlock works
- [ ] Wi-Fi connects
- [ ] Cellular calls work
- [ ] Mobile data functional
- [ ] Battery charging works

### Important (Should Pass)
- [ ] Bluetooth pairs and works
- [ ] GPS gets location fix
- [ ] NFC reads tags
- [ ] All sensors report data
- [ ] USB modes work
- [ ] Glyph LEDs functional
- [ ] Performance acceptable
- [ ] Battery life reasonable

### Optional (Nice to Have)
- [ ] VoLTE/VoWiFi work
- [ ] Hotspot functional
- [ ] OTA updates work
- [ ] Charging control works
- [ ] LiveDisplay functional

## Continuous Testing

### Regression Testing
- Test before every release
- Test after kernel updates
- Test after major system changes

### User Feedback
- Monitor user reports
- Track common issues
- Prioritize fixes

## Resources

- [Android CTS](https://source.android.com/compatibility/cts)
- [Android VTS](https://source.android.com/compatibility/vts)
- [LineageOS Testing Guide](https://wiki.lineageos.org/test_framework.html)
