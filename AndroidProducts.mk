#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-FileCopyrightText: 2026 VoltageOS
# SPDX-License-Identifier: Apache-2.0
#

PRODUCT_MAKEFILES := \
    $(LOCAL_DIR)/yaap_asteroids.mk \
    $(LOCAL_DIR)/voltage_asteroids.mk \
    $(LOCAL_DIR)/lineage_asteroids.mk

COMMON_LUNCH_CHOICES := \
    yaap_asteroids-cp2a-user \
    yaap_asteroids-cp2a-userdebug \
    yaap_asteroids-cp2a-eng \
    voltage_asteroids-cp2a-user \
    voltage_asteroids-cp2a-userdebug \
    voltage_asteroids-cp2a-eng
