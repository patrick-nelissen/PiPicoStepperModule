# Pi Pico Stepper Module
Stepper Motor motion controller with trapezoidal motion profile and RS485 interface.

## ABOUT

This microPython application runs on a Raspberry Pi Pico (RP2040) and is controlling a Stepper Motor Driver Module. The hardware is a TB6600 derivative from Toshiba, specifically the TB67S109AFTG.

The Module's enclosure is re-engineered and modified to make room for:
1. The Pi Pico board with USB access
2. DC/DC Converter to power the Pi Pico
3. A serial RS-485 half-duplex converter and connectivity
4. Opto Coupler connectivity to home the controlled axis
5. PCB Screw Terminal Block receiver for external connectivity of item 3. and 4.

## SOFTWARE

### MotionControl.py
This module is the top-level module that communicates with the master on the RS485 serial interface. It monitors the RS485 bus for commands and queries and acts on those that are intended for its hardware module.

### lib/CommandQueue.py
This module manages the mimicking of the AllMotion protocol as specified in Command_Set.pdf in the \Hardware\Datasheets folder.

### lib/StepConfiguration/py
This module manages configuration parameters specific to this hardware.
These include, but are not limited to module number (RS485 is a multi-drop communication bus), but also defaults used by StepControl.py
 
### lib/StepControl.py
This module manages the control of the low-level stepper hardware's ENABLE, DIRECTION, and STEP signals.
It takes speed, acceleration, move distance, step size etc as input, and then calculates a pulse delay table to create and execute a trapezoidal motion profile.

### Utilities

#### Utilities/SendRs485Command.py
Run RS485 interface on Host.

#### Utilities/UsbCommand.py
Use the REPL Host interface available on the USB of Pi Pico

## HARDWARE

The hardware files consist of:
1. Build Instructions
2. Wiring instruction for wiring the Pi Pico to:
	- TB6600, 4A Stepper Motor Driver 4A for Nema 17 23 and 34 Stepper Motor
      https://www.amazon.com/dp/B08PKJG2ND
	- SparkFun Transceiver Breakout - RS-485
      https://www.sparkfun.com/products/10124
	- 6-Pin 5.08mm Pitch Male Female PCB Screw Terminal Block
      https://www.amazon.com/dp/B093DMG1QZ
	- IR Slotted Optical Optocoupler, 3.3V to 5V
      https://www.amazon.com/dp/B09W5KWFV6
    - MP1584EN DC-DC, 3A Converter, 24V to 12V - 3V
      https://www.amazon.com/dp/B08247LRYS
3. Datasheets for:
	- TB67S109AFTG stepper controller
	- AllMotion Command Interface
4. CAD design files for the re-engineered enclosure in format:
	- SolidWorks .sldpt
	- .step files
	- .png file depicting the design
5. 3D print files in:
	- .3mf format (PrusaSlicer 2.5 export)
	- .stl file
	- .step file (see CAD)
	- .png depicting the "Paint On Supports" that are recommended
	
