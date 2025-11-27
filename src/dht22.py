from typing import ClassVar, Mapping, Any, Optional
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.sensor import Sensor
from viam.logging import getLogger
import asyncio # <-- ADDED: Required for non-blocking I/O

import time
import RPi.GPIO as GPIO

LOGGER = getLogger(__name__)


class DHTResult:
    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2
    ERR_NOT_FOUND = 3

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity

    def is_valid(self):
        return self.error_code == DHTResult.ERR_NO_ERROR


class DHT:
    def __init__(self, pin, isDht11=True):
        self.__pin = pin
        self.__isDht11 = isDht11
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin, GPIO.OUT)

    def read(self):
        GPIO.setup(self.__pin, GPIO.OUT)
        self.__send_and_sleep(GPIO.HIGH, 0.05)
        self.__send_and_sleep(GPIO.LOW, 0.02)
        GPIO.setup(self.__pin, GPIO.IN, GPIO.PUD_UP)

        data = self.__collect_input()
        pull_up_lengths = self.__parse_data_pull_up_lengths(data)

        if len(pull_up_lengths) == 0:
            return DHTResult(DHTResult.ERR_NOT_FOUND, 0, 0)

        if len(pull_up_lengths) != 40:
            return DHTResult(DHTResult.ERR_MISSING_DATA, 0, 0)

        bits = self.__calculate_bits(pull_up_lengths)
        the_bytes = self.__bits_to_bytes(bits)
        checksum = self.__calculate_checksum(the_bytes)

        if the_bytes[4] != checksum:
            return DHTResult(DHTResult.ERR_CRC, 0, 0)

        temperature, humidity = self.__process_data(the_bytes)
        return DHTResult(DHTResult.ERR_NO_ERROR, temperature, humidity)

    def __send_and_sleep(self, output, sleep):
        GPIO.output(self.__pin, output)
        time.sleep(sleep)

    def __collect_input(self):
        data = []
        unchanged_count = 0
        last = -1
        max_unchanged_count = 100

        while True:
            current = GPIO.input(self.__pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break
        return data

    def __parse_data_pull_up_lengths(self, data):
        state = 1
        lengths = []
        current_length = 0

        for current in data:
            current_length += 1
            if state == 1:
                if current == GPIO.LOW:
                    state = 2
            elif state == 2:
                if current == GPIO.HIGH:
                    state = 3
            elif state == 3:
                if current == GPIO.LOW:
                    state = 4
            elif state == 4:
                if current == GPIO.HIGH:
                    state = 5
                    current_length = 0
            elif state == 5:
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = 4
        return lengths

    def __calculate_bits(self, pull_up_lengths):
        shortest_pull_up = 1000
        longest_pull_up = 0

        for length in pull_up_lengths:
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length

        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2
        bits = []
        for length in pull_up_lengths:
            bits.append(length > halfway)
        return bits

    def __bits_to_bytes(self, bits):
        byte = 0
        the_bytes = []

        for i, bit in enumerate(bits):
            byte = byte << 1
            if bit:
                byte = byte | 1
            if (i + 1) % 8 == 0:
                the_bytes.append(byte)
                byte = 0
        return the_bytes

    def __calculate_checksum(self, the_bytes):
        return sum(the_bytes[:4]) & 255

    def __process_data(self, the_bytes):
        if self.__isDht11:
            temperature = the_bytes[2] + float(the_bytes[3]) / 10
            humidity = the_bytes[0] + float(the_bytes[1]) / 10
        else:  # DHT22
            temperature = (the_bytes[2] * 256 + the_bytes[3]) / 10
            humidity = (the_bytes[0] * 256 + the_bytes[1]) / 10
        return temperature, humidity

    def cleanup(self):
        GPIO.cleanup()


class dht22(Sensor, Reconfigurable):
    """
    DHT22 Temperature and Humidity Sensor for Raspberry Pi
    """
    MODEL: ClassVar[Model] = Model(ModelFamily("wootter", "dht22-sensor"), "linux")

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
        self.sensor = DHT(self.pin, isDht11=False)
        LOGGER.info(f"DHT22 reconfigured with GPIO pin: {self.pin}")

    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, Any]:
        """
        Read temperature and humidity from DHT22 sensor.

        Returns:
            Mapping[str, Any]: Temperature and humidity readings.
        """
        # Retry logic: DHT22 sensors often need multiple attempts
        max_retries = 3
        retry_delay = 2.0  # seconds between retries
        
        for attempt in range(max_retries):
            # FIX: Use asyncio.to_thread to prevent blocking the event loop
            result = await asyncio.to_thread(self.sensor.read)

            if result.is_valid():
                temperature = result.temperature
                humidity = result.humidity
                
                LOGGER.info(f"Temperature: {temperature}°C, Humidity: {humidity}% (attempt {attempt + 1})")
                
                return {
                    "temperature_celsius": round(temperature, 2),
                    "humidity_percent": round(humidity, 2),
                    "temperature_fahrenheit": round(temperature * 9/5 + 32, 2)
                }
            else:
                error_messages = {
                    DHTResult.ERR_MISSING_DATA: "Missing data from DHT22 sensor",
                    DHTResult.ERR_CRC: "CRC checksum error from DHT22 sensor",
                    DHTResult.ERR_NOT_FOUND: "DHT22 sensor not responding"
                }
                error_msg = error_messages.get(result.error_code, "Unknown error")
                
                if attempt < max_retries - 1:
                    LOGGER.warning(f"DHT22 error on attempt {attempt + 1}/{max_retries}: {error_msg}. Retrying...")
                    await asyncio.sleep(retry_delay)
                else:
                    LOGGER.error(f"DHT22 error after {max_retries} attempts: {error_msg}")
                    return {
                        "error": error_msg,
                        "error_code": result.error_code
                    }

    async def close(self): # <-- ADDED: Component lifecycle method
        """
        Clean up GPIO resources when the module is shut down.
        """
        if self.sensor:
            # FIX: Use asyncio.to_thread to make synchronous cleanup non-blocking
            await asyncio.to_thread(self.sensor.cleanup)