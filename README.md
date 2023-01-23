# Pi Pico StepperModule
Stepper Motor motion controller with trapezoidal motion profile and RS485 interface.

## ABOUT

This microPython application runs on a Raspberry Pi Pico (RP2040), and is controlling a Stepper Motor Driver Module. The hardware is a TB6600 derivative from Toshiba, specifically the TB67S109AFTG.
The Module's encloser is re-engineered and modified to make room for:
1. The Pi Pico board with USB access
1. A serial RS-485 half-duplex converter and connectivity
2. DC/DC Converter to power the Pi Pico
3. Opto Coupler connectivity to home the controlled axis

## PARTS
1. TB6600, 4A Stepper Motor Driver 4A for Nema 17 23 and 34 Stepper Motor

   https://www.amazon.com/dp/B08PKJG2ND?ref=ppx_yo2ov_dt_b_product_details&th=1
2. SparkFun Transceiver Breakout - RS-485

   https://www.sparkfun.com/products/10124
3. 6-Pin 5.08mm Pitch Male Female PCB Screw Terminal Block

   https://www.amazon.com/dp/B093DMG1QZ?psc=1&ref=ppx_yo2ov_dt_b_product_details
4. IR Slotted Optical Optocoupler, 3.3V to 5V

   https://www.amazon.com/dp/B09W5KWFV6?psc=1&ref=ppx_yo2ov_dt_b_product_details
5. MP1584EN DC-DC, 3A Converter, 24V to 12V - 3V

   https://www.amazon.com/dp/B08247LRYS?psc=1&ref=ppx_yo2ov_dt_b_product_details


