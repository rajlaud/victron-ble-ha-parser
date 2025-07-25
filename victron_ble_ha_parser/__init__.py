"""A parser module for use by Home Assistant."""

from .custom_state_data import SensorDeviceClass, Units, Keys
from .parser import VictronBluetoothDeviceData
from victron_ble.devices.base import (
    OperationMode,
    ChargerError,
    AlarmReason,
)
from victron_ble.devices.battery_monitor import AuxMode
from victron_ble.devices.smart_lithium import BalancerStatus
from victron_ble.devices.dc_energy_meter import MeterType

__all__ = [
    "Keys",
    "Units",
    "SensorDeviceClass",
    "VictronBluetoothDeviceData",
    "OperationMode",
    "ChargerError",
    "AuxMode",
    "AlarmReason",
    "MeterType",
    "BalancerStatus",
]
