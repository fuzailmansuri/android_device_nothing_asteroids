#
# SPDX-FileCopyrightText: 2026 VoltageOS
# SPDX-License-Identifier: Apache-2.0
#

$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

$(call inherit-product, device/nothing/asteroids/device.mk)
$(call inherit-product, vendor/voltage/config/common_full_phone.mk)

PRODUCT_BRAND := Nothing
PRODUCT_DEVICE := asteroids
PRODUCT_MANUFACTURER := Nothing
PRODUCT_MODEL := A059
PRODUCT_NAME := voltage_asteroids

PRODUCT_GMS_CLIENTID_BASE := android-nothing

TARGET_SCREEN_HEIGHT := 2412
TARGET_SCREEN_WIDTH := 1080

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="qssi_64-user 17 CQ2A.260522.002-CP2A.260605.016 2609152123 release-keys" \
    BuildFingerprint=Nothing/Asteroids/Asteroids:14/UKQ1.260129.001/2609152123:user/release-keys \
    DeviceName=Asteroids \
    DeviceProduct=Asteroids \
    SystemDevice=Asteroids \
    SystemName=Asteroids

# Maintainer
PRODUCT_SYSTEM_DEFAULT_PROPERTIES += \
    ro.voltage.maintainer=fruitzail

# Enforce all requested product packages exist
$(call enforce-product-packages-exist, \
    Calendar \
    Camera2 \
    Gallery2 \
    com.android.ranging \
    rild \
    product_manifest.xml \
)
