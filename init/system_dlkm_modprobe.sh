#! /vendor/bin/sh

SYSTEM_DLKM_DIR="/system_dlkm/lib/modules"
VENDOR_DLKM_DIR="/vendor_dlkm/lib/modules"

MODPROBE="/vendor/bin/modprobe"

blocked_modules=""
if [ -f "${VENDOR_DLKM_DIR}/system_dlkm.modules.blocklist" ]; then
    while read -r keyword module rest || [ -n "$keyword" ]; do
        [ "$keyword" = blocklist ] || continue
        module=$(printf '%s' "${module%.ko}" | tr '-' '_')
        blocked_modules="$blocked_modules $module"
    done < "${VENDOR_DLKM_DIR}/system_dlkm.modules.blocklist"
fi

# YAAP can install modules flat or under a kernel-version directory.
for dir in "$SYSTEM_DLKM_DIR" "$SYSTEM_DLKM_DIR"/*; do
    [ -f "$dir/modules.dep" ] && [ -f "$dir/modules.load" ] || continue
    status=0
    while read -r module rest || [ -n "$module" ]; do
        case "$module" in ""|\#*) continue ;; esac
        name=${module##*/}
        name=$(printf '%s' "${name%.ko}" | tr '-' '_')
        case " $blocked_modules " in *" $name "*) continue ;; esac
        # Keep the packaged order and try the rest even if one driver fails.
        "$MODPROBE" -b -d "$dir" -a "$module" || status=1
    done < "$dir/modules.load"
    exit "$status"
done

echo "No system_dlkm module load list and dependency index found" >&2
exit 1
