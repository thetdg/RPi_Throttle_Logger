# RPi_Throttle_Logger
## A well formatted vcgencmd get_throttled report generator

Run on a RaspberryPi only
Author: Tanmoy Dasgupta
Refer to: https://www.raspberrypi.com/documentation/computers/os.html#get_throttled

Run this program in the background through any suitable utility such as GNU Screen. 
It will create a logfile named `throttle_data.txt` in the directory from which you ran 
the program. It will periodically fetch the status of `vcgencmd get_throttled` 
and log the status if something has changed. Note that, if nothing has changed 
between two successive checks, then no log entry will be made.
