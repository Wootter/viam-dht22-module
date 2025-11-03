# [dht22 modular service](https://app.viam.com/module/wootter/sensor/dht22)

This module implements the [rdk sensor API](https://github.com/rdk/sensor-api) in a `wootter:sensor:dht22` model.
With this model, you can read temperature and humidity from a DHT22 sensor.

## Requirements

The DHT22 sensor must be connected to a Raspberry Pi GPIO pin.

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the [`wootter:sensor:dht22` module](https://app.viam.com/module/wootter/sensor/dht22).

## Configure your sensor

> [!NOTE]  
> Before configuring your sensor, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

* Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com/).
* Click on the **Components** subtab and click the `sensor` subtab.
* Select the `wootter:sensor:dht22` model. 
* Enter a name for your sensor and click **Create**.
* On the new component panel, copy and paste the following attribute template into your sensor's **Attributes** box:

```json
{
  "pin": 4
}
```
* Save and wait for the component to finish setup

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `wootter:sensor:dht22` sensor:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `pin` | integer | **Required** | GPIO pin number where the DHT22 data pin is connected |

### Example Configuration

```json
{
  "pin": 4
}
```

## Hardware Setup

Connect your DHT22 sensor:
- **VCC** → 3.3V or 5V
- **GND** → Ground
- **DATA** → GPIO pin (e.g., GPIO 4)

## Readings

The sensor returns:

```json
{
  "temperature_celsius": 22.5,
  "humidity_percent": 45.2,
  "temperature_fahrenheit": 72.5
}
```
