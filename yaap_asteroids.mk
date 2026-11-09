#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

TARGET_BUILD_GAPPS := true

$(call inherit-product, device/nothing/asteroids/device.mk)
$(call inherit-product, vendor/yaap/config/common_full_phone.mk)

PRODUCT_BRAND := Nothing
PRODUCT_DEVICE := asteroids
PRODUCT_MANUFACTURER := Nothing
PRODUCT_MODEL := A059
PRODUCT_NAME := yaap_asteroids

PRODUCT_GMS_CLIENTID_BASE := android-nothing

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="qssi_64-user 17 CQ2A.260522.002-CP2A.260605.016 2610232146 release-keys" \
    BuildFingerprint=Nothing/Asteroids/Asteroids:14/UKQ1.260129.001/2610232146:user/release-keys \
    DeviceName=Asteroids \
    DeviceProduct=Asteroids \
    SystemDevice=Asteroids \
    SystemName=Asteroids

TARGET_ENABLE_BLUR := true
TARGET_SUPPORTS_QUICK_TAP := true
TARGET_FACE_UNLOCK_SUPPORTED := true
