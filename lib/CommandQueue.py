# COMMAND STRING EXAMPLE (allmotion)
#
# /1A12345R<CR>
# This breaks down to:
# 1. “/” is the start character. It lets the EZ Steppers know that a command is coming in.
# 2. “1” is the device address, (set on address switch on device).
# 3. “A12345” makes the motor turn to Absolute position 12345
# 4. “R” Tells the EZ Stepper to Run the command that it has received.
# <CR> is a carriage return that tells the EZ Stepper that the command string is complete and should be parsed.

# Regex module
import re

# Time module
from time import sleep, sleep_ms

# Filesystem to write data to non-volatile flash
import os
os.chdir("/")

from StepControl import Stepper
from StepConfiguration import StepperConfiguration

MY_ID               = "/1"
MY_ID_REGEX         = "^\/1.*$"
RUN_COMMAND_REGEX   = "^\/1.*R$"
VALID_COMMAND       = "([APDZvVTLse][0-9]*)|(R)"
VALID_COMMAND_REGEX = "^\/[0-9]" + VALID_COMMAND + "$"
PARSE_COMMAND_REGEX = "^([APDZvVLTRse])([0-9]*)$"

# Stepper driver command sequence
class CommandSequence:

    CommandQueue = []
    
    myStepper = Stepper()
    myConfig = StepperConfiguration()
    
    storeProgram = False
    
    def __init__(self):

        print("I am controller: ", self.myConfig.GetControllerNumber())
    
    def AddToQueue(self, string=""):
        
        # Remove first 2 characters "/" and number       
        string = string[2:]
        
        while True :
            # Find a first match of a valid command
            # NOTE: MicroPython doesn't support counted repetitions; hence * instead of {0-10}
            #       MicroPyhton doesn't support repeated group matches
            matches = re.search(VALID_COMMAND, string)

            # Get out of the while loop upon the first non-match
            if matches == None :
                break
            
            # Print for now. This is where we store the induvidual commends in a  list
            print("Command: ", matches.group(0))
            self.CommandQueue.append(matches.group(0))         
            
            if self.storeProgram:
                filename = "program1.txt"
                file = open(filename, "a")
                file.write(matches.group(0))
                file.close()
                
                # Last command a "R" command?
                if matches.group(0) == "R":
                    # Stop storing the program
                    self.storeProgram = False
                    
                    # Clear the command queue.
                    # We only want to store, not execute
                    self.CommandQueue.clear()
          
            # Remove the first match from the string and then look for a next match
            string = string[len(matches.group(0)): len(string)]
            
            if matches.group(0) == "s1":
                self.storeProgram = True
                print("Store program: ", self.storeProgram)
                
                # Open file again as empty file
                filename = "program1.txt"
                file = open(filename, "w")
                file.close() 
                 
    def Print(self):
        
        print(self.CommandQueue) 

    def CommandForMe(self, string = ""):
        
        self.Match = re.search(MY_ID_REGEX, string)

        if self.Match != None:
            
            print("Command: ", string, " is for me!")
            return True

        else:
            print("Not for me!", string)   
            return False
        
    def ValidCommand(self, string = ""):
        
        self.Match = re.search(VALID_COMMAND_REGEX, string)

        if self.Match != None:
            
            print("Valid command: ", string)
            return True

        else:
            print("Invalid command: ", string)
            return False        
        
    def RunCommand(self, string = ""):
        
        # Command string ends with a "R"
        self.Match = re.search(RUN_COMMAND_REGEX, string)

        if self.Match != None:           
            return True
        else:
            return False        

    def ExecCommandQueue(self):
        
        print("EXEC QUEUE", self.CommandQueue)
        for Command in self.CommandQueue:
            self.Match = re.search("^([APDZvVLTRse])([0-9]*)$", Command)

            if self.Match != None:
                
                # Get the Command and the Value argument
                Command = self.Match.group(1)
                Value = self.Match.group(2)
                
                print("Command: ", Command, " with value: ", Value)
                
                
                if Command == "A":
                    
                    # Get the current absolute position
                    relativeMoveDistance = int(Value)/10.0 - self.myStepper.GetAbsoluteMoveDistance()
                    
                    if relativeMoveDistance < 0:
                        # Negative (CCW) relative move
                        self.myStepper.SetStepDirection("CCW")                      
                    else:
                        # Positive (CW) relative move
                        self.myStepper.SetStepDirection("CW")                         
                        
                    # Distance (value) is in 0.1 mm resolution
                    self.myStepper.SetRelativeMoveDistance(abs(relativeMoveDistance))
                    
                    # Calculate and execute the move
                    self.myStepper.CalcMove()
                    self.myStepper.ExecMove()
                    
                elif Command == "P":

                    self.myStepper.EnableDriver()
                    
                    # Positive (CW) relative move
                    self.myStepper.SetStepDirection("CW")
                    
                    # Distance (value) is in 0.1 mm resolution
                    self.myStepper.SetRelativeMoveDistance(int(Value)/10.0)
                    
                    # Calculate and execute the move
                    self.myStepper.CalcMove()
                    self.myStepper.ExecMove()
                                        
                elif Command == "D":
 
                    self.myStepper.EnableDriver()

                    # Negative (CCW) relative move
                    self.myStepper.SetStepDirection("CCW")
                    
                    # Distance (value) is in 0.1 mm resolution
                    self.myStepper.SetRelativeMoveDistance(int(Value)/10.0)
                    
                    # Calculate and execute the move
                    self.myStepper.CalcMove()
                    self.myStepper.ExecMove()
                    
                elif Command == "Z":
                    
                    self.myStepper.EnableDriver()
                    
                    # Distance (Value) is in 1 mm resolution
                    self.myStepper.HomeAxis(int(Value))
                    
                elif Command == "v":
                    # Start velocity : not implemented
                    pass
                
                elif Command == "V":

                    # Max Velocity (Value) is in 1 mm/s resolution
                    self.myStepper.SetMaxVelocity(int(Value))
                
                elif Command == "L":
                    
                    # Acceleration (value) is in 1 mm/s2 resolution
                    self.myStepper.SetAcceleration(int(Value))
                    
                elif Command == "M":
                    
                    # Value in Milisecond units
                    sleep(int(Value))
                    
                elif Command == "R":
                   
                    print("BEFORE CLEAR", self.CommandQueue)
                    # All commands have run, empty queue
                    self.CommandQueue.clear()
                    print("AFTER CLEAR", self.CommandQueue)
                
                elif Command == "s":
                    
                    # Stores a program 0-10
                    # Program 0 is executed upon startup (not implemented)
                    filename = "program{}.txt"
                    
                    #os.remove(filename.format(int(Value)))
                    file = open(filename.format(int(Value)), "w")
                    
                    # Remove the first command from the queue
                    # We do not want to store the 's#'
                    self.CommandQueue.pop(0)
                    
                    for cmd in self.CommandQueue:
                        file.write(cmd)
                    file.close()                    
                    
                    # Clear the queue that we entered this loop in 
                    self.CommandQueue.clear()
                                        
                elif Command == "e":
                    
                    # Open the appropriate file that has the program stored.
                    filename = "program{}.txt"
                    file = open(filename.format(int(Value)))
                    
                    # Read the stored command sequence an dclose the file
                    CommandStr = file.read()
                    file.close()
                    
                    print("Loading command string: ", CommandStr)
                    
                    # The AddQueue expects the controller's MY_ID
                    CommandStr = MY_ID + CommandStr
                    
                    # Clear the queue that we have
                    self.CommandQueue.clear()
                    
                    # Load the stored command sequence
                    self.AddToQueue(CommandStr)
                    
                    # Execute it
                    self.ExecCommandQueue()
                
                else:
                    
                    print("Unknown command: ", Command)
                
            else:
                print("Invalid Command: ", Command)  



