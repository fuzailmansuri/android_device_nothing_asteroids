# SELinux Policy Documentation

## Overview

The Nothing Phone (3a) device tree includes custom SELinux (Security-Enhanced Linux) policies to properly secure custom hardware interfaces, vendor services, and Nothing-specific features while maintaining LineageOS security standards.

## SELinux Mode

- **Target Mode**: Enforcing
- **Policy Type**: Android S+ (API 31+)
- **Base Policy**: Qualcomm vendor policy + LineageOS extensions

## Policy Structure

### Policy Directories

```
sepolicy/
├── vendor/          # Vendor-specific policies (HAL, drivers, services)
├── public/          # Public type definitions (system_ext)
└── private/         # Private system_ext policies
```

### Base Policy Inclusion

```makefile
# From BoardConfig.mk
include device/qcom/sepolicy_vndr/SEPolicy.mk

BOARD_VENDOR_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/vendor
SYSTEM_EXT_PUBLIC_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/public
SYSTEM_EXT_PRIVATE_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/private
```

## Custom Policies

### 1. Nothing Framework (nothing-fwk)

**Purpose**: Framework JAR providing Nothing-specific APIs.

**Policy Files**: 
- `sepolicy/vendor/nothing_fwk.te`
- `sepolicy/public/nothing_fwk.te`

**Key Permissions**:
```
# Allow system server to access Nothing framework APIs
allow system_server nothing_fwk_service:service_manager find;

# Allow apps to use Nothing framework
binder_call(platform_app, nothing_fwk)
allow platform_app nothing_fwk_service:service_manager find;
```

### 2. Glyph Interface

**Purpose**: LED control for Nothing's Glyph Interface.

**Policy Files**: 
- `sepolicy/vendor/hal_glyph.te`
- `sepolicy/vendor/file_contexts` (Glyph LED sysfs paths)

**Key Permissions**:
```
# Glyph HAL access to LED control
allow hal_glyph sysfs_leds:dir r_dir_perms;
allow hal_glyph sysfs_leds:file rw_file_perms;
allow hal_glyph sysfs_leds:lnk_file read;

# Glyph service registration
add_service(hal_glyph, hal_glyph_service)
```

**File Contexts**:
```
/sys/devices/platform/soc/[0-9a-f]+\.i2c/i2c-[0-9]+/[0-9]+-[0-9a-f]+/leds(/.*)? u:object_r:sysfs_leds:s0
/vendor/bin/hw/vendor\.nothing\.glyph@1\.0-service u:object_r:hal_glyph_exec:s0
```

### 3. UDFPS (Under-Display Fingerprint Scanner)

**Purpose**: Fingerprint sensor HAL and daemon policies.

**Policy Files**: 
- `sepolicy/vendor/hal_fingerprint_asteroids.te`
- `sepolicy/vendor/vendor_fingerprint.te`

**Key Permissions**:
```
# Fingerprint HAL
allow hal_fingerprint_default fingerprint_device:chr_file rw_file_perms;
allow hal_fingerprint_default uhid_device:chr_file rw_file_perms;
allow hal_fingerprint_default tee_device:chr_file rw_file_perms;

# UDFPS touch input
allow hal_fingerprint_default input_device:dir r_dir_perms;
allow hal_fingerprint_default input_device:chr_file rw_file_perms;

# UDFPS display control
allow hal_fingerprint_default sysfs_graphics:dir search;
allow hal_fingerprint_default sysfs_graphics:file rw_file_perms;
```

### 4. Custom Sensors

**Purpose**: Nothing-specific sensor implementations.

**Policy Files**: 
- `sepolicy/vendor/hal_sensors_asteroids.te`

**Key Permissions**:
```
# Sensor HAL multihal
allow hal_sensors_default vendor_configs_file:dir r_dir_perms;
allow hal_sensors_default vendor_configs_file:file r_file_perms;

# Sensor calibration data
allow hal_sensors_default mnt_vendor_file:dir r_dir_perms;
allow hal_sensors_default persist_sensors_file:dir rw_dir_perms;
allow hal_sensors_default persist_sensors_file:file create_file_perms;
```

