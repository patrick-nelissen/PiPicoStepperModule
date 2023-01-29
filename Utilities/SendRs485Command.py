import time
import serial


rxStatus = {
    "-1" : "Unknow Status",
     "0" : "No Error",
     "1" : "Initialization Error",
     "2" : "Bad Command",
     "3" : "Operand Outof Range"
}


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial("COM16", 57600, timeout=0, bytesize=8, parity="N", stopbits=1)

ser.isOpen()

print( 'Enter your serial commands below.\r\nInsert "exit" to leave the application.')

keyboardInput = 1
while 1 :
    # get keyboard input
    keyboardInput = input("Enter Command: ")
        # Python 3 users
        # input = input(">> ")
    if keyboardInput == "exit":
        ser.close()
        exit()
    else:
        string = bytes(keyboardInput, "utf-8")
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        ser.write(string)
        out = ""
        outString = ""
        # let's wait 0.1 second before reading output (let's give device time to answer)
        time.sleep(0.1)
        while ser.inWaiting() > 0:
            out = ser.read(1)
            outString += out.decode()
            
        if outString != "":
            #print( "Serial Reply: " + rxStatus[outString])
            print( "Serial Reply: " + outString)
