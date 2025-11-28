from typing import ClassVar, Mapping, Any, Optional
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.sensor import Sensor
from viam.logging import getLogger
import asyncio

import time
import board
import adafruit_dht

LOGGER = getLogger(__name__)

class DHT:
    def __init__(self, pin):
        # Map GPIO pin numbers to board pins
        pin_map = {
            17: board.D17,
            4: board.D4,
            18: board.D18,
            22: board.D22,
            27: board.D27
        }
        
        if pin not in pin_map:
            raise ValueError(f"GPIO pin {pin} not supported. Use pins: {list(pin_map.keys())}")
            
        self.dht_sensor = adafruit_dht.DHT22(pin_map[pin])
        self.pin = pin
        
    def read(self):
        try:
            temperature = self.dht_sensor.temperature
            humidity = self.dht_sensor.humidity
            
            if temperature is not None and humidity is not None:
                return {"temperature": temperature, "humidity": humidity, "error": None}
            else:
                return {"temperature": None, "humidity": None, "error": "No data received"}
        except RuntimeError as e:
            return {"temperature": None, "humidity": None, "error": f"RuntimeError: {str(e)}"}
        except Exception as e:
            return {"temperature": None, "humidity": None, "error": f"Unexpected error: {str(e)}"}
    
    def cleanup(self):
        if hasattr(self.dht_sensor, 'exit'):
            self.dht_sensor.exit()


class dht22(Sensor, Reconfigurable):
    """
    DHT22 Temperature and Humidity Sensor for Raspberry Pi using Adafruit library
    """
    MODEL: ClassVar[Model] = Model(ModelFamily("wootter", "sensor"), "dht22")

    def __init__(self, name: str):
        super().__init__(name)
        self.pin = None
        self.sensor = None
        LOGGER.info(f"{self.__class__.__name__} initialized.")

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        instance = cls(config.name)
        instance.reconfigure(config, dependencies)
        return instance

    @classmethod
    def validate(cls, config: ComponentConfig):
        if "pin" not in config.attributes.fields:
            raise Exception("'pin' must be defined in the configuration.")
        return ([], [])

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.pin = int(config.attributes.fields["pin"].number_value)
        self.sensor = DHT(self.pin)
        LOGGER.info(f"DHT22 reconfigured with GPIO pin: {self.pin}")

    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, Any]:
        """
        Read temperature and humidity from DHT22 sensor using Adafruit library.

        Returns:
            Mapping[str, Any]: Temperature and humidity readings.
        """
        # Retry logic: DHT22 sensors often need multiple attempts
        max_retries = 5
        retry_delay = 2.0
        
        for attempt in range(max_retries):
            try:
                # Use asyncio.to_thread to prevent blocking the event loop
                result = await asyncio.to_thread(self.sensor.read)

                if result["error"] is None:
                    temperature = result["temperature"]
                    humidity = result["humidity"]
                    
                    LOGGER.info(f"Temperature: {temperature}°C, Humidity: {humidity}% (attempt {attempt + 1})")
                    
                    return {
                        "temperature_celsius": round(temperature, 2),
                        "humidity_percent": round(humidity, 2),
                        "temperature_fahrenheit": round(temperature * 9/5 + 32, 2)
                    }
                else:
                    error_msg = result["error"]
                    
                    if attempt < max_retries - 1:
                        LOGGER.warning(f"DHT22 error on attempt {attempt + 1}/{max_retries}: {error_msg}. Retrying...")
                        await asyncio.sleep(retry_delay)
                    else:
                        LOGGER.error(f"DHT22 error after {max_retries} attempts: {error_msg}")
                        return {
                            "error": error_msg,
                            "temperature_celsius": None,
                            "humidity_percent": None
                        }
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                if attempt < max_retries - 1:
                    LOGGER.warning(f"DHT22 exception on attempt {attempt + 1}/{max_retries}: {error_msg}. Retrying...")
                    await asyncio.sleep(retry_delay)
                else:
                    LOGGER.error(f"DHT22 exception after {max_retries} attempts: {error_msg}")
                    return {
                        "error": error_msg,
                        "temperature_celsius": None,
                        "humidity_percent": None
                    }

    async def close(self):
        """
        Clean up resources when the module is shut down.
        """
        if self.sensor:
            await asyncio.to_thread(self.sensor.cleanup)