# Pi Pico StepperModule
Stepper Motor motion controller with trapezoidal motion profile and RS485 interface.

## ABOUT

This microPython application runs on a Raspberry Pi Pico (RP2040), and is controlling a Stepper Motor Driver Module. The hardware is a TB6600 derivative from Toshiba, specifically the TB67S109AFTG.

The Module's encloser is re-engineered and modified to make room for:
1. The Pi Pico board with USB access
2. DC/DC Converter to power the Pi Pico
3. A serial RS-485 half-duplex converter and connectivity
4. Opto Coupler connectivity to home the controlled axis
5. PCB Screw Terminal Block receiver for external connectivity of item 3. and 4.


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
	
