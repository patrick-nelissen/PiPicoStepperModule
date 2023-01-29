# RP2040
import machine
from machine import Pin

# Time
from utime import sleep, sleep_ms, sleep_us, ticks_us

# Math
from math import sqrt

# Garbage collection
# NOTE: We do a lot of square root calculations that create
#       a lot of garbage that requires on demand collection
#
import gc


class Stepper:
    
    # Stepper driver pin definitions
    Ena  = Pin(2, Pin.OUT)
    Dir  = Pin(3, Pin.OUT)
    Ste  = Pin(4, Pin.OUT)
    Home = Pin(5, Pin.IN)

    # Defaults
    ss     = 0.137 # Stepsize in mm
    vmax   = 1000  # Maximum desired linear velocity in mm/s
    acc    = 2000  # Acceleration in mm/s2
    deltaS = 100.0 # Distance to travel in mm
    hS     = 100   # Maximum distance to travel in mm when seeking home flag
    absPos = 0.0   # Absolute position in mm (negative when invalid)
    absCnt = 0     # Absolute stepcount in (micro)steps (negative when invalid)
    
    StepDelays = []
    Homed = False
        
    def _init_(self, ss=0.137, vmax=1000, acc=2000, deltaS=100.0, hS=100, absPo=-1.0, absCnt=-1 ):
        self.DisableDriver()
        self.Homed = False
        self.ss = ss         # Stepsize in mm
        self.vmax = vmax     # Maximum desired linear velocity in mm/s
        self.acc = acc       # Acceleration in mm/s2
        self.deltaS = deltaS # Distance to travel in mm
        self.hS = hS         # Maximum distance to travel in mm when seeking home flag
        self.absPos = absPos # Absolute position in mm (negative when invalid)
        self.absCnt = absCnt # Absolute stepcount in (micro)steps (negative when invalid)
    
    def EnableDriver(self):
        self.Ena.value(0)
        print("Driver enabled")
        
    def DisableDriver(self):
        self.Ena.value(1)
        print("Driver disabled")

    def SetStepDirection( self, StepDirection = "CW" ):
        
        self.StepDirection = StepDirection
        print("Step direction set to: ", self.StepDirection)
        
        if StepDirection == "CW":
            self.Dir.value(1)
        elif StepDirection == "CCW":
            self.Dir.value(0)

    def SetStepSize(self, ss):
    
        self.ss = ss
        print("Step size set to: ", self.ss, " mm")
        
    def GetStepSize(self):
        
        # Return step size in mm
        return self.ss 

    def SetAbsoluteMoveDistance(self, absS):
    
        self.absS = absS
        print("Absolute move distance set to: ", self.absS, " mm")

    def GetAbsoluteMoveDistance(self):
    
        # Return absolute motor position in mm
        return self.absPos

    def SetRelativeMoveDistance(self, deltaS):
    
        self.deltaS = deltaS
        print("Relative move distance set to: ", self.deltaS, " mm")

    def SetMaxVelocity(self, vmax):
    
        self.vmax = vmax
        print("Max. velocity set to: ", self.vmax, " mm/s")
        
    def GetMaxVelocity(self):
            
        # Return maximum velocity mm/s
        return self.vmax
        
    def SetAcceleration(self, acc):
    
        self.acc = acc
        print("Acceleration set to: ", self.acc, " mm/s2")
    
    def GetAcceleration(self):
    
        return self.acc        
           
    def HomeAxis(self, hS):
        
        # Home distance is maximum distance the stepper will move to find home flag
        self.hS = hS
        
        print("Home Flag: ", self.Home.value())
        
        # Are we in the home flag already?
        if self.Home.value() == 1:
            
            # Move out of the flag by 4.0 mm
            self.SetStepDirection( "CW" )       
            absSteps = round(10.0 / self.ss) # Calc number of steps we need to do
            
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
                self.absPos = 0.0
                self.absCnt = 0
                break

        # Reached th eend of the home move?
        if incStep == absSteps - 1:
            print("Home Failed - Cannot find home!")
                
    def CalcMove(self):
        
        # Clear previous calculated motion delays
        self.StepDelays.clear()
        
        # Set the target vmax for this move.
        # Dependiong on the acceleration profile the target vmax might get adjusted
        vmax_target = self.vmax
        
        absSteps = round(abs(self.deltaS) / self.ss) # number of steps we need to do

        print("absSteps: ", absSteps)

        # define end point of acceleration and start point of deceleration
        s_1 = vmax_target * vmax_target / (2 * self.acc)
        s_2 = self.deltaS - s_1

        print("s_1: ", s_1)
        print("s_2: ", s_2)

        if s_1 > s_2: # if we dont even reach full speed
            s_1 = self.deltaS / 2
            s_2 = self.deltaS / 2;
            vmax_target = sqrt(self.deltaS * self.acc)

        print("s_1_m: ", s_1)
        print("s_2_m: ", s_2)
        print("vmax target: ", vmax_target)

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
                vcurr = sqrt( self.vmax * self.vmax - 2 * (s - s_2) * self.acc)
               
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

            if self.StepDirection == "CW":
                self.Dir.value(1)
            elif self.StepDirection == "CCW":
                self.Dir.value(0)
            else:
                print("Undefined step direction: ", StepDirection)
                
                # Default to CW
                self.Dir.value(1)
            
            # Now step through the list of pre-calculated delsyas and genere the pulse train to execute the motion
            for StepDelay in self.StepDelays:
                    
                # act accordingly
                self.Ste.value(1)
                self.Ste.value(0)
                
                sleep_us(StepDelay)
        else:
            print("Axis has not been homed!")

