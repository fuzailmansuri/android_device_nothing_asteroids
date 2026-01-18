# LineageOS Device Tree for Nothing Phone (3a)

## Device Information

| Device       | Nothing Phone (3a)                          |
| -----------: | :------------------------------------------ |
| SoC          | Qualcomm SM7635 (Snapdragon 7s Gen 3)      |
| CPU          | Octa-core (1x2.5 GHz Cortex-A76 & 3x2.36 GHz Cortex-A76 & 4x1.8 GHz Cortex-A55) |
| GPU          | Adreno 710                                  |
| Memory       | 8/12 GB RAM                                 |
| Shipped Android | 14.0                                     |
| Storage      | 128/256 GB UFS 3.1                          |
| Display      | 6.56" AMOLED, 1080 x 2400 pixels, 120 Hz   |
| Camera (Rear)| Dual: 50 MP (wide) + 50 MP (telephoto)     |
| Camera (Front)| 32 MP                                      |
| Battery      | Li-Po 5000 mAh, non-removable              |

## Device Codenames

- **Internal Codename**: Asteroids
- **Platform**: volcano (pineapple)
- **Model**: A059
- **Board**: volcano

## Features

### Working
- ✅ Booting
- ✅ Display & Touchscreen
- ✅ Audio & Microphone
- ✅ Wi-Fi & Bluetooth
- ✅ Cellular Network (RIL)
- ✅ GPS & Location Services
- ✅ Camera (Rear & Front)
- ✅ Fingerprint Scanner (UDFPS)
- ✅ NFC (Multi-SKU support)
- ✅ USB & Charging
- ✅ Sensors (Accelerometer, Gyroscope, Compass, Proximity, Light)
- ✅ Video Playback
- ✅ SELinux Enforcing
- ✅ A/B OTA Updates (with Virtual A/B compression)
- ✅ Glyph Interface LEDs

### Device Variants (SKU)
This device tree supports multiple regional variants:
- **Base/ROW**: Standard global variant
- **EEA**: European Economic Area
- **IND**: India
- **TUR**: Turkey
- **JPN**: Japan (with eSIM/FeliCa NFC support)
- **Pro Variants**: ProEEA, ProIND, ProROW, ProTUR

## Build Instructions

### Prerequisites
- Ubuntu 20.04 or newer (or similar Linux distribution)
- At least 300GB of free storage
- 16GB RAM minimum (32GB recommended)
- LineageOS 23.x build environment set up

### Initialize Repository
```bash
repo init -u https://github.com/LineageOS/android.git -b lineage-23.2 --git-lfs
```

### Clone Device Trees
```bash
git clone https://github.com/fuzailmansuri/android_device_nothing_asteroids device/nothing/asteroids
git clone https://github.com/Nothing-Kernel/kernel_nothing_sm7635 kernel/nothing/sm7635
git clone https://github.com/Nothing-Kernel/kernel_nothing_sm7635-modules kernel/nothing/sm7635-modules
git clone https://github.com/fuzailmansuri/android_vendor_nothing_asteroids vendor/nothing/asteroids
```

### Extract Proprietary Blobs
```bash
cd device/nothing/asteroids
./extract-files.py /path/to/stock/rom/or/adb
```

### Build
```bash
source build/envsetup.sh
lunch lineage_asteroids-ap4a-userdebug
make bacon -j$(nproc --all)
```

## Kernel Configuration

### Source
- **Repository**: kernel/nothing/sm7635
- **Base**: GKI 6.1 kernel
- **Configuration**: 
  - `gki_defconfig`
  - `vendor/pineapple_perf.config`
  - `vendor/asteroids_perf.config`

### Kernel Modules
The device uses extensive kernel module support for:
- Audio (AGM, PAL HALs)
- Camera (ISP, sensor drivers)
- Display (Qualcomm display drivers)
- Graphics (Adreno GPU)
- Networking (RMNet, IPA)
- Video (hardware codec)
- Wi-Fi (QCA6750)
- Bluetooth
- Fingerprint & Touchscreen (Nothing-specific drivers)

Modules are loaded in stages:
- **Recovery**: Critical boot modules (`modules.load.recovery`)
- **Vendor Boot**: Early userspace modules (`modules.load.vendor_boot`)
- **Vendor DLKM**: Vendor-specific drivers (`modules.load.vendor_dlkm`)
- **System DLKM**: System-level modules (`modules.load.system_dlkm`)

## Partition Layout

### Dynamic Partitions
The device uses dynamic partitioning with super partition:
- **Super Partition Size**: 9.0 GB (9663676416 bytes)
- **Dynamic Partitions**: system, system_ext, product, vendor, odm, system_dlkm, vendor_dlkm

### Static Partitions
- **boot**: 96 MB
- **vendor_boot**: 96 MB
- **init_boot**: 8 MB
- **dtbo**: 24 MB
- **recovery**: 100 MB

### Filesystem
- **Default**: ext4
- **Optional**: EROFS (Read-Only FS for improved performance)
- **F2FS Support**: Available for userdata

## Audio Configuration

The device uses Qualcomm AGM (Audio Graph Manager) and PAL (Platform Abstraction Layer) HALs.

### Audio Paths
- HAL directory: `hardware/qcom-caf/sm8650/audio/primary-hal`
- PAL directory: `hardware/qcom-caf/sm8650/audio/pal`
- Device configs: `audio/` (volcano-specific mixer paths)

**Note**: While using SM8650 audio base, device-specific configurations are in the local `audio/` directory.

## SELinux Policies

Custom SELinux policies are defined in:
- `sepolicy/vendor/` - Vendor-specific policies
- `sepolicy/public/` - Public type definitions
- `sepolicy/private/` - Private system_ext policies