### 5. Thermal Management

**Purpose**: Thermal HAL and thermal daemon policies.

**Policy Files**: 
- `sepolicy/vendor/thermal-engine.te`
- `sepolicy/vendor/vendor_thermal.te`

**Key Permissions**:
```
# Thermal daemon
allow thermal-engine thermal_device:file rw_file_perms;
allow thermal-engine sysfs_thermal:dir r_dir_perms;
allow thermal-engine sysfs_thermal:file rw_file_perms;
allow thermal-engine sysfs_thermal:lnk_file read;

# Charging thermal control
allow thermal-engine sysfs_battery_supply:dir r_dir_perms;
allow thermal-engine sysfs_battery_supply:file rw_file_perms;
```

### 6. Audio HAL

**Purpose**: AGM/PAL audio HAL policies.

**Policy Files**: 
- `sepolicy/vendor/hal_audio.te`

**Key Permissions**:
```
# Audio HAL
allow hal_audio_default audio_device:dir r_dir_perms;
allow hal_audio_default audio_device:chr_file rw_file_perms;

# ADSP access
allow hal_audio_default adsprpc_device:chr_file r_file_perms;

# Audio config files
allow hal_audio_default vendor_audio_data_file:dir rw_dir_perms;
allow hal_audio_default vendor_audio_data_file:file create_file_perms;
```

### 7. Camera HAL

**Purpose**: Camera HAL and camera server policies.

**Policy Files**: 
- `sepolicy/vendor/hal_camera.te`

**Key Permissions**:
```
# Camera HAL
allow hal_camera_default camera_device:chr_file rw_file_perms;
allow hal_camera_default video_device:chr_file rw_file_perms;
allow hal_camera_default video_device:dir r_dir_perms;

# Camera config and calibration
allow hal_camera_default mnt_vendor_file:dir r_dir_perms;
allow hal_camera_default vendor_camera_data_file:dir rw_dir_perms;
allow hal_camera_default vendor_camera_data_file:file create_file_perms;
```

### 8. NFC Multi-SKU

**Purpose**: NFC HAL for different chip variants (ST21, ST54J).

**Policy Files**: 
- `sepolicy/vendor/hal_nfc.te`
- `sepolicy/vendor/vendor_nfc.te`

**Key Permissions**:
```
# NFC HAL
allow hal_nfc_default nfc_device:chr_file rw_file_perms;
allow hal_nfc_default vendor_nfc_vendor_data_file:dir rw_dir_perms;
allow hal_nfc_default vendor_nfc_vendor_data_file:file create_file_perms;

# I2C access for NFC
allow hal_nfc_default self:capability { dac_override dac_read_search };

# eSE (embedded Secure Element) for Japan SKU
allow hal_nfc_default ese_device:chr_file rw_file_perms;
```

### 9. Vibrator HAL

**Purpose**: Custom vibrator HAL with haptic effects.

**Policy Files**: 
- `sepolicy/vendor/hal_vibrator_asteroids.te`

**Key Permissions**:
```
# Vibrator HAL
allow hal_vibrator_default sysfs_vibrator:dir r_dir_perms;
allow hal_vibrator_default sysfs_vibrator:file rw_file_perms;

# Haptic effects
allow hal_vibrator_default vendor_vibrator_data_file:dir r_dir_perms;
allow hal_vibrator_default vendor_vibrator_data_file:file r_file_perms;
```

### 10. Charging Control

**Purpose**: LineageOS Health HAL charging control.

**Policy Files**: 
- `sepolicy/vendor/hal_health.te`

