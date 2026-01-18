# Device Tree & DTBO Documentation

## Overview

The Nothing Phone (3a) uses Device Tree Blobs (DTB) and Device Tree Blob Overlays (DTBO) to describe hardware configuration to the kernel. This approach allows a single kernel to support multiple device variants through runtime overlay selection.

## Device Tree Structure

### Platform
- **Board Platform**: volcano (Snapdragon 7s Gen 3)
- **SoC**: SM7635 (Snapdragon 7s Gen 3)
- **Board Name**: volcano
- **Device Variants**: Multiple SKUs (Base, Pro, Regional variants)

## DTB Configuration

### Main DTB (Device Tree Blob)
- **Location**: Included in boot.img
- **Configuration**: `BOARD_INCLUDE_DTB_IN_BOOTIMG := true`
- **Purpose**: Base hardware description for platform initialization

The DTB contains:
- CPU topology (Cortex-A76 + Cortex-A55)
- Memory configuration
- Power domains
- Clock tree
- Interrupt controllers
- Base peripheral definitions

### DTB Merge Configuration
```makefile
BOARD_USES_QCOM_MERGE_DTBS_SCRIPT := true
TARGET_MERGE_DTBS_WILDCARD := *volcano*
```

**Purpose**: Merges all volcano-related DTB files from kernel output.

**Process**:
1. Kernel builds multiple DTB files for different board variants
2. Build system filters DTBs matching `*volcano*` pattern
3. Qualcomm merge script combines compatible DTBs
4. Merged DTB included in boot image

## DTBO (Device Tree Blob Overlay)

### DTBO Partition
- **Partition**: dtbo.img (separate partition)
- **Size**: 24 MB (0x1800000)
- **Configuration**: `TARGET_NEEDS_DTBOIMAGE := true`
- **Purpose**: Hardware variant-specific overlays

### DTBO Selection

The bootloader selects appropriate DTBO based on:
1. **Board Variant ID** - Read from hardware fuses
2. **SKU/Region** - Read from persistent properties
3. **Hardware Revision** - PCB version detection

### Common DTBO Overlays

#### Display Panel Variants
Different display panels may be used across production batches:
- Panel A: AMOLED 120Hz (Primary)
- Panel B: AMOLED 120Hz (Alternate vendor)

DTBO configures:
- Panel initialization sequences
- Brightness curves
- Color calibration
- Touch integration

#### Audio Codec Variants
Different audio codec configurations:
- Speaker amplifier variations
- Microphone configurations
- Headphone jack settings (if applicable)

#### Camera Sensor Variants
Different camera sensor modules:
- Primary sensor variations (Sony/Samsung)
- Secondary sensor variations
- Flash LED configurations

#### Regional Hardware Differences
- **Japan (JPN)**: FeliCa NFC chip (ST54J)
- **Global**: Standard NFC chip (ST21)
- **Pro Models**: Additional hardware features

#### Charging & Battery
- Battery capacity detection
- Charging IC configuration
- Thermal sensor mappings

## Building DTB/DTBO

### Kernel Configuration
The device tree source files are in kernel:
```
kernel/nothing/sm7635/arch/arm64/boot/dts/vendor/qcom/
├── volcano-*.dts          # Main board DTS files
├── volcano-*-overlay.dts  # DTBO overlay files
└── sm7635.dtsi           # SoC base definitions
```

### Build Process
```bash
# Build kernel with DTBs
make ARCH=arm64 O=out gki_defconfig vendor/pineapple_perf.config vendor/asteroids_perf.config
make ARCH=arm64 O=out Image.gz dtbs -j$(nproc)

# DTBs are in: out/arch/arm64/boot/dts/vendor/qcom/
```

### Device Tree Compiler
Uses `dtc` (Device Tree Compiler):
```bash
# Decompile DTB to DTS (human-readable)
dtc -I dtb -O dts -o volcano.dts volcano.dtb

# Compile DTS to DTB
dtc -I dts -O dtb -o volcano.dtb volcano.dts

# Check DTBO structure
dtc -I dtb -O dts -o overlay.dts dtbo.img
```

## Device Tree Properties

### Key Properties Configured

#### Hardware Identifiers
```
model = "Qualcomm Technologies, Inc. Volcano Nothing Phone 3a";
compatible = "qcom,volcano", "qcom,sm7635";
qcom,board-id = <0x03 0x00>;
qcom,msm-id = <0x03 0x10000>;
```

#### Memory Configuration
```
memory@a0000000 {
    device_type = "memory";
    reg = <0x0 0xa0000000 0x0 0x20000000>;  // Example: 8GB RAM
};
```

