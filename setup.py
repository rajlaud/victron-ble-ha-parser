import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="victron_ble_ha_parser",
    version="0.3.0",
    license="apache-2.0",
    author="Raj Laud",
    author_email="raj.laud@gmail.com",
    description="A parser for Victron BLE messages suitable for use with Home Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rajlaud/victron-ble-ha-parser",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "bluetooth-sensor-state-data>=1.6.1",
        "sensor-state-data>=2.16.0",
        "victron-ble>=0.6.0",
    ],
)
