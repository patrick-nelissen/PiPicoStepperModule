# Filesystem to write data to non-volatile flash
import machine

import json

# Filesystem to write data to non-volatile flash
import os
os.chdir("/")

# reading the data from the file
with open("ConfigFile.txt") as config_file:
    ConfigData = config_file.read()

config_file.close()

print( "Data type before reconstruction : ", type(ConfigData) )

# reconstructing the data as a dictionary
js = json.loads( ConfigData )

print( "Data type after reconstruction : ", type(js) )
print( js )