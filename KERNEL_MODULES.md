# Kernel Module Loading Documentation

## Overview

The Nothing Phone (3a) uses a GKI (Generic Kernel Image) with loadable kernel modules for hardware-specific drivers. Modules are loaded in stages during boot for optimal performance and recovery support.

## Module Loading Stages

### 1. Recovery Modules (`modules.load.recovery`)
Loaded during recovery mode and early boot for critical hardware access.

**Purpose**: Minimal set of modules required for:
- Storage access (UFS)
- Display output
- Touchscreen input
- USB connectivity
- Basic power management

**When loaded**: First stage bootloader and recovery environment.

### 2. Vendor Boot Modules (`modules.load.vendor_boot`)
Loaded in early userspace (init_boot/vendor_boot ramdisk).

**Purpose**: Early hardware initialization modules needed before mounting filesystems:
- Block device drivers
- Filesystem support
- Essential platform drivers

**When loaded**: During vendor_boot ramdisk execution, before partition mounting.

### 3. Vendor DLKM Modules (`modules.load.vendor_dlkm`)
Vendor-specific dynamically loadable kernel modules.

**Purpose**: Main hardware driver modules:
- Audio (AGM, PAL, codec drivers)
- Camera (ISP, sensor drivers, flash control)
- Display (Qualcomm DRM, panel drivers)
- Graphics (Adreno GPU)
- Video (hardware encoder/decoder)
- Network (RMNet, IPA for cellular data)
- Wi-Fi (QCA6750 WLAN driver)
- Bluetooth (Qualcomm BT driver)
- NFC (ST54J, ST21 controllers)
- Fingerprint (Goodix/Egis/Focal UDFPS drivers)
- Touchscreen (Goodix/Novatek/Focal drivers)
- Sensors (accelerometer, gyroscope, magnetometer)
- Thermal management
- Power supply and charging

**When loaded**: After vendor partition is mounted, during Android init.

### 4. System DLKM Modules (`modules.load.system_dlkm`)
System-level kernel modules (typically minimal for GKI compliance).

**Purpose**: Generic system modules that don't belong to vendor partition.

**When loaded**: After system partition is mounted.

## Module Categories

### Audio Modules
- **agm.ko** - Audio Graph Manager
- **pal.ko** - Platform Abstraction Layer
- **q6_dlkm.ko** - Qualcomm DSP interface
- **adsp_loader_dlkm.ko** - ADSP firmware loader
- **bolero_cdc_dlkm.ko** - Bolero codec
- **wcd_core_dlkm.ko** - WCD codec core
- **snd_event_dlkm.ko** - Sound event notification

### Camera Modules
- **camera.ko** - Camera HAL interface
- **cam_icp.ko** - Image Control Processor
- **cam_isp.ko** - Image Signal Processor
- **cam_jpeg.ko** - JPEG encoder/decoder
- **cam_sensor_module.ko** - Camera sensor drivers

### Display & Graphics Modules
- **msm_drm.ko** - Qualcomm Display DRM driver
- **adreno.ko** - Adreno GPU driver
- **msm_kgsl.ko** - Kernel Graphics Support Layer

### Network Modules
- **rmnet_core.ko** - RMNet core (cellular data)
- **rmnet_ctl.ko** - RMNet control
- **rmnet_offload.ko** - RMNet offload engine
- **rmnet_shs.ko** - Smart Hash Scheduler
- **rmnet_perf.ko** - Performance optimizations
- **ipa_dlkm.ko** - Internet Packet Accelerator

### Wi-Fi & Bluetooth
- **wlan.ko** - QCA6750 WLAN driver (qcacld-3.0)
- **btpower.ko** - Bluetooth power management
- **bt_fm_slim.ko** - Bluetooth FM SLIM driver

### Sensor Modules
- **sensors.ko** - Generic sensor framework
- **sensors_class.ko** - Sensor class driver
- **dynamic_sensor_hal.ko** - Dynamic sensor HAL

### Custom Nothing Modules
- **goodix_fod.ko** - Goodix fingerprint on display
- **touchscreen.ko** - Custom touchscreen drivers (Goodix/Novatek/Focal)

## Module Blocklist

Modules listed in `modules.blocklist` are prevented from auto-loading:
- Conflicting drivers
- Deprecated modules
- Test/debug modules not for production

Blocked modules in `system_dlkm.modules.blocklist` prevent system modules from loading.

## Debugging Module Loading

### Check loaded modules
```bash
adb shell lsmod
```

### Check module load failures
```bash
adb shell dmesg | grep -i "module"
adb logcat -d | grep -i "insmod"
```

### Manually load a module
```bash
adb root
adb shell insmod /vendor/lib/modules/<module_name>.ko
```

### Check module dependencies
```bash
adb shell modinfo <module_name>
```

### View module load order
```bash
adb shell cat /proc/modules
```

## Common Issues

### Module Not Found
**Symptom**: "module not found" or "No such file" errors.

**Causes**:
- Module not compiled with kernel
- Module path incorrect in `.load` file
- Missing module dependencies

**Solution**: Verify module exists in kernel output and path matches.

### Module Version Mismatch
**Symptom**: "version magic mismatch" errors.

**Causes**:
- Kernel and modules compiled from different sources
- Kernel version changed but modules not rebuilt

**Solution**: Clean rebuild of both kernel and modules.

### Missing Symbols
**Symptom**: "Unknown symbol" errors when loading module.

**Causes**:
- Dependency module not loaded
- Symbol not exported by kernel

**Solution**: Load dependency modules first, or enable symbol export in kernel config.

### Hardware Not Working
**Symptom**: Hardware feature (camera, audio, etc.) not functional.

**Causes**:
- Required module not loaded
- Module loaded but firmware missing
- SELinux denials preventing module access

**Solution**: 
1. Check module is loaded: `lsmod | grep <module>`
2. Check firmware exists: `ls /vendor/firmware`
3. Check SELinux denials: `dmesg | grep avc`

## Best Practices

1. **Minimal Recovery**: Keep recovery modules minimal for fastest recovery boot
2. **Dependency Order**: Load modules in dependency order (base modules before dependent ones)
3. **Blocklist Management**: Block conflicting/deprecated modules to avoid issues
4. **Testing**: Test each loading stage individually during development
5. **Documentation**: Update this file when adding/removing modules

## Module Signing

For production builds with enforced module signature verification:
1. Generate module signing keys
2. Sign all modules during build
3. Configure kernel to verify signatures
4. Include public key in kernel for verification

Current configuration uses unsigned modules for development.

## References

- [Linux Kernel Module Documentation](https://www.kernel.org/doc/html/latest/kbuild/modules.html)
- [Android GKI Documentation](https://source.android.com/devices/architecture/kernel/generic-kernel-image)
- [Qualcomm DLKM Documentation](https://docs.qualcomm.com/)
