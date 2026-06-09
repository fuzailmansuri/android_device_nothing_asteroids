/*
 * Copyright (C) 2026 The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

package com.nothing.kafka;

import android.content.Context;
import android.database.ContentObserver;
import android.net.Uri;
import android.os.Handler;

public class EventObserver extends ContentObserver {

    public interface EventCallback {
        void updateEvent(String str);
    }

    private Uri mUri;

    public EventObserver(Context context, Handler handler, String eventTag) {
        super(handler);
        this.mUri = Uri.parse("content://com.nothing.proxy.kafka.provider/" + eventTag);
    }

    public void register(EventCallback callback, boolean bool) {
        // Stub implementation, no-op
    }

    public void unregister() {
        // Stub implementation, no-op
    }
}
