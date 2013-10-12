#!/usr/bin/python3

# Simple PWM implementation for controlling speed of motor in one direction.
# Attach motor to ground and to a digital (open-collector) output on PiFace.

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

while True:
	for x in list(range(0, 10)) + list(range(10, 0, -1)):
		d = x / 10
		t = d / 100
		f = (1 - d) / 100
		for i in range(0, 10):
			if t > 0:
				pfd.output_pins[2].turn_on()
				sleep(t)
			if f > 0:
				pfd.output_pins[2].turn_off()
				sleep(f)
