# Victron BLE HA Parser

## Overview

This project exists solely to provide an interface to the excellent
[victron-ble](https://github.com/keshavdv/victron-ble) project suitable for use with a Home
Assistant integration. Thank you to Keshav Varma for maintaining the `victron-ble` project.

## Installing the Home Assistant custom component

Currently the Home Assistant integration is only available as a custom component, for testing
purposes.
The goal is to make this part of Home Assistant core.

If you'd like to test this, clone my fork on the HA project and checkout the `victron-ble-custom-component` branch:

`git clone https://github.com/rajlaud/home-assistant.git --branch victron-ble-custom-component`

Then, copy or symlink `homeassistant/components/victron-ble` into your `config/custom_components` folder.

## Details

The parser module has one class, `VictronBluetoothDeviceData`, which parses Bleak advertisements and
updates itself with the sensor data from the advertisement. Each instance of
`VictronBluetoothDeviceData` should be fed advertisements from exactly one Victron device (based on
the MAC address) and the instance needs to be initiated with the encryption key of the device that
is going to be sending updates. If the encryption key is set correctly everything else will be
figured out automatically.

There is a handy package from maintainers of the HA project called `sensor-state-data` to make it
easy to automate ingesting sensor state updates like this. Unfortunately, we need to use a unit
(amp-hours) not supported by the module and my PR to include amp-hours was rejected because they are
not a common unit (https://github.com/Bluetooth-Devices/sensor-state-data/pull/47). For that
reason, we need a custom extension of sensor-state-data, which is contained in the
custom-sensor-state.py file.
