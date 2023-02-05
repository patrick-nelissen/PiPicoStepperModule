#   _____ _              _____             __ _                       _   _                           
#  / ____| |            / ____|           / _(_)                     | | (_)                          
# | (___ | |_ ___ _ __ | |     ___  _ __ | |_ _  __ _ _   _ _ __ __ _| |_ _  ___  _ __    _ __  _   _ 
#  \___ \| __/ _ \ '_ \| |    / _ \| '_ \|  _| |/ _` | | | | '__/ _` | __| |/ _ \| '_ \  | '_ \| | | |
#  ____) | ||  __/ |_) | |___| (_) | | | | | | | (_| | |_| | | | (_| | |_| | (_) | | | |_| |_) | |_| |
# |_____/ \__\___| .__/ \_____\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__|_|\___/|_| |_(_) .__/ \__, |
#                | |                             __/ |                                   | |     __/ |
#                |_|                            |___/                                    |_|    |___/ 
#

import machine

import json

# Filesystem to write data to non-volatile flash
import os

class StepperConfiguration:

    os.chdir("/")

    CONFIGURATION_FILE = "ConfigurationData.txt"


    DefaultConfigurationData = {
        "CtrlNumber"   : 1,
        "StepSize"     : 0.137441,
        "MaxVelocity"  : 1000,
        "Acceleration" : 2000
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
            
            # Now that it is there, open the file that has the configuration data
            config_file = open(self.CONFIGURATION_FILE)
            self.Data = config_file.read()
            config_file.close()

        else:
            
            # reconstructing the data as a dictionary
            self.ConfigData = json.loads( self.Data )
            print( "Current configuration: ")
            print( self.ConfigData )
            
    def GetControllerNumber(self):
        
        return self.ConfigData["CtrlNumber"]
    
    def GetStepSize(self):
    
        return self.ConfigData["StepSize"]
    
    def GetAcceleration(self):
     
        return self.ConfigData["Acceleration"]
     
    def GetMaxVelocity(self):
     
        return self.ConfigData["MaxVelocity"]