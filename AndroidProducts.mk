#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

PRODUCT_MAKEFILES := \
    $(LOCAL_DIR)/lineage_asteroids.mk \
    $(LOCAL_DIR)/yaap_asteroids.mk \
    $(LOCAL_DIR)/custom_asteroids.mk

COMMON_LUNCH_CHOICES := \
    lineage_asteroids-cp2a-user \
    lineage_asteroids-cp2a-userdebug \
    lineage_asteroids-cp2a-eng
