# Filesystem to write data to non-volatile flash
import machine

import json

# Filesystem to write data to non-volatile flash
import os



class StepperConfiguration:

    os.chdir("/")

    CONFIGURATION_FILE = "ConfigurationData.txt"

    DefaultConfigurationData = {
        "CtrlNumber"         : 1,
        "StepSize"           : 0.137441,
        "DefaultMaxVelocity" : 1000,
        "DefaultAcceleration": 2000
    }

    Data = ""
    ConfigDate=[]

    def __init__(self):
               
        # During init, read the configuration data from flash for this Stepper Controller.
        # If no configuration data file present, create one with DefaultConfigurationData setting .
        
        # Try opening the file from flash
        try:
            
            # Open the file that has the configuration data
            config_file = open(self.CONFIGURATION_FILE)
            
            # Try reading the data
            try:
            
                self.Data = config_file.read()
            
            except:
                
                print("Cannot read date from: ", self.CONFIGURATION_FILE)
                
            else:
                
                config_file.close()
                
        except:
            
            # Unable to open the configuration file
            # Creat a default one...
            
            print("File " + self.CONFIGURATION_FILE + " not present.")
            print("Creating " + self.CONFIGURATION_FILE + " with following defaults:")
            print(self.DefaultConfigurationData)
                  
            with open(self.CONFIGURATION_FILE, "w") as config_file:
                config_file.write(json.dumps(self.DefaultConfigurationData))

            config_file.close()

        else:
            
            # reconstructing the data as a dictionary
            self.ConfigData = json.loads( self.Data )
            print( "Default configuration: ")
            print( self.ConfigData )
            
    def GetControllerNumber(self):
        
        return self.ConfigData['CtrlNumber']
