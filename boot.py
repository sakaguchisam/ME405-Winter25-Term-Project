import pyb
from pyb import UART
from time import sleep_ms

# Initialize UART (Make sure this matches your Bluetooth module's default settings)
ser = UART(5, 38400, timeout=1000)
pyb.repl_uart(ser)


