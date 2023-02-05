#  _    _     _      _____                                          _               
# | |  | |   | |    / ____|                                        | |              
# | |  | |___| |__ | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| |  _ __  _   _ 
# | |  | / __| '_ \| |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` | | '_ \| | | |
# | |__| \__ \ |_) | |___| (_) | | | | | | | | | | | (_| | | | | (_| |_| |_) | |_| |
# \____/|___/_.__/ \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_(_) .__/ \__, |
#                                                                     | |     __/ |
#                                                                     |_|    |___/ 
# Use the REPL inmterafce instead of thr RS485 to send Allmotion Style commands
#
import machine
from machine import Pin, UART
from time import sleep_ms
from CommandQueue import CommandSequence

# Command reply status
UNKNOWN     = -1 # Unknown status
NO_ERROR    =  0 # No error
INIT_ERROR  =  1 # Initialization error
BAD_COMMAND =  2 # Bad Command
OP_OO_RANGE =  3 # Operand out of range

# Get a Command Sequence object
myQueue = CommandSequence()

while True:
    
    CmdStatus = UNKNOWN 

    # get keyboard input
    keyboardInput = input("Enter Command: ")
    if keyboardInput == "exit":
        exit()
    else:
        CmdStr = bytes(keyboardInput, "utf-8")
        
    if CmdStr != None:
        # Decode byte string to character string
        CmdStr=CmdStr.decode('utf-8', 'replace')
        
        # Command or query for me?
        if myQueue.CommandOrQueryForMe(CmdStr) :
            
            # Valid Command?
            if myQueue.ValidCommand(CmdStr):
                # Add to command queue
                myQueue.AddToQueue(CmdStr)
                CmdStatus = NO_ERROR
                
            # Valid Query?    
            elif myQueue.ValidQuery(CmdStr):
                # Get the reply value
                CmdStatus = myQueue.GetQueueReply(CmdStr)
                
            else:
                CmdStatus = BAD_COMMAND
                
            # Print the queue
            myQueue.Print()
           
        # Did we get a (R)un command?
        if myQueue.RunCommand(CmdStr):
            # Execute the queue of commands
            myQueue.ExecCommandQueue()
            
        print("Status: ", CmdStatus)

