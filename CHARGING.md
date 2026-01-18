# Charging Configuration Guide

## Overview

The Nothing Phone (3a) supports advanced charging features including fast charging, thermal management, and LineageOS charging control. This document covers charging system configuration and troubleshooting.

## Hardware Specifications

### Battery
- **Capacity**: 5000 mAh Li-Po
- **Type**: Non-removable
- **Nominal Voltage**: 3.85V
- **Charging Voltage**: 4.4V max
- **Technology**: Dual-cell design for faster charging

### Charging Support
- **Wired Fast Charging**: 45W (expected, verify with vendor specs)
- **USB Power Delivery**: USB-C PD 3.0
- **Wireless Charging**: Not specified (verify with hardware)
- **Reverse Wireless Charging**: Not specified

## Charging Control Paths

### Primary Charging Control
```bash
# Main charging enable/disable control
/proc/charger/usb_charger_en
```

**Usage**:
```bash
# Enable charging
echo 1 > /proc/charger/usb_charger_en

# Disable charging
echo 0 > /proc/charger/usb_charger_en

# Check status
cat /proc/charger/usb_charger_en
```

### Battery Information Paths
```bash
# Battery status (Charging, Discharging, Not charging, Full)
/sys/class/power_supply/battery/status

# Battery capacity (0-100%)
/sys/class/power_supply/battery/capacity

# Battery health (Good, Overheat, Dead, etc.)
/sys/class/power_supply/battery/health

# Battery temperature (decidegrees Celsius, divide by 10)
/sys/class/power_supply/battery/temp

# Battery voltage (microvolts, divide by 1000000 for volts)
/sys/class/power_supply/battery/voltage_now

# Current flow (microamps, negative = discharging)
/sys/class/power_supply/battery/current_now

# Charging speed
/sys/class/power_supply/battery/charge_type
```

### USB/Charger Information
```bash
# USB online status (0 = disconnected, 1 = connected)
/sys/class/power_supply/usb/online

# USB type (SDP, DCP, CDP, etc.)
/sys/class/power_supply/usb/type

# USB voltage input
/sys/class/power_supply/usb/voltage_now

# USB current limit
/sys/class/power_supply/usb/current_max
```

## LineageOS Health HAL Configuration

### Charging Control Feature
Configured in `BoardConfig.mk`:
```makefile
# Lineage Health
$(call soong_config_set,lineage_health,charging_control_charging_path,/proc/charger/usb_charger_en)
```

### Health HAL Package
Defined in `device.mk`:
```makefile
PRODUCT_PACKAGES += \
    vendor.lineage.health-service.default
```

### User Access
Users can control charging via:
1. **Settings → Battery → Charging control**
2. Enable "Limit charging" 
3. Set charging limit (e.g., 80%, 90%)

**Benefits**:
- Extends battery lifespan
- Reduces battery wear from constant 100% charge
- Ideal for devices that stay plugged in

## Fast Charging Configuration

### Fast Charging Detection
```bash
# Check if fast charging is active
adb shell cat /sys/class/power_supply/battery/charge_type

# Possible values:
# - "Fast" or "Quick" = Fast charging active
# - "Normal" = Standard charging
# - "Trickle" = Low current charging
```

### Fast Charging Enablement
Fast charging should be automatically enabled when:
1. Compatible fast charger connected (45W PD charger)
2. Battery temperature in safe range (15-45°C)
3. Battery charge level below 80%
4. Device not in use/screen off (for optimal speed)

### Force Fast Charging (Debug Only)
```bash
# Some devices support forcing fast charge mode
# WARNING: Only for testing, may damage battery if used incorrectly

adb root
adb shell "echo 1 > /sys/class/power_supply/battery/input_suspend"
adb shell "echo 0 > /sys/class/power_supply/battery/input_suspend"
```

## Thermal Management During Charging

### Thermal Throttling
The device automatically reduces charging speed when:
- Battery temperature > 40°C
- Skin temperature > 42°C (front/back sensors)
- CPU/GPU under heavy load

### Thermal Zones
```bash
# Monitor thermal zones during charging
adb shell cat /sys/class/thermal/thermal_zone*/temp

# Battery thermal zone (typically thermal_zone0)
adb shell cat /sys/class/thermal/thermal_zone0/temp

# Monitor in real-time
adb shell "while true; do cat /sys/class/thermal/thermal_zone0/temp; sleep 1; done"
```

### Safe Temperature Ranges
- **Optimal**: 20-30°C
- **Acceptable**: 15-40°C
- **Warning**: 40-45°C (charging slows)
- **Critical**: > 45°C (charging stops)

## Charging Optimization

### Adaptive Charging
LineageOS may include adaptive charging features:
- **Smart charging**: Learns usage patterns
- **Scheduled full charge**: Completes charging just before daily wake time
- **Battery care**: Reduces wear by managing charge cycles

### Background Charging Optimization
```bash
# Suspend non-essential services during charging
# Configured in power HAL and thermal engine
```

## Debugging Charging Issues

### Check Charging Status
```bash
# Full battery dump
adb shell dumpsys battery

# Key fields to check:
# - AC powered: true/false
# - USB powered: true/false
# - Wireless powered: true/false (if supported)
# - status: Charging/Discharging/Not charging/Full
# - health: Good/Overheat/Dead/Over voltage/etc.
# - present: true/false
# - level: 0-100
# - voltage: mV
# - temperature: decidegrees C
# - technology: Li-ion/Li-poly
```

### Common Charging Issues

#### Issue: Not Charging When Plugged In
**Symptoms**: Charger connected, but battery not charging

