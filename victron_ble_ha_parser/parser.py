"""Data class for Victron BLE suitable for Home Assistant integration."""

import logging
from struct import error as struct_error

from bluetooth_sensor_state_data import BluetoothData

from home_assistant_bluetooth import BluetoothServiceInfo

from victron_ble.devices import (
    BatteryMonitor,
    BatteryMonitorData,
    DcDcConverter,
    DcDcConverterData,
    DcEnergyMeter,
    DcEnergyMeterData,
    SolarCharger,
    SolarChargerData,
    SmartBatteryProtect,
    SmartBatteryProtectData,
    SmartLithium,
    SmartLithiumData,
    VEBus,
    VEBusData,
    detect_device_type,
)

from .custom_state_data import Keys, SensorDeviceClass, Units

_LOGGER = logging.getLogger(__name__)

VICTRON_IDENTIFIER = 0x02E1


class VictronBluetoothDeviceData(BluetoothData):
    """Class to hold Victron BLE device data."""

    def __init__(self, advertisement_key: str | None = None) -> None:
        """Initialize the Victron Bluetooth device data with an encryption key."""
        super().__init__()
        self._advertisement_key: str | None = advertisement_key

    def validate_advertisement_key(self, data: bytes) -> bool:
        """Validate the advertisement key."""
        if not self._advertisement_key:
            _LOGGER.debug("Advertisement key not set")
            return False

        parser = detect_device_type(data)
        if parser is None:
            _LOGGER.error("Unable to detect device type")
            return False

        parsed_data = parser(self._advertisement_key).parse_container(data)
        if parsed_data is None:
            _LOGGER.error("Unable to parse data")
            return False

        encrypted_data = parsed_data.encrypted_data

        try:
            key_first_byte = bytes.fromhex(self._advertisement_key)[0]
        except ValueError:
            _LOGGER.error("Invalid advertisement key")
            return False

        if encrypted_data[0] != key_first_byte:
            # only possible check is whether the first byte matches
            _LOGGER.error("Advertisement key does not match")
            return False

        return True

    def _start_update(self, data: BluetoothServiceInfo) -> None:
        try:
            raw_data = data.manufacturer_data[VICTRON_IDENTIFIER]
        except (KeyError, IndexError):
            # not a Victron device
            return

        if not raw_data.startswith(b"\x10"):
            # not an instant-update advertisement
            return

        try:
            parser = detect_device_type(raw_data)
        except struct_error:
            parser = None

        if parser is None:
            _LOGGER.debug("Ignoring unsupported advertisement %s", raw_data.hex())
            return
        if not issubclass(
            parser,
            (
                BatteryMonitor,
                DcDcConverter,
                DcEnergyMeter,
                SmartBatteryProtect,
                SmartLithium,
                SolarCharger,
                VEBus,
            ),
        ):
            _LOGGER.debug("Unsupported device type")
            return
        self.set_device_manufacturer(data.manufacturer or "Victron")
        self.set_device_name(data.name)
        self.set_device_type(parser.__name__)
        if not self.validate_advertisement_key(raw_data):
            return
        assert self._advertisement_key is not None  # keep pylance happy

        try:
            parsed_data = parser(self._advertisement_key).parse(raw_data)
        except ValueError:
            parsed_data = None
        if parsed_data is None:
            _LOGGER.debug("Unable to parse data")
            return
        if isinstance(parsed_data, BatteryMonitorData):
            self._update_battery_monitor(parsed_data)
        elif isinstance(parsed_data, DcDcConverterData):
            self._update_dc_dc_converter(parsed_data)
        elif isinstance(parsed_data, DcEnergyMeterData):
            self._update_dc_energy_meter(parsed_data)
        elif isinstance(parsed_data, SolarChargerData):
            self._update_solar_charger(parsed_data)
        elif isinstance(parsed_data, SmartBatteryProtectData):
            self._update_smart_battery_protect(parsed_data)
        elif isinstance(parsed_data, SmartLithiumData):
            self._update_smart_lithium(parsed_data)
        elif isinstance(parsed_data, VEBusData):
            self._update_vebus(parsed_data)

    def _update_battery_monitor(self, data: BatteryMonitorData) -> None:
        self.update_sensor(
            Keys.REMAINING_MINUTES,
            Units.TIME_MINUTES,  # type: ignore [arg-type]
            data.get_remaining_mins(),
            SensorDeviceClass.DURATION,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.CURRENT,
            Units.ELECTRIC_CURRENT_AMPERE,  # type: ignore [arg-type]
            data.get_current(),
            SensorDeviceClass.CURRENT,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.STATE_OF_CHARGE,
            Units.PERCENTAGE,  # type: ignore [arg-type]
            data.get_soc(),
            SensorDeviceClass.BATTERY,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.CONSUMED_AMPERE_HOURS,
            Units.ELECTRIC_CURRENT_FLOW_AMPERE_HOUR,  # type: ignore [arg-type]
            data.get_consumed_ah(),
            SensorDeviceClass.CURRENT_FLOW,  # type: ignore [arg-type]
        )
        alarm = data.get_alarm()
        self.update_sensor(
            Keys.ALARM,
            None,
            alarm.name if alarm else "no alarm",
        )
        self.update_sensor(
            Keys.AUX_MODE,
            None,
            data.get_aux_mode().name,
        )
        self.update_sensor(
            Keys.TEMPERATURE,
            Units.TEMP_CELSIUS,  # type: ignore [arg-type]
            data.get_temperature(),
            SensorDeviceClass.TEMPERATURE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.STARTER_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_starter_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.MIDPOINT_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_midpoint_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )

    def _update_dc_dc_converter(self, data: DcDcConverterData) -> None:
        charge_state = data.get_charge_state()
        self.update_sensor(
            Keys.CHARGE_STATE,
            None,
            charge_state.name if charge_state else None,
        )
        charger_error = data.get_charger_error()
        self.update_sensor(
            Keys.CHARGER_ERROR,
            None,
            charger_error.name if charger_error else None,
        )
        self.update_sensor(
            Keys.INPUT_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_input_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )
        off_reason = data.get_off_reason()
        self.update_sensor(
            Keys.OFF_REASON,
            None,
            off_reason.name if off_reason else None,
        )
        self.update_sensor(
            Keys.OUTPUT_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_output_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )

    def _update_dc_energy_meter(self, data: DcEnergyMeterData) -> None:
        meter_type = data.get_meter_type()
        if meter_type is not None:
            meter_type_string = meter_type.name
        else:
            meter_type_string = None
        self.update_sensor(
            Keys.METER_TYPE,
            None,
            meter_type_string,
        )
        self.update_sensor(
            Keys.CURRENT,
            Units.ELECTRIC_CURRENT_AMPERE,  # type: ignore [arg-type]
            data.get_current(),
            SensorDeviceClass.CURRENT,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )
        alarm = data.get_alarm()
        self.update_sensor(
            Keys.ALARM,
            None,
            alarm.name if alarm else "no alarm",
        )
        self.update_sensor(
            Keys.TEMPERATURE,
            Units.TEMP_CELSIUS,  # type: ignore [arg-type]
            data.get_temperature(),
            SensorDeviceClass.TEMPERATURE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.AUX_MODE,
            None,
            data.get_aux_mode().name,
        )
        self.update_sensor(
            Keys.TEMPERATURE,
            Units.TEMP_CELSIUS,  # type: ignore [arg-type]
            data.get_temperature(),
            SensorDeviceClass.TEMPERATURE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.STARTER_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_starter_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )

    def _update_smart_battery_protect(self, data: SmartBatteryProtectData) -> None:
        device_state = data.get_device_state()
        self.update_sensor(
            Keys.DEVICE_STATE,
            None,
            device_state.name if device_state else None,
        )
        output_state = data.get_output_state()
        self.update_sensor(
            Keys.OUTPUT_STATE,
            None,
            output_state.name if output_state else None,
        )
        error_code = data.get_error_code()
        self.update_sensor(
            Keys.ERROR_CODE,
            None,
            error_code.name if error_code else None,
        )
        alarm_reason = data.get_alarm_reason()
        self.update_sensor(
            Keys.ALARM,
            None,
            alarm_reason.name if alarm_reason else None,
        )
        warning_reason = data.get_warning_reason()
        self.update_sensor(
            Keys.WARNING,
            None,
            warning_reason.name if warning_reason else None,
        )
        off_reason = data.get_off_reason()
        self.update_sensor(
            Keys.OFF_REASON,
            None,
            off_reason.name if off_reason else None,
        )
        self.update_sensor(
            Keys.INPUT_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_input_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.OUTPUT_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_output_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )

    def _update_smart_lithium(self, data: SmartLithiumData) -> None:
        self.update_sensor(
            Keys.BATTERY_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_battery_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.BATTERY_TEMPERATURE,
            Units.TEMP_CELSIUS,  # type: ignore [arg-type]
            data.get_battery_temperature(),
            SensorDeviceClass.TEMPERATURE,  # type: ignore [arg-type]
        )
        balancer_status = data.get_balancer_status()
        self.update_sensor(
            Keys.BALANCER_STATUS,
            None,
            balancer_status.name if balancer_status else None,
        )
        for i in range(7):
            self.update_sensor(
                getattr(Keys, f"CELL_{i+1}_VOLTAGE"),
                Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
                data.get_cell_voltages()[i],
                SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
            )

    def _update_solar_charger(self, data: SolarChargerData) -> None:
        charge_state = data.get_charge_state()
        self.update_sensor(
            Keys.CHARGE_STATE,
            None,
            charge_state.name if charge_state else None,
        )
        self.update_sensor(
            Keys.BATTERY_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_battery_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.BATTERY_CURRENT,
            Units.ELECTRIC_CURRENT_AMPERE,  # type: ignore [arg-type]
            data.get_battery_charging_current(),
            SensorDeviceClass.CURRENT,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.YIELD_TODAY,
            Units.ENERGY_WATT_HOUR,  # type: ignore [arg-type]
            data.get_yield_today(),
            SensorDeviceClass.ENERGY,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.SOLAR_POWER,
            Units.POWER_WATT,  # type: ignore [arg-type]
            data.get_solar_power(),
            SensorDeviceClass.POWER,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.EXTERNAL_DEVICE_LOAD,
            Units.ELECTRIC_CURRENT_AMPERE,  # type: ignore [arg-type]
            data.get_external_device_load(),
            SensorDeviceClass.CURRENT,  # type: ignore [arg-type]
        )

    def _update_vebus(self, data: VEBusData) -> None:
        device_state = data.get_device_state()
        self.update_sensor(
            Keys.DEVICE_STATE,
            None,
            device_state.name if device_state else None,
        )
        ac_in_state = data.get_ac_in_state()
        self.update_sensor(
            Keys.AC_IN_STATE,
            None,
            ac_in_state.name if ac_in_state else None,
        )
        self.update_sensor(
            Keys.AC_IN_POWER,
            Units.POWER_WATT,  # type: ignore [arg-type]
            data.get_ac_in_power(),
            SensorDeviceClass.POWER,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.AC_OUT_POWER,
            Units.POWER_WATT,  # type: ignore [arg-type]
            data.get_ac_out_power(),
            SensorDeviceClass.POWER,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.BATTERY_CURRENT,
            Units.ELECTRIC_CURRENT_AMPERE,  # type: ignore [arg-type]
            data.get_battery_current(),
            SensorDeviceClass.CURRENT,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.BATTERY_VOLTAGE,
            Units.ELECTRIC_POTENTIAL_VOLT,  # type: ignore [arg-type]
            data.get_battery_voltage(),
            SensorDeviceClass.VOLTAGE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.BATTERY_TEMPERATURE,
            Units.TEMP_CELSIUS,  # type: ignore [arg-type]
            data.get_battery_temperature(),
            SensorDeviceClass.TEMPERATURE,  # type: ignore [arg-type]
        )
        self.update_sensor(
            Keys.STATE_OF_CHARGE,
            Units.PERCENTAGE,  # type: ignore [arg-type]
            data.get_soc(),
            SensorDeviceClass.BATTERY,  # type: ignore [arg-type]
        )
