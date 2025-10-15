import time
import RPi.GPIO as GPIO

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
        GPIO.setup(self.__pin, GPIO.OUT)  # Set the pin as output initially

    def read(self):
        GPIO.setup(self.__pin, GPIO.OUT)  # Ensure the pin is set up as OUTPUT before sending HIGH/LOW signal.

        # Send start signal
        self.__send_and_sleep(GPIO.HIGH, 0.05)
        self.__send_and_sleep(GPIO.LOW, 0.02)
        GPIO.setup(self.__pin, GPIO.IN, GPIO.PUD_UP)  # Switch pin to input mode for reading

        # Collect data
        data = self.__collect_input()
        pull_up_lengths = self.__parse_data_pull_up_lengths(data)

        # If no data collected
        if len(pull_up_lengths) == 0:
            return DHTResult(DHTResult.ERR_NOT_FOUND, 0, 0)

        # If data length is incorrect
        if len(pull_up_lengths) != 40:
            return DHTResult(DHTResult.ERR_MISSING_DATA, 0, 0)

        # Process bits
        bits = self.__calculate_bits(pull_up_lengths)
        the_bytes = self.__bits_to_bytes(bits)
        checksum = self.__calculate_checksum(the_bytes)

        # Checksum mismatch
        if the_bytes[4] != checksum:
            return DHTResult(DHTResult.ERR_CRC, 0, 0)

        # Process temperature and humidity values
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
            if state == 1:  # INIT_PULL_DOWN
                if current == GPIO.LOW:
                    state = 2  # INIT_PULL_UP
            elif state == 2:  # INIT_PULL_UP
                if current == GPIO.HIGH:
                    state = 3  # DATA_FIRST_PULL_DOWN
            elif state == 3:  # DATA_FIRST_PULL_DOWN
                if current == GPIO.LOW:
                    state = 4  # DATA_PULL_UP
            elif state == 4:  # DATA_PULL_UP
                if current == GPIO.HIGH:
                    state = 5  # DATA_PULL_DOWN
                    current_length = 0
            elif state == 5:  # DATA_PULL_DOWN
                if current == GPIO.LOW:
                    lengths.append(current_length)
                    state = 4  # DATA_PULL_UP
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
