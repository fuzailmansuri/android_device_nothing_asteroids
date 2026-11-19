#!/vendor/bin/sh
# SPDX-License-Identifier: Apache-2.0

VENDOR_DLKM_DIR="/vendor_dlkm/lib/modules"
VENDOR_DIR="/vendor/lib/modules"
MODPROBE="/vendor/bin/modprobe"
audio_arch=$(getprop ro.boot.audio)

for dir in "$VENDOR_DLKM_DIR" "$VENDOR_DIR"; do
    [ -f "$dir/modules.dep" ] && [ -f "$dir/modules.load" ] || continue

    case "$audio_arch" in
        audioreach) audio_blocklist="$dir/modules.audio.ar.blocklist" ;;
        audiolite) audio_blocklist="$dir/modules.audio.audiolite.blocklist" ;;
        *) audio_blocklist="$dir/modules.audio.legacy.blocklist" ;;
    esac

    blocked_modules=""
    for blocklist in "$dir/modules.blocklist" "$audio_blocklist"; do
        [ -f "$blocklist" ] || continue
        while read -r keyword module rest || [ -n "$keyword" ]; do
            [ "$keyword" = blocklist ] || continue
            module=$(printf '%s' "${module%.ko}" | tr '-' '_')
            blocked_modules="$blocked_modules $module"
        done < "$blocklist"
    done

    status=0
    while read -r module rest || [ -n "$module" ]; do
        case "$module" in ""|\#*) continue ;; esac
        name=${module##*/}
        name=$(printf '%s' "${name%.ko}" | tr '-' '_')
        case " $blocked_modules " in *" $name "*) continue ;; esac
        # Serialize initialization, including remoteproc and DSP dependencies.
        "$MODPROBE" -b -d "$dir" -a "$module" || status=1
    done < "$dir/modules.load"

    # Qualcomm init waits for completion, even when an optional driver failed.
    setprop vendor.all.modules.ready 1 || exit 1
    exit "$status"
done

echo "No vendor module load list and dependency index found" >&2
exit 1
