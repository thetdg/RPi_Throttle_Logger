"""
A well formatted vcgencmd get_throttled report generator
Run on a RaspberryPi only
Author: Tanmoy Dasgupta
Refer to: https://www.raspberrypi.com/documentation/computers/os.html#get_throttled

Run this program in the background through any suitable utility such as GNU Screen. 
It will create a logfile named throttle_data.txt in the directory from which you ran 
the program. It will periodically fetch the status of `vcgencmd get_throttled` 
and log the status if something has changed. Note that, if nothing has changed 
between two successive checks, then no log entry will be made.
"""

import subprocess
import asyncio 
import datetime


status_list = [ 'Soft temperature limit has occurred since last reboot',
                'Throttling has occurred since last reboot',
                'Arm frequency capping has occurred since last reboot', 
                'Under-voltage has occurred since last reboot',
                'Soft temperature limit currently active', 
                'Currently throttled',
                'Arm frequency currently capped', 
                'Under-voltage currently detected' ]

old_output = ''

async def get_throttled_data():

    global status_list
    global old_output

    data = subprocess.run(['vcgencmd', 'get_throttled'], capture_output=True)
    throttled_data = str(data.stdout)
    
    while True:
        if throttled_data == "b'throttled=0x0\\n'":
            output = 'All okay! Nothing to report.\n\n'
            
        else:
            output = ''
            old_status = bin(int(throttled_data[14], 16))[2:]
            old_status = '0'*(4 - len(old_status)) + old_status
            cur_status = bin(int(throttled_data[18], 16))[2:]
            cur_status = '0'*(4 - len(cur_status)) + cur_status

            status = old_status + cur_status

            for count in range(8):
                if status[count] == '1':
                    output += status_list[count] + '\n'
            
        if output != old_output:
            with open('throttle_data.txt', 'a') as f:
                timestamp = str(datetime.datetime.now()).split('.')[0]
                f.write(timestamp + '\n' + output + '\n')
        
        old_output = output
            
        await asyncio.sleep(10)     


event_loop = asyncio.get_event_loop()
event_loop.create_task(get_throttled_data())
event_loop.run_forever()
