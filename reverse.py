#!/usr/bin/python3

from time import sleep
import pifacedigitalio as pfdio
import signal
import sys

def signal_handler(signal, frame):
        pfd.output_pins[0].turn_off()
        pfd.output_pins[1].turn_off()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

pfdio.init()

pfd = pfdio.PiFaceDigital()

l = 0
r = 1

while True:
	l = r
	r = 1 - l
	pfd.output_pins[l].turn_on()
	pfd.output_pins[r].turn_off()
	sleep(0.05)
	pfd.output_pins[l].turn_off()
	sleep(0.2)
