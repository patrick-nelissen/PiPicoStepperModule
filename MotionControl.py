import machine
from machine import Pin, UART
from time import sleep_ms
from CommandQueue import CommandSequence


# RS485 pin definitions
TX_PIN  = 0
RX_PIN  = 1
RST_PIN = 6  

# Define UART
uart0 =UART(0, baudrate=57600, bits=8, parity=None, stop=1, tx=Pin(TX_PIN), rx=Pin(RX_PIN))

# Define RST (Request To Transmitt)
RST  = Pin(RST_PIN, Pin.OUT)

# Flush serial buffer
def flushSerial(uart):
    while uart.any():
        uart.read(1)

# Set RST HIGH to transmit data
def  transmitData():
    RST.value(1)

# Set RST LOW to receive data
def receiveData():
    RST.value(0)      
 
# Start with listening
receiveData()

# Flush startup garbage from serial buffer
flushSerial(uart0)


myQueue = CommandSequence()

while True:
    
    commandReceived = False
    
    RxStr = uart0.read()
    if RxStr != None:
        RxStr.decode('utf-8')
        commandReceived = True
        
        # Command for me?
        if myQueue.CommandForMe(RxStr) :
            
            # Valid Command?
            if myQueue.ValidCommand(RxStr):
                # Add to cammand queue
                myQueue.AddToQueue(RxStr)
            # Print the queue
            myQueue.Print()
           
    
    # Acknowledge Command received
    if commandReceived :
                
        # Switch RS485 levelshifter to transmit mode
        transmitData()
               
        # Write the ack
        uart0.write("ACK")

        # Give the hardware some time to kick out this data
        sleep_ms(1)
        
        # Switch RS485 levelshifter back to receive mode
        receiveData()
        
        # Flush the uart in case the TX->RX caused some noise
        flushSerial(uart0)

        # Did we get a (R)un command?
        if myQueue.RunCommand(RxStr):
            # Execute the queue of commands
            myQueue.ExecCommandQueue()