Key policies for:
- Nothing-fwk framework module
- Glyph LED interface
- UDFPS fingerprint scanner
- Custom sensors and thermal management

## VINTF Manifests

Hardware interface manifests:
- `vintf/framework_manifest.xml` - Framework hardware interfaces
- `vintf/framework_matrix_nothing.xml` - Framework compatibility matrix
- `vintf/manifest_asteroids.xml` - ODM-level hardware interfaces
- `vintf/manifest_volcano.xml` - Platform-specific interfaces
- `vintf/manifest_JPN.xml` - Japan-specific hardware (eSIM, FeliCa)

## Security

### Verified Boot (AVB)
The device implements AVB 2.0 with vbmeta chaining:
- Boot, recovery, init_boot images signed separately
- System vbmeta chain: product, system, system_ext
- Vendor vbmeta chain: odm, vendor, vendor_dlkm, system_dlkm

**⚠️ IMPORTANT**: Current configuration uses test keys. For production builds:
1. Generate production signing keys
2. Replace all `external/avb/test/data/testkey_rsa2048.pem` references in `BoardConfig.mk`
3. Sign all images with production keys

### Security Patches
- **Boot Security Patch**: 2025-09-05
- **Vendor Security Patch**: 2025-09-05

## Special Features

### Glyph Interface
The device includes Nothing's Glyph LED interface:
- **Packages**: ParanoidGlyph, GlyphAdapter
- **Control**: LED zones controlled via HAL
- **Overlays**: Custom overlays in RRO packages

### Charging Control
LineageOS Health HAL with charging control:
- **Path**: `/proc/charger/usb_charger_en`
- Allows limiting charge to extend battery life

### LiveDisplay
Qualcomm SDM LiveDisplay support:
- Color mode switching
- Adaptive brightness
- DisplayManager integration disabled (dm:false)

## Overlays (RRO)

Extensive Runtime Resource Overlay support for customization:
- Framework overlays (AsteroidsFrameworksOverlay)
- SystemUI overlays (AsteroidsSystemUIOverlay)
- Settings overlays (AsteroidsSettingsOverlay, AsteroidsSettingsProviderOverlay)
- WiFi overlays (per-variant: Base, Pro)
- Carrier, Telephony, Secure Element configs
- Camera overlays (AsteroidsApertureOverlay)

See `rro_overlays/` directory for all overlay packages.

## Testing & Validation

### Pre-submission Checklist
- [ ] Boot test (device boots to UI)
- [ ] Audio playback & recording
- [ ] Camera photo & video capture
- [ ] Wi-Fi connection
- [ ] Bluetooth pairing
- [ ] Cellular data & calls
- [ ] GPS location fix
- [ ] Fingerprint unlock
- [ ] NFC tap (if applicable to SKU)
- [ ] Glyph LEDs functional
- [ ] Charging & battery reporting
- [ ] A/B OTA update
- [ ] SELinux enforcing (no critical denials)

### Module Loading Validation
```bash
# Check loaded modules
adb shell lsmod

# Verify no module loading failures
adb logcat -d | grep -i "module"

# Check for SELinux denials
adb shell dmesg | grep -i "avc"
```

### Performance Validation
```bash
# CPU frequencies
adb shell cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq

# GPU frequency
adb shell cat /sys/class/kgsl/kgsl-3d0/devfreq/cur_freq

# Memory info
adb shell cat /proc/meminfo
```

## Known Issues

1. **Audio HAL Base**: Using SM8650 audio HAL as base. Verify volcano-specific mixer paths are correctly applied.
2. **AVB Keys**: Currently using test keys; must be replaced for production builds.

## Additional Documentation

This device tree includes comprehensive documentation for various aspects:

- **[KERNEL_MODULES.md](KERNEL_MODULES.md)** - Detailed kernel module loading documentation
  - Module loading stages (recovery, vendor_boot, vendor_dlkm, system_dlkm)
  - Module categories (audio, camera, display, network, sensors)
  - Debugging module loading issues
  
- **[DEVICE_TREE.md](DEVICE_TREE.md)** - Device tree and DTBO overlay documentation
  - DTB/DTBO structure and configuration
  - Hardware variant overlay selection
  - Device tree debugging techniques
  
- **[SELINUX.md](SELINUX.md)** - SELinux policy documentation
  - Custom policies for Nothing-specific features (Glyph, UDFPS)
  - HAL service policies
  - Debugging SELinux denials
  
- **[TESTING.md](TESTING.md)** - Comprehensive testing guide
  - Core functionality tests (display, audio, camera, sensors)
  - Performance testing
  - Battery and charging tests
  - Test checklists and automation
  
- **[CHARGING.md](CHARGING.md)** - Charging configuration and troubleshooting
  - Fast charging configuration
  - Thermal management
  - LineageOS charging control
  - Debugging charging issues
  
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
  - How to contribute
  - Coding standards
  - Testing requirements
  - PR submission process

## Contributing

Contributions are welcome! Please:
1. Test thoroughly on actual hardware
2. Follow LineageOS code style guidelines
3. Document changes in commit messages
4. Ensure SELinux policies are correctly defined
5. Validate no ABI breakages with module updates

## References

- [LineageOS Wiki](https://wiki.lineageos.org/)
- [Qualcomm SM7635 Platform](https://www.qualcomm.com/products/mobile/snapdragon/smartphones/snapdragon-7-series-mobile-platforms)
- [Nothing Phone (3a) Specifications](https://nothing.tech/)

## Copyright & License

```
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
```

This device tree is licensed under the Apache License, Version 2.0.
