"""Live BLE test driver for victron-ble-ha-parser.

Scans for nearby Victron devices, locks onto the first matching device,
and prints sensor updates only when values change.

Usage:
    python test_live.py <advertisement_key> [--address AA:BB:CC:DD:EE:FF] [--duration 30]
"""

import argparse
import asyncio

from bleak import BleakScanner
from home_assistant_bluetooth import BluetoothServiceInfo
from victron_ble_ha_parser import VictronBluetoothDeviceData

VICTRON = 0x02E1


async def scan(key: str, address: str | None, duration: int) -> None:
    parser = VictronBluetoothDeviceData(advertisement_key=key)
    locked_address: str | None = address
    failed_addresses: set = set()
    last_values: dict = {}

    def callback(device, adv):
        nonlocal locked_address, last_values

        if VICTRON not in adv.manufacturer_data:
            return

        raw = adv.manufacturer_data[VICTRON]
        if not raw.startswith(b"\x10"):
            return

        # Skip devices we've already ruled out
        if device.address in failed_addresses:
            return

        # Once locked, ignore other devices
        if locked_address and device.address.upper() != locked_address.upper():
            return

        # Before locking, verify the key actually works for this device
        if not locked_address:
            from victron_ble.devices import detect_device_type
            device_parser = detect_device_type(raw)
            if device_parser is None:
                failed_addresses.add(device.address)
                return
            try:
                parsed = device_parser(key).parse(raw)
            except (ValueError, Exception):
                parsed = None
            if parsed is None:
                failed_addresses.add(device.address)
                print(f"  Skipping {device.name} ({device.address}) — key mismatch")
                return
            locked_address = device.address
            print(f"Locked onto {device.name} ({device.address})")

        info = BluetoothServiceInfo(
            device.name or "Unknown",
            device.address,
            adv.rssi,
            adv.manufacturer_data,
            adv.service_data or {},
            adv.service_uuids or [],
            "local",
        )

        result = parser.update(info)

        # Build current values dict
        current_values = {}
        for dev_key, val in result.entity_values.items():
            current_values[dev_key.key] = val.native_value

        # Only print when values change
        if current_values == last_values:
            return
        last_values = current_values

        print(f"\n--- {device.name} ({device.address}) RSSI={adv.rssi} ---")
        for dev_key in result.entity_descriptions:
            desc = result.entity_descriptions[dev_key]
            val = result.entity_values.get(dev_key)
            unit = desc.native_unit_of_measurement or ""
            print(f"  {val.name}: {val.native_value} {unit}")

    print(f"Scanning for Victron devices ({duration}s)...")
    if address:
        print(f"Filtering for address: {address}")
    print()

    scanner = BleakScanner(detection_callback=callback)
    await scanner.start()
    await asyncio.sleep(duration)
    await scanner.stop()
    print("\nScan complete.")


def main():
    ap = argparse.ArgumentParser(description="Live test for victron-ble-ha-parser")
    ap.add_argument("key", help="Advertisement encryption key (hex string)")
    ap.add_argument("--address", "-a", help="Filter to a specific MAC address")
    ap.add_argument("--duration", "-d", type=int, default=30, help="Scan duration in seconds (default: 30)")
    args = ap.parse_args()

    asyncio.run(scan(args.key, args.address, args.duration))


if __name__ == "__main__":
    main()
