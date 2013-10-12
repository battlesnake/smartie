#!/usr/bin/python3

from time import sleep
import pifacedigitalio as pfdio
import signal
import sys

def signal_handler(signal, frame):
        pfd.output_pins[2].turn_off()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

pfdio.init()

pfd = pfdio.PiFaceDigital()

b = 0

while True:
	b = 1 - b
	if b:
		pfd.output_pins[2].turn_on()
	else:
		pfd.output_pins[2].turn_off()
	sleep(2.5)
