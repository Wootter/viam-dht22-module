import asyncio
from typing import Any, ClassVar, Dict, Mapping, Optional
from viam.components.sensor import Sensor
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
import Adafruit_DHT
import RPi.GPIO as GPIO


class MySensor(Sensor):
    """
    DHT22 Temperature and Humidity Sensor for Raspberry Pi
    This sensor module reads temperature and humidity data from a DHT22 sensor
    connected to a Raspberry Pi GPIO pin.
    """
    
    # Define the model of the sensor
    MODEL: ClassVar[Model] = Model(ModelFamily("wootter", "dht22-sensor"), "linux")

    def __init__(self, name: str, pin: int):
        """
        Initialize the DHT22 sensor with the name and GPIO pin.
        
        Args:
            name: The name of the sensor component
            pin: The GPIO pin number where the DHT22 is connected
        """
        super().__init__(name)
        self.pin = pin
        # DHT22 is also known as AM2302
        self.sensor_type = Adafruit_DHT.DHT22

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> "MySensor":
        """
        Create a new instance of the sensor using the configuration.
        
        Args:
            config: Component configuration containing the GPIO pin
            dependencies: Component dependencies (not used for this sensor)
            
        Returns:
            A new MySensor instance
        """
        # Extract the pin number from the configuration attributes
        pin = config.attributes.fields["pin"].number_value
        if not pin:
            raise ValueError("GPIO pin number must be specified in configuration")
        
        sensor = cls(config.name, int(pin))
        return sensor

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:
        """
        Read the humidity and temperature from the DHT22 sensor.
        
        Args:
            extra: Optional extra parameters
            **kwargs: Additional keyword arguments
            
        Returns:
            A dictionary containing temperature (Celsius) and humidity (percentage),
            or an error message if reading fails
        """
        # Read from the DHT22 sensor
        # Adafruit_DHT.read_retry ensures multiple read attempts for reliability
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_type, self.pin)
        
        if humidity is not None and temperature is not None:
            return {
                "temperature_celsius": round(temperature, 2),
                "humidity_percent": round(humidity, 2),
                "temperature_fahrenheit": round(temperature * 9/5 + 32, 2)
            }
        else:
            return {
                "error": "Failed to read from DHT22 sensor",
                "pin": self.pin
            }


async def main():
    """
    Test function to verify sensor readings.
    This will be called when the module is run standalone.
    """
    # Create a new sensor object and get readings (using GPIO pin 4 as default)
    my_sensor = MySensor(name="dht22_sensor", pin=4)
    readings = await my_sensor.get_readings()
    print("DHT22 Sensor Readings:")
    print(readings)


# Run the main function when the script is executed directly
if __name__ == '__main__':
    asyncio.run(main())
