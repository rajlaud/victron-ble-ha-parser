"""Custom state data for victron-ble. See https://github.com/Bluetooth-Devices/sensor-state-data/pull/47."""

import sensor_state_data
import sensor_state_data.enum


class SensorDeviceClass(sensor_state_data.BaseDeviceClass):
    """Custom class to support victron-ble specific device classes."""

    # inherited fields

    BATTERY = sensor_state_data.DeviceClass.BATTERY
    CURRENT = sensor_state_data.DeviceClass.CURRENT
    DURATION = sensor_state_data.DeviceClass.DURATION
    ENERGY = sensor_state_data.DeviceClass.ENERGY
    POWER = sensor_state_data.DeviceClass.POWER
    SIGNAL_STRENGTH = sensor_state_data.DeviceClass.SIGNAL_STRENGTH
    TEMPERATURE = sensor_state_data.DeviceClass.TEMPERATURE
    VOLTAGE = sensor_state_data.DeviceClass.VOLTAGE

    # new fields

    CURRENT_FLOW = "current_flow"
    ENUM = "enum"


class Units(sensor_state_data.enum.StrEnum):
    """Custom class to support victron-ble specific units."""

    # inherited fields

    ELECTRIC_CURRENT_AMPERE = sensor_state_data.Units.ELECTRIC_CURRENT_AMPERE
    ELECTRIC_POTENTIAL_VOLT = sensor_state_data.Units.ELECTRIC_POTENTIAL_VOLT
    ENERGY_WATT_HOUR = sensor_state_data.Units.ENERGY_WATT_HOUR
    PERCENTAGE = sensor_state_data.Units.PERCENTAGE
    POWER_WATT = sensor_state_data.Units.POWER_WATT
    TEMP_CELSIUS = sensor_state_data.Units.TEMP_CELSIUS
    TIME_MINUTES = sensor_state_data.Units.TIME_MINUTES

    # new fields

    ELECTRIC_CURRENT_FLOW_AMPERE_HOUR = "Ah"


class Keys(sensor_state_data.enum.StrEnum):
    """Class of victron-ble keys."""

    AC_IN_POWER = "ac_in_power"
    AC_IN_STATE = "ac_in_state"
    AC_OUT_POWER = "ac_out_power"
    AC_OUT_STATE = "ac_out_state"
    ALARM = "alarm"
    AUX_MODE = "aux_mode"
    BALANCER_STATUS = "balancer_status"
    BATTERY_CURRENT = "battery_current"
    BATTERY_TEMPERATURE = "battery_temperature"
    BATTERY_VOLTAGE = "battery_voltage"
    CELL_1_VOLTAGE = "cell_1_voltage"
    CELL_2_VOLTAGE = "cell_2_voltage"
    CELL_3_VOLTAGE = "cell_3_voltage"
    CELL_4_VOLTAGE = "cell_4_voltage"
    CELL_5_VOLTAGE = "cell_5_voltage"
    CELL_6_VOLTAGE = "cell_6_voltage"
    CELL_7_VOLTAGE = "cell_7_voltage"
    CHARGE_STATE = "charge_state"
    CHARGER_ERROR = "charger_error"
    CONSUMED_AMPERE_HOURS = "consumed_ampere_hours"
    CURRENT = "current"
    DEVICE_STATE = "device_state"
    ERROR_CODE = "error_code"
    EXTERNAL_DEVICE_LOAD = "external_device_load"
    INPUT_VOLTAGE = "input_voltage"
    METER_TYPE = "meter_type"
    MIDPOINT_VOLTAGE = "midpoint_voltage"
    OFF_REASON = "off_reason"
    OUTPUT_STATE = "output_state"
    OUTPUT_VOLTAGE = "output_voltage"
    REMAINING_MINUTES = "remaining_minutes"
    SOLAR_POWER = "solar_power"
    STARTER_VOLTAGE = "starter_voltage"
    STATE_OF_CHARGE = "state_of_charge"
    TEMPERATURE = "temperature"
    VOLTAGE = "voltage"
    WARNING = "warning"
    YIELD_TODAY = "yield_today"
