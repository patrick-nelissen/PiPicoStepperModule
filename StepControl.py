# RP2040
import machine
import gc
from machine import Pin

# Time
from utime import sleep, sleep_ms, sleep_us, ticks_us

# Math
from math import sqrt


class Stepper:
    
    # Stepper driver pin definitions
    Ena  = Pin(2, Pin.OUT)
    Dir  = Pin(3, Pin.OUT)
    Ste  = Pin(4, Pin.OUT)
    Home = Pin(5, Pin.IN)

    # Defaults
    ss = 0.137441         # Stepsize in mm
    vmax = 1000           # Maximum desired linear velocity in mm/s
    acc = 10000           # Acceleration in mm/(s*s)
    deltaS = 20*109.95574 # Distance to travel in mm
    hS = 100              # Maximum distance to travel in mm for finding home flag


    def _init_(self):
        self.EnableDriver()
        self.Homed = False
        self.StepDelays = []
    
    def EnableDriver(self):
        self.Ena.value(0)
        
    def DisableDriver(self):
        self.Ena.value(1) 

    def SetStepDirection( self, StepDirection = "CW" ):
        
        self.StepDirection = StepDirection
        
        if self.StepDirection == "CW":
            self.Dir.value(1)
        elif self.StepDirection == "CCW":
            self.Dir.value(0)
        else:
            print("Undefined step direction: ", StepDirection)

    def SetStepSize(self, ss):
    
        self.ss = ss
        print("Step size set to: ", self.ss, " mm")

    def SetAbsoluteMoveDistance(self, absS):
    
        self.absS = absS
        print("Absolute move distance set to: ", self.absS, " mm")

    def SetRelativeMoveDistance(self, deltaS):
    
        self.deltaS = deltaS
        print("Relative move distance set to: ", self.deltaS, " mm")

    def SetMaxVelocity(self, vmax):
    
        self.vmax = vmax
        print("Max. velocity set to: ", self.vmax, " mm/s")
        
    def SetAcceleration(self, acc):
    
        self.acc = acc
        print("Acceleration set to: ", self.acc, " mm/s2")
       
    def SetMaxHomeMoveDistance(self, hS):
    
        self.hS = hS
        print("Max home move distance set to: ", self.acc, " mm/s2")     

    def HomeAxis(self, hS):
        
        # Home distance is maximum distnace teh stepper will move to find home flag
        self.hS = hS
        
        # Are we in the home flag already?
        if self.Home.value() == 1:
            
            # Move out of the flag by 4.0 mm
            self.SetStepDirection( "CW" )       
            absSteps = round(abs(10.0) / self.ss) # Calc number of steps we need to do
            
            # Take 1 ms steps
            for incStep in range(absSteps):
                self.Ste.value(1)
                self.Ste.value(0)
                sleep_ms(1)
                
            # Still at the home position?
            if self.Home.value() == 1:
                print("Home failed - Unable to move out of home-flag!")
                    
        # Find the flag by moving CCW for no more than 100.0mm
        self.SetStepDirection( "CCW" )       
        absSteps = round(self.hS / self.ss) # Calc number of steps we need to do                

        # Take 1 ms steps
        for incStep in range(absSteps):
            self.Ste.value(1)
            self.Ste.value(0)
            sleep_ms(1)
                
            # Found home?
            if self.Home.value() == 1:
                print("Home found!")
                self.Homed = True
                break

        # Reached th eend of the home move?
        if incStep == absSteps - 1:
            print("Home Failed - Cannot find home!")
                
    def CalcMove(self):
        
        absSteps = round(abs(self.deltaS) / self.ss) # number of steps we need to do

        print("absSteps: ", absSteps)

        # define end point of acceleration and start point of deceleration
        s_1 = self.vmax * self.vmax / (2 * self.acc)
        s_2 = self.deltaS - s_1

        print("s_1: ", s_1)
        print("s_2: ", s_2)

        if s_1 > s_2: # if we dont even reach full speed
            s_1 = self.deltaS / 2
            s_2 = self.deltaS / 2;
            vmax = sqrt(self.deltaS * self.acc)

        print("s_1_m: ", s_1)
        print("s_2_m: ", s_2)
        print("vmax: ", vmax)

        vcurr = 0

        # Run garbage collector
        print("Mem Free before garbage collection: ", gc.mem_free())
        gc.collect()
        print("Mem Free after garbage collection: ", gc.mem_free())


        # Pre calculate the delays for the motion.
        # In that way the garbage collector will not kick in and create hick-ups within the pulsetrain to execute the move.

        for incStep in range(absSteps):
                   
            # calculate central position of current step
            s = (incStep + 0.5) * self.ss
            
            # calculate velocity at current step
            if s < s_1:
                vcurr = sqrt(2 * s * self.acc)
            elif s < s_2:
                vcurr = self.vmax
            else:
                vcurr = sqrt( self.vmax * self.vmax - 2 * (self.s - s_2) * self.acc)
               
            # convert velocity to delay
            tDelay = round(self.ss / vcurr * 1e6) # in micro seconds
            
            # Store the motion data in this list
            self.StepDelays.append(tDelay)

        # Let the garbage collector do its thing prior to the move
        print("Mem Free before garbage collection: ", gc.mem_free())
        gc.collect()
        print("Mem Free after garbage collection: ", gc.mem_free())

  
    def ExecMove(self):

        if self.Homed :

            self.SetStepDirection("CW")

            # Now step through the list of pre-calculated delsyas and genere the pulse train to execute the motion
            for StepDelay in self.StepDelays:
                    
                # act accordingly
                self.Ste.value(1)
                self.Ste.value(0)
                
                sleep_us(StepDelay)
        else:
            print("Axis has not been homed!")



