# Filesystem to write data to non-volatile flash
import machine

import json

# Filesystem to write data to non-volatile flash
import os
os.chdir("/")

ConfigData = {
    "CtrlNumber"         : 1,
    "StepSize"           : 0.137441,
    "DefaultMaxVelocity" : 1000,
    "DefaultAcceleration": 2000,
    }

with open('ConfigFile.txt', 'w') as config_file:
	config_file.write(json.dumps(ConfigData))

config_file.close()
