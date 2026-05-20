#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-FileCopyrightText: 2026 YAAP
# SPDX-License-Identifier: Apache-2.0
#

TARGET_BUILD_GAPPS := true
TARGET_ENABLE_EPPE := true

$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

$(call inherit-product, device/nothing/asteroids/device.mk)
$(call inherit-product, vendor/yaap/config/common_full_phone.mk)

PRODUCT_BRAND := Nothing
PRODUCT_DEVICE := asteroids
PRODUCT_MANUFACTURER := Nothing
PRODUCT_MODEL := A059
PRODUCT_NAME := yaap_asteroids

PRODUCT_GMS_CLIENTID_BASE := android-nothing

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildFingerprint=Nothing/Asteroids/Asteroids:17/CQ2A.260522.002-CP2A.260605.016/2611061007:user/release-keys \
    BuildSystemFingerprint=qti/qssi_64/qssi_64:17/CQ2A.260522.002-CP2A.260605.016/2611061007:user/release-keys \
    DeviceName=Asteroids \
    DeviceProduct=Asteroids \
    SystemDevice=Asteroids \
    SystemName=Asteroids
