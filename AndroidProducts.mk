#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

PRODUCT_MAKEFILES := \
    $(LOCAL_DIR)/clover_asteroids.mk \
    $(LOCAL_DIR)/voltage_asteroids.mk

COMMON_LUNCH_CHOICES := \
    voltage_asteroids-cp2a-user \
    voltage_asteroids-cp2a-userdebug \
    voltage_asteroids-cp2a-eng \
    voltage_asteroids-user \
    voltage_asteroids-userdebug \
    voltage_asteroids-eng
