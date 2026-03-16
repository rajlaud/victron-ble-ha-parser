"""Tests for all supported device types."""

import pytest
from home_assistant_bluetooth import BluetoothServiceInfo
from syrupy.assertion import SnapshotAssertion

from victron_ble_ha_parser import VictronBluetoothDeviceData

# Test data from upstream keshavdv/victron-ble test suite

DEVICES = {
    "battery_monitor": {
        "name": "SmartShunt",
        "advertisement": "100289a302b040af925d09a4d89aa0128bdef48c6298a9",
        "key": "aff4d0995b7d1e176c0c33ecb9e70dcd",
    },
    "battery_sense": {
        "name": "Smart Battery Sense",
        "advertisement": "1000a4a3025f150d8dcbff517f30eb65e76b22a04ac4e1",
        "key": "0da694539597f9cf6c613cde60d7bf05",
    },
    "solar_charger": {
        "name": "BlueSolar MPPT",
        "advertisement": "100242a0016207adceb37b605d7e0ee21b24df5c",
        "key": "adeccb947395801a4dd45a2eaa44bf17",
    },
    "dc_dc_converter": {
        "name": "Orion Smart DC-DC",
        "advertisement": "1000c0a304121d64ca8d442b90bbdf6a8cba",
        "key": "64ba49f1a8562e45197a8e1fe50d7658",
    },
    "dc_energy_meter": {
        "name": "DC Energy Meter",
        "advertisement": "100289a30d787fafde83ccec982199fd815286",
        "key": "aff4d0995b7d1e176c0c33ecb9e70dcd",
    },
    "smart_battery_protect": {
        "name": "Smart Battery Protect",
        "advertisement": "1080b0a3093523fadedea38b1af8bcbde91ca8b6dbb60e",
        "key": "fac570d66380b797a5b7543758be00e4",
    },
    "vebus": {
        "name": "MultiPlus-II",
        "advertisement": "100380270c1252dad26f0b8eb39162074d140df410",
        "key": "da3f5fa2860cb1cf86ba7a6d1d16b9dd",
    },
    "ac_charger": {
        "name": "Smart Charger",
        "advertisement": "100030a308f926c1b5170a0d2280335bf12d5ed083",
        "key": "c129cf8f75c3fe5a1655b481e205fb7d",
    },
}


def make_service_info(device_id: str) -> BluetoothServiceInfo:
    device = DEVICES[device_id]
    return BluetoothServiceInfo(
        name=device["name"],
        address="AA:BB:CC:DD:EE:FF",
        rssi=-60,
        manufacturer_data={0x02E1: bytes.fromhex(device["advertisement"])},
        service_data={},
        service_uuids=[],
        source="local",
    )


@pytest.mark.parametrize("device_id", DEVICES.keys())
class TestDeviceSupported:
    def test_supported(self, device_id: str) -> None:
        """Test that each device type is recognized as supported."""
        device = VictronBluetoothDeviceData(DEVICES[device_id]["key"])
        assert device.supported(make_service_info(device_id))


@pytest.mark.parametrize("device_id", DEVICES.keys())
class TestDeviceSensors:
    def test_sensors(self, device_id: str, snapshot: SnapshotAssertion) -> None:
        """Test that each device type produces the expected sensor update."""
        device = VictronBluetoothDeviceData(DEVICES[device_id]["key"])
        update = device.update(make_service_info(device_id))
        assert update == snapshot


def make_service_info_with_data(manufacturer_data: bytes) -> BluetoothServiceInfo:
    """Create a BluetoothServiceInfo with arbitrary Victron manufacturer data."""
    return BluetoothServiceInfo(
        name="Test Device",
        address="AA:BB:CC:DD:EE:FF",
        rssi=-60,
        manufacturer_data={0x02E1: manufacturer_data},
        service_data={},
        service_uuids=[],
        source="local",
    )


# A known-good advertisement payload used to exercise key validation in isolation.
_BATTERY_MONITOR_ADV = bytes.fromhex(
    DEVICES["battery_monitor"]["advertisement"]
)


@pytest.mark.parametrize(
    "raw_data",
    [
        b"",
        b"\x10",
        bytes.fromhex("deadbeef"),
    ],
)
class TestMalformedManufacturerData:
    """Malformed manufacturer data must never raise and must not be reported as supported."""

    def test_supported_returns_false(self, raw_data: bytes) -> None:
        """supported() returns False for malformed advertisement payloads."""
        device = VictronBluetoothDeviceData(DEVICES["battery_monitor"]["key"])
        assert not device.supported(make_service_info_with_data(raw_data))

    def test_validate_key_returns_false(self, raw_data: bytes) -> None:
        """validate_advertisement_key() returns False for malformed advertisement payloads."""
        device = VictronBluetoothDeviceData(DEVICES["battery_monitor"]["key"])
        assert device.validate_advertisement_key(raw_data) is False


@pytest.mark.parametrize(
    "key",
    [
        "",
        "not-hex",
        "00",
    ],
)
class TestInvalidAdvertisementKey:
    """Invalid advertisement keys must never raise and validate_advertisement_key must return False."""

    def test_validate_key_returns_false(self, key: str) -> None:
        """validate_advertisement_key() returns False for invalid key strings."""
        device = VictronBluetoothDeviceData(key)
        assert device.validate_advertisement_key(_BATTERY_MONITOR_ADV) is False