#### Display Configuration
```
&sde_dsi {
    qcom,dsi-display-primary = <&dsi_panel_nothing_asteroids>;
    qcom,boot-display = <&dsi_panel_nothing_asteroids>;
};

&dsi_panel_nothing_asteroids {
    qcom,mdss-dsi-panel-width = <1080>;
    qcom,mdss-dsi-panel-height = <2400>;
    qcom,mdss-dsi-panel-framerate = <120>;
    qcom,mdss-dsi-panel-clockrate = <920000000>;
};
```

#### GPIO/Pinctrl Configuration
```
&tlmm {
    fingerprint_reset_default: fingerprint_reset_default {
        mux {
            pins = "gpio25";
            function = "gpio";
        };
        config {
            pins = "gpio25";
            drive-strength = <2>;
            bias-disable;
            output-low;
        };
    };
};
```

#### Power Regulators
```
&pm8550_l1 {
    regulator-name = "pm8550_l1";
    regulator-min-microvolt = <1800000>;
    regulator-max-microvolt = <1800000>;
    qcom,init-voltage = <1800000>;
};
```

## DTBO Overlay Examples

### Example: Touchscreen Variant Overlay
```dts
&i2c_0 {
    touchscreen@5d {
        compatible = "goodix,gt9886";
        reg = <0x5d>;
        interrupt-parent = <&tlmm>;
        interrupts = <21 0x2008>;
        reset-gpios = <&tlmm 20 GPIO_ACTIVE_HIGH>;
        irq-gpios = <&tlmm 21 GPIO_ACTIVE_HIGH>;
    };
};
```

### Example: Camera Sensor Overlay
```dts
&i2c_1 {
    camera_main@10 {
        compatible = "sony,imx766";
        reg = <0x10>;
        qcom,cam-power-seq-val = <1 1 1>;
        qcom,cam-power-seq-delay = <1 1 5>;
    };
};
```

## Debugging Device Tree

### View Current Device Tree
```bash
# View compiled device tree from running device
adb root
adb pull /sys/firmware/devicetree/base devicetree
find devicetree -type f -exec sh -c 'echo "{}:"; cat "{}"' \;
```

### Check DTBO Loading
```bash
# Check bootloader log for DTBO selection
adb shell dmesg | grep -i "dtbo"
adb shell dmesg | grep -i "overlay"
```

### Verify Hardware Detection
```bash
# Check if hardware is properly detected via device tree
adb shell cat /proc/device-tree/model
adb shell cat /proc/device-tree/compatible
```

## Common Issues

### DTBO Selection Failure
**Symptom**: Device boots but hardware features not working.

**Causes**:
- DTBO partition corrupt or missing
- Bootloader can't match device variant to DTBO
- DTBO compatibility mismatch

**Solution**: 
1. Verify DTBO partition: `fastboot flash dtbo dtbo.img`
2. Check bootloader logs: `fastboot oem log`
3. Ensure DTB and DTBO versions match

### Hardware Not Detected
**Symptom**: Specific hardware (camera, touchscreen) not detected.

**Causes**:
- Missing device tree node
- GPIO configuration incorrect
- Power sequence timing issues

**Solution**:
1. Check kernel logs: `dmesg | grep -i <device>`
2. Verify device tree node exists
3. Check GPIO states: `cat /sys/kernel/debug/gpio`

### Panel/Display Issues
**Symptom**: Display not working or incorrect resolution.

**Causes**:
- Wrong panel DTBO selected
- Display timing parameters incorrect
- Power rails not configured

**Solution**:
1. Check display driver probe: `dmesg | grep -i "dsi\|panel"`
2. Verify panel power sequence
3. Check display DTBO overlay applied correctly

## Best Practices

1. **Version Control**: Keep DTS files in kernel source tree
2. **Overlay Minimization**: Only override necessary properties in DTBO
3. **Documentation**: Comment complex device tree configurations
4. **Testing**: Test all DTBO variants on actual hardware
5. **Validation**: Use `dtc` to validate syntax before building
6. **Compatibility**: Ensure DTB/DTBO compatibility across kernel versions

## References

- [Linux Device Tree Documentation](https://www.kernel.org/doc/html/latest/devicetree/index.html)
- [Android Device Tree Guide](https://source.android.com/devices/architecture/dto)
- [Qualcomm Device Tree Bindings](https://www.kernel.org/doc/Documentation/devicetree/bindings/arm/qcom.yaml)
- [Device Tree Compiler (dtc)](https://git.kernel.org/pub/scm/utils/dtc/dtc.git)
