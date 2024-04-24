from basecar import *
import time

bc = BaseCar

bc.drive(50,1)
time.sleep(3)
bc.stop()
time.sleep(1)
bc.drive(50,-1)
time.sleep(3)
bc.stop
