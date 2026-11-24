#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024-2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/nothing',
    'hardware/qcom-caf/sm8650',
    'vendor/qcom/common/vendor/perf',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libar-pal',
        'libar-acdb',
        'liblx-osal',
        'libats',
        'libagm',
        'libpalclient',
        'libglyph_lights_shim',
    ): lib_fixup_remove,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'com.qualcomm.qti.imscmservice@2.0',
        'com.qualcomm.qti.imscmservice@2.1',
        'com.qualcomm.qti.imscmservice@2.2',
        'com.qualcomm.qti.uceservice@2.0',
        'com.qualcomm.qti.uceservice@2.1',
        'com.qualcomm.qti.uceservice@2.2',
        'com.qualcomm.qti.uceservice@2.3',
        'libntf',
        'vendor.qti.ImsRtpService-V1-ndk',
        'vendor.qti.data.factoryservice-V1-ndk',
        'vendor.qti.data.mwqemaidlservice-V1-ndk',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.data.cneaidlservice.internal.api-V1-ndk',
        'vendor.qti.hardware.data.cneaidlservice.internal.constants-V1-ndk',
        'vendor.qti.hardware.data.cneaidlservice.internal.server-V1-ndk',
        'vendor.qti.hardware.data.connectionfactory-V1-ndk',
        'vendor.qti.hardware.data.dataactivity-V1-ndk',
        'vendor.qti.hardware.data.dynamicddsaidlservice-V1-ndk',
        'vendor.qti.hardware.data.flowaidlservice-V1-ndk',
        'vendor.qti.hardware.data.iwlandata-V1-ndk',
        'vendor.qti.hardware.data.ka-V1-ndk',
        'vendor.qti.hardware.data.lceaidlservice-V1-ndk',
        'vendor.qti.hardware.data.qmiaidlservice-V1-ndk',
        'vendor.qti.hardware.dpmaidlservice-V1-ndk',
        'vendor.qti.hardware.limits@1.0',
        'vendor.qti.hardware.limits@1.1',
        'vendor.qti.hardware.mwqemadapteraidlservice-V1-ndk',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccsyshal@1.2',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.ims.callcapability@1.0',
        'vendor.qti.ims.callcapabilityaidlservice-V1-ndk',
        'vendor.qti.ims.callinfo@1.0',
        'vendor.qti.ims.configaidlservice-V1-ndk',
        'vendor.qti.ims.connectionaidlservice-V1-ndk',
        'vendor.qti.ims.factory@1.0',
        'vendor.qti.ims.factory@1.1',
        'vendor.qti.ims.factoryaidlservice-V1-ndk',
        'vendor.qti.ims.rcsconfig@2.0',
        'vendor.qti.ims.rcsconfig@2.1',
        'vendor.qti.ims.rcssipaidlservice-V1-ndk',
        'vendor.qti.ims.rcsuceaidlservice-V1-ndk',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
        'vendor.qti.latencyaidlservice-V1-ndk',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
        'vendor.qti.qspmhal-V1-ndk',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    # The stock RC starts a daemon absent from the Asteroids vendor payload.
    'vendor/etc/init/init.vendor.wlan.rc': blob_fixup()
        .regex_replace(
            r'\nservice wifi_qos_daemon /vendor/bin/wifi_qos_daemon\n'
            r'    class late_start\n'
            r'    user wifi\n'
            r'    group wifi inet net_admin oem_2912 system\n'
            r'    capabilities NET_ADMIN\n'
            r'    oneshot\n',
            '',
        ),
    'vendor/bin/init.qti.kernel.sh': blob_fixup()
        .regex_replace(r'(?m)^start_msm_irqbalance\n', ''),
    (
        'vendor/lib64/libdpps.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    (
        'vendor/lib64/libqms_client.so',
        'vendor/bin/qcc-vendor',
        'vendor/bin/xtra-daemon',
        'vendor/bin/qms',
        'vendor/lib64/libcne.so',
        'vendor/lib64/libqcc_sdk.so',
    ): blob_fixup()
        .add_needed('libbinder_shim.so'),
    (
        'vendor/etc/seccomp_policy/c2audio.vendor.base-arm64.policy',
        'vendor/etc/seccomp_policy/codec2.vendor.base-arm64.policy',
    ): blob_fixup()
        .regex_replace(r'(?ms)(^munmap: 1\n.*?)^munmap: 1\n', r'\1'),
    (
        'vendor/etc/seccomp_policy/c2audio.vendor.ext-arm64.policy',
        'vendor/etc/seccomp_policy/codec2.vendor.ext-arm64.policy',
    ): blob_fixup()
        .regex_replace(r'(?m)^(_llseek|getdents64): 1\n', ''),
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': blob_fixup()
        .add_line_if_missing('lseek: 1'),
    'vendor/etc/lvacfs_params/1mic/LVACFS_Configuration.txt': blob_fixup()
        .patch_file('audio/lvacfs_1mic_config.patch'),
    'vendor/etc/lvacfs_params/2mic/LVACFS_Configuration.txt': blob_fixup()
        .patch_file('audio/lvacfs_2mic_config.patch'),
    'vendor/lib64/libarcsoft_dark_vision_raw.so': blob_fixup()
        .clear_symbol_version('remote_register_buf')
        .clear_symbol_version('rpcmem_alloc')
        .clear_symbol_version('rpcmem_free'),
    (
        'vendor/lib64/libcapiv2uvvendor.so',
        'vendor/lib64/liblistensoundmodel2vendor.so',
        'vendor/lib64/libVoiceSdk.so',
    ): blob_fixup().replace_needed(
        'libtensorflowlite_c.so',
        'libtensorflowlite_c_vendor.so',
    ),
    'vendor/bin/hw/vendor.qti.hardware.lights.service': blob_fixup()
        .add_needed('libglyph_lights_shim.so'),
    'vendor/lib64/hw/libproviderextension.so': blob_fixup()
        .replace_needed('android.hardware.graphics.allocator-V2-ndk.so', 'android.hardware.graphics.allocator-V1-ndk.so'),
    'vendor/lib64/libmorpho_RapidEffect.so': blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/lib64/libntcamallocator.so': blob_fixup()
        .add_needed('libui_shim.so'),
    'vendor/lib64/libntcamskia.so': blob_fixup()
        .add_needed('libnativewindow.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libbinder_shim.so')
        .add_needed('libhidlbase_shim.so'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'vendor/lib64/libwa_sat.so': blob_fixup()
        .binary_regex_replace(b'/system\x00', b'/vendor\x00'),
}  # fmt: skip

module = ExtractUtilsModule(
    'asteroids',
    'nothing',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
