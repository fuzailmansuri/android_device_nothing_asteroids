/*
 * Copyright (C) 2026 The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

package com.nothing.kafka;

import android.content.Context;

public class EventProducer {

    public static final String AUTHORITY = "com.nothing.proxy.kafka.provider";
    private static EventProducer sInstance;

    public static synchronized EventProducer getInstance(Context context) {
        if (sInstance == null) {
            sInstance = new EventProducer();
        }
        return sInstance;
    }

    public void fire(String eventTag, String eventValue) {
        // Stub implementation, no-op
    }
}
