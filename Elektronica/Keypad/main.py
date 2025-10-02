# Elektronica - Keypad
from machine import Pin, ADC
from utime import sleep_ms

# Define the ADC GPIO pin for the 5-button keypad
KEYPAD_PIN = 26  # Adjust this pin number as needed

# Initialize the ADC
adc = ADC(Pin(KEYPAD_PIN))


def read_keypad():
    # Read the ADC value
    adc_value = adc.read_u16()  # Read the ADC value (0-65535)
    print(adc_value)

    # Map the ADC value to a key
    if adc_value < 1000:
        return "Key 1"
    # elif ...:
    #
    # (!) voeg hier de code voor de andere buttons toe
    #
    else:
        return "No key"


def main():
    print("Starting keypad reader...")

    while True:
        key = read_keypad()
        print(f"{key} pressed")
        sleep_ms(500)  # Wait half a second before reading again


if __name__ == "__main__":
    main()