**Key Permissions**:
```
# Health HAL
allow hal_health_default sysfs_battery_supply:dir r_dir_perms;
allow hal_health_default sysfs_battery_supply:file rw_file_perms;
allow hal_health_default sysfs_usb_supply:dir r_dir_perms;
allow hal_health_default sysfs_usb_supply:file rw_file_perms;

# Charging control path
allow hal_health_default proc_charger:dir r_dir_perms;
allow hal_health_default proc_charger:file rw_file_perms;
```

## File Contexts

### Vendor Binaries
```
# file_contexts
/vendor/bin/hw/android\.hardware\.sensors@[0-9].[0-9]-service-multihal\.asteroids u:object_r:hal_sensors_default_exec:s0
/vendor/bin/hw/android\.hardware\.vibrator-service\.asteroids u:object_r:hal_vibrator_default_exec:s0
```

### Device Nodes
```
# file_contexts
/dev/goodix_fp u:object_r:fingerprint_device:s0
/dev/spidev[0-9]+\.[0-9]+ u:object_r:spidev_device:s0
```

### Sysfs Paths
```
# file_contexts
/sys/devices/platform/soc/[0-9a-f]+\.qcom,glink_pkt/glink_pkt_charger(/.*)? u:object_r:sysfs_battery_supply:s0
/sys/devices(/platform)?/soc/[0-9a-f]+\.i2c/i2c-[0-9]+/[0-9]+-[0-9a-f]+/leds(/.*)? u:object_r:sysfs_leds:s0
```

## Debugging SELinux

### Check SELinux Status
```bash
adb shell getenforce
# Output should be: Enforcing
```

### View SELinux Denials
```bash
# Recent denials
adb shell dmesg | grep -i "avc.*denied"

# Audit log
adb shell cat /sys/fs/selinux/avc/cache_stats
```

### Generate Policy from Denials
```bash
# Pull denials from device
adb pull /sys/fs/pstore/console-ramoops-0 ./console.txt

# Generate policy rules (requires audit2allow)
cat console.txt | grep "avc.*denied" | audit2allow -p sepolicy

# Or use sesearch to analyze existing policy
sesearch -A -s hal_fingerprint_default -t fingerprint_device sepolicy
```

### Test Policy Changes
```bash
# Set to permissive (for testing only!)
adb root
adb shell setenforce 0

# Test your changes...

# Re-enable enforcing
adb shell setenforce 1
```

## Common Denial Patterns

### HAL Service Access
```
avc: denied { find } for service=vendor.nothing.glyph@1.0::IGlyph/default
Solution: allow <domain> <service>_service:service_manager find;
```

### Sysfs File Access
```
avc: denied { write } for name="brightness" path="/sys/class/leds/.../brightness"
Solution: allow <domain> sysfs_leds:file rw_file_perms;
```

### Device Node Access
```
avc: denied { read write } for path="/dev/goodix_fp"
Solution: allow <domain> fingerprint_device:chr_file rw_file_perms;
```

## Best Practices

1. **Minimal Permissions**: Grant only necessary permissions
2. **Type Enforcement**: Create specific types for custom devices/files
3. **Domain Separation**: Keep HALs in separate domains
4. **No Permissive**: Never ship with permissive domains in production
5. **Audit Denials**: Review all denials during development
6. **Neverallow Compliance**: Ensure policies don't violate neverallow rules
7. **Documentation**: Comment complex policy rules

## Testing Checklist

- [ ] SELinux enforcing on boot
- [ ] No critical denials in dmesg
- [ ] All HAL services start successfully
- [ ] Nothing-specific features work (Glyph, UDFPS)
- [ ] No permissive domains
- [ ] CTS/VTS SELinux tests pass
- [ ] No neverallow violations

## Resources

- [SELinux for Android](https://source.android.com/security/selinux)
- [Writing SELinux Policy](https://source.android.com/security/selinux/device-policy)
- [SELinux Policy Language](https://selinuxproject.org/page/PolicyLanguage)
- [audit2allow Tool](https://linux.die.net/man/1/audit2allow)
