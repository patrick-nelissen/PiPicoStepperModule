# PiPicoStepperModule
Stepper Motor motion controller with RS485 interface

## About

This microPython application runs on a Raspberry Pi Pico (aka RP2040), and is controlling a Stepper Motor Driver Module bought on Amazon. This driver is build around a TB6600 derivative from Toshiba, specifically the XXXXXXX.
The Module's encloser is re-engineered and modified to make room for:
1. The Pi Pico board with USB access
1. A serial RS-485 half-duplex converter and connectivity
2. DC/DC Converter to power teh Pi Pico
3. Opto Coupler connectivity to home the controlled axis

