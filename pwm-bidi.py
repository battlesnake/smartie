#!/usr/bin/python3

# Variable-speed, bi-directional motor control interface, using MOSFET H-bridge
# to supply motor.  Attach gates of MOSFETs to 10k 5V-pullup resistors and to
# open-collector outputs #2, #3 on PiFace.

# Imports for PiFace, timing and user interface
from time import sleep
import pifacedigitalio as pfdio
import signal
import sys
import curses

# Ctrl+C handler, performs clean-up before terminating
def signal_handler(signal, frame):
	terminate()

# Register Ctrl+C handler
signal.signal(signal.SIGINT, signal_handler)

# Clean shutdown of the driver (clears PiFace ports)
def terminate():
	pfd.output_pins[2].turn_off()
	pfd.output_pins[3].turn_off()
	sys.exit(0)

# PiFace interface
pfdio.init()
pfd = pfdio.PiFaceDigital()

def main(scr):
	scr.nodelay(1)
	# Direction (0/1) and speed (0-10)
	dir = 0
	speed = 0
	# Pins on PiFace to use
	pulsepin = 2
	fixedpin = 3
	# Fraction of a second per timeslice (Linux can handle up to 1/1000,
	# Windows is limited to around 1/18 but the Pi doesn't run Windows so
	# no problem :D).  Anywhere from 10 to 1000 should be fine on the Pi.
	timeslice = 50
	# Number of slices to drive before checking for input (note that the
	# value of slicecount / timeslice defines the maximum time that this
	# driver will take to respond to a command so if slicecount / timeslice
	# equals 0.1 then this driver could take up to 0.1 seconds to respond
	# to a control change command.
	slicecount = 2
	# Max and min voltage on motor power supply.  Not used for now.
	vmax = 6
	vmin = 0
	# Max speed (invisibly used to scale user-supplied speed, if using e.g.
	# 3V motors on a 5V supply)
	maxspeed = 5
	# Annoying voltage drop over open-collector output (WHY couldn't they
	# use open-drain MOSFETs instead of BJTs...).  Not used for now.
	vdrop = 0.682
	# Main loop
	while True:
		# Driver state
		scr.addstr(2, 2, "Speed: {0}  ".format(speed))
		scr.addstr(4, 2, "Direction: {0}  "
			.format("left" if dir else "right"))
		# Ugly input handling (Python lacks switch/select/case)
		c = scr.getch()
		if c == curses.KEY_LEFT:
			dir = 1
		elif c == curses.KEY_RIGHT:
			dir = 0
		elif c == curses.KEY_UP:
			speed = (speed + 1) if speed < 10 else 10
		elif c == curses.KEY_DOWN:
			speed = (speed - 1) if speed > 0 else 0
		elif c == ord('q'):
			break
		# Calculate time to power motor for, per slice
		d = speed * maxspeed / 100
		t = d / timeslice
		f = (1 - d) / timeslice
		if dir:
			t,f = f,t
		if dir:
			pfd.output_pins[fixedpin].turn_on()
		else:
			pfd.output_pins[fixedpin].turn_off()
		# Show diagnostic data
		scr.addstr(6, 2, "Duty: {0:.2f},{1:.2f}/{2:.2f} ms"
			.format(t*1000, f*1000, (t+f)*1000))
		# Run some timeslices
		for i in range(0, slicecount):
			# Port enabled (open-collector "switch" closed)
			if t > 0:
				pfd.output_pins[pulsepin].turn_on()
				sleep(t)
			# Port disabled (open-collector "switch" opened)
			if f > 0:
				pfd.output_pins[pulsepin].turn_off()
				sleep(f)

# Start the interface
curses.wrapper(main)

# Clean exit
terminate()
