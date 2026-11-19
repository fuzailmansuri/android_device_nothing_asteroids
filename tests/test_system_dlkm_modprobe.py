#!/usr/bin/env python3
"""Exercise the boot loader with a fake modprobe; never load host modules."""

from pathlib import Path
import os
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "init/system_dlkm_modprobe.sh"
VENDOR_SCRIPT = SCRIPT.with_name("vendor_modprobe.sh")


class ModuleLoaderTest(unittest.TestCase):
    def run_loader(self, *, nested=False, fail="", blocklist="", metadata=True):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            system = root / "system"
            vendor = root / "vendor"
            directory = system / "android17-6.1" if nested else system
            directory.mkdir(parents=True)
            vendor.mkdir()
            log = root / "calls"
            modprobe = root / "modprobe"
            modprobe.write_text(
                "#!/bin/sh\n"
                f"printf '%s\\n' \"$5\" >> '{log}'\n"
                f"[ \"$3\" = '{directory}' ] || exit 2\n"
                f"[ \"$5\" != '{fail}' ]\n"
            )
            modprobe.chmod(0o755)
            if metadata:
                (directory / "modules.dep").write_text("")
                # Final line deliberately lacks a newline.
                (directory / "modules.load").write_text("# boot modules\ndiag\ncan_bcm\ntipc")
            (vendor / "system_dlkm.modules.blocklist").write_text(blocklist)
            script = root / "loader.sh"
            script.write_text(
                SCRIPT.read_text()
                .replace('SYSTEM_DLKM_DIR="/system_dlkm/lib/modules"', f'SYSTEM_DLKM_DIR="{system}"')
                .replace('VENDOR_DLKM_DIR="/vendor_dlkm/lib/modules"', f'VENDOR_DLKM_DIR="{vendor}"')
                .replace('MODPROBE="/vendor/bin/modprobe"', f'MODPROBE="{modprobe}"')
            )
            result = subprocess.run(["sh", str(script)], capture_output=True, text=True)
            calls = log.read_text().splitlines() if log.exists() else []
            return result, calls

    def test_flat_layout_preserves_order(self):
        result, calls = self.run_loader()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ["diag", "can_bcm", "tipc"])

    def test_version_directory(self):
        result, calls = self.run_loader(nested=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ["diag", "can_bcm", "tipc"])

    def test_failure_is_reported_after_remaining_modules_are_attempted(self):
        result, calls = self.run_loader(fail="diag")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(calls, ["diag", "can_bcm", "tipc"])

    def test_blocklist_normalizes_module_names(self):
        result, calls = self.run_loader(blocklist="# comment\nblocklist can-bcm\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ["diag", "tipc"])

    def test_missing_metadata_is_failure(self):
        result, calls = self.run_loader(metadata=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(calls, [])
        self.assertIn("dependency index", result.stderr)

    def test_final_blocklist_entry_without_newline(self):
        result, calls = self.run_loader(blocklist="blocklist tipc")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ["diag", "can_bcm"])


class VendorLoaderTest(unittest.TestCase):
    def run_loader(self, *, fail="", audio_arch="audioreach"):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / "vendor_dlkm"
            directory.mkdir()
            (directory / "modules.dep").write_text("")
            (directory / "modules.load").write_text("adsp_loader_dlkm\nlegacy_audio\nfrpc-adsprpc")
            (directory / "modules.audio.ar.blocklist").write_text("blocklist legacy-audio")
            log = root / "calls"
            prop = root / "properties"
            for name, body in {
                "modprobe": f"printf '%s\\n' \"$5\" >> '{log}'\n[ \"$5\" != '{fail}' ]\n",
                "getprop": f"printf '%s\\n' '{audio_arch}'\n",
                "setprop": f"printf '%s %s\\n' \"$1\" \"$2\" >> '{prop}'\n",
            }.items():
                command = root / name
                command.write_text("#!/bin/sh\n" + body)
                command.chmod(0o755)
            script = root / "loader.sh"
            script.write_text(
                VENDOR_SCRIPT.read_text()
                .replace('VENDOR_DLKM_DIR="/vendor_dlkm/lib/modules"', f'VENDOR_DLKM_DIR="{directory}"')
                .replace('VENDOR_DIR="/vendor/lib/modules"', f'VENDOR_DIR="{root / "absent"}"')
                .replace('MODPROBE="/vendor/bin/modprobe"', f'MODPROBE="{root / "modprobe"}"')
            )
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"])
            result = subprocess.run(["sh", str(script)], env=env, capture_output=True, text=True)
            return result, log.read_text().splitlines(), prop.read_text().splitlines()

    def test_dsp_order_and_audio_blocklist(self):
        result, calls, properties = self.run_loader()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ["adsp_loader_dlkm", "frpc-adsprpc"])
        self.assertEqual(properties, ["vendor.all.modules.ready 1"])

    def test_failure_does_not_skip_other_modules_or_deadlock_init(self):
        result, calls, properties = self.run_loader(fail="adsp_loader_dlkm")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(calls, ["adsp_loader_dlkm", "frpc-adsprpc"])
        self.assertEqual(properties, ["vendor.all.modules.ready 1"])

    def test_legacy_audio_uses_its_own_blocklist(self):
        result, calls, properties = self.run_loader(audio_arch="legacy")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, ["adsp_loader_dlkm", "legacy_audio", "frpc-adsprpc"])


if __name__ == "__main__":
    unittest.main()