**Debug**:
```bash
# Check USB online status
adb shell cat /sys/class/power_supply/usb/online
# Should be: 1

# Check charging control
adb shell cat /proc/charger/usb_charger_en
# Should be: 1

# Check battery status
adb shell cat /sys/class/power_supply/battery/status
# Should be: Charging

# Check for thermal shutdown
adb shell cat /sys/class/power_supply/battery/temp
# Should be < 450 (45.0°C)
```

**Possible Causes**:
- Charging control disabled (LineageOS battery settings)
- Temperature too high
- Faulty cable/charger
- USB-C port dirty/damaged

#### Issue: Slow Charging
**Symptoms**: Charging slower than expected

**Debug**:
```bash
# Check current input
adb shell cat /sys/class/power_supply/battery/current_now
# Fast charging: > 3000000 (3A)
# Normal charging: 1000000-2000000 (1-2A)
# Slow charging: < 1000000 (1A)

# Check charge type
adb shell cat /sys/class/power_supply/battery/charge_type
```

**Possible Causes**:
- Using non-PD charger
- Thermal throttling active
- Background apps consuming power
- Battery near full (charging slows > 80%)

#### Issue: Overheating During Charging
**Symptoms**: Device becomes very hot when charging

**Debug**:
```bash
# Monitor temperatures
adb shell cat /sys/class/thermal/thermal_zone*/temp

# Check if throttling active
adb shell cat /sys/devices/virtual/thermal/tz-by-name/battery/temp
```

**Solutions**:
- Remove phone case during fast charging
- Ensure good ventilation
- Reduce screen brightness
- Close resource-intensive apps
- Use standard charging instead of fast charging

#### Issue: Battery Draining While Charging
**Symptoms**: Battery percentage decreases even when plugged in

**Debug**:
```bash
# Check power consumption
adb shell dumpsys batterystats

# Check wake locks
adb shell dumpsys power | grep -i "wake"

# Check CPU usage
adb shell top -m 10 -d 1
```

**Possible Causes**:
- High CPU/GPU usage (gaming, video recording)
- Screen at max brightness
- Weak charger (< 18W)
- Battery degraded

### Battery Calibration

If battery percentage is inaccurate:

```bash
# Method 1: Reset battery stats (requires root)
adb root
adb shell rm /data/system/batterystats.bin
adb reboot

# Method 2: Full discharge/charge cycle
# 1. Use device until it shuts down (0%)
# 2. Charge to 100% without interruption
# 3. Keep plugged for 1 more hour after 100%
# 4. Restart device
```

## Power Supply Monitoring Script

Create a monitoring script for debugging:

```bash
#!/bin/bash
# charge_monitor.sh - Monitor charging status

while true; do
    clear
    echo "===== Battery Charging Monitor ====="
    echo ""
    echo "Status: $(adb shell cat /sys/class/power_supply/battery/status)"
    echo "Capacity: $(adb shell cat /sys/class/power_supply/battery/capacity)%"
    echo "Voltage: $(adb shell cat /sys/class/power_supply/battery/voltage_now | awk '{printf "%.2f V", $1/1000000}')"
    echo "Current: $(adb shell cat /sys/class/power_supply/battery/current_now | awk '{printf "%.2f mA", $1/1000}')"
    echo "Temp: $(adb shell cat /sys/class/power_supply/battery/temp | awk '{printf "%.1f °C", $1/10}')"
    echo "Charge Type: $(adb shell cat /sys/class/power_supply/battery/charge_type)"
    echo "Health: $(adb shell cat /sys/class/power_supply/battery/health)"
    echo ""
    echo "USB Online: $(adb shell cat /sys/class/power_supply/usb/online)"
    echo "USB Type: $(adb shell cat /sys/class/power_supply/usb/type)"
    echo ""
    echo "Charging Control: $(adb shell cat /proc/charger/usb_charger_en)"
    echo ""
    sleep 2
done
```

## Best Practices

### For Users
1. **Use official or certified chargers** - Ensures safe fast charging
2. **Avoid extreme temperatures** - Charge in 20-30°C environment
3. **Enable charging control** - Set limit to 80-90% for daily use
4. **Don't overcharge** - Unplug when reaching target charge level
5. **Calibrate occasionally** - Do full charge cycle monthly

### For Developers
1. **Test all charging scenarios** - Fast, slow, wireless, USB-C
2. **Monitor temperatures** - Ensure thermal limits enforced
3. **Validate charging control** - Test LineageOS charging limit feature
4. **Check power consumption** - Optimize for low idle drain
5. **Log charging events** - Help diagnose user issues

## SELinux Considerations

Ensure Health HAL has proper permissions:

```
# hal_health.te
allow hal_health_default sysfs_battery_supply:dir r_dir_perms;
allow hal_health_default sysfs_battery_supply:file rw_file_perms;
allow hal_health_default proc_charger:dir r_dir_perms;
allow hal_health_default proc_charger:file rw_file_perms;
```

Check for denials:
```bash
adb shell dmesg | grep -i "avc.*health"
```

## Firmware Configuration

Charging parameters may be defined in device tree:

```dts
&qcom_smbcharger {
    qcom,float-voltage-mv = <4400>;
    qcom,fastchg-current-ma = <4500>;
    qcom,thermal-mitigation = <4500 3500 2500 1500 0>;
    qcom,battery-capacity-mah = <5000>;
};
```

## References

- [Android Power Management](https://source.android.com/devices/tech/power)
- [USB Power Delivery Specification](https://www.usb.org/usb-charger-pd)
- [LineageOS Health HAL](https://github.com/LineageOS/android_hardware_lineage_health)
- [Battery University - Charging Li-ion](https://batteryuniversity.com/learn/article/charging_lithium_ion_batteries)
