from bluepy import btle
import traceback

import db_operations as db


SETUP_DATA = b"\x01\00" #bytes sent to pulse oximeter handle to turn on notifications


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, name):
        btle.DefaultDelegate.__init__(self)
        self.counter = 0 ## counter to slow down output. 
        self.name = name
    
    def handleNotification(self, cHandle, data):
        if self.counter == 25:
            
            db.update_heart_rate(self.name, (str(data[3])))
            
            # Printing heart rates to console to make sure backend is working
            # 3rd index in data object is the heart rate.
            print(f"{self.name}: {data[3]}     ", end='\r')
            print(end="\x1b[2K")
            self.counter = 0
        else:
            self.counter += 1
# Main function all wrapped in try/except
# This is to handle sensors bein connected or waiting for connection
# Stack trace still prints for debugging/monitoring
def main():
    try:
        db.show_connecting()
        
        # Initialisation for pulse oximeter 1 -------

        pulse1 = btle.Peripheral("00:A0:50:60:7C:4F") #### Pulse oximeter #1
        pulse1.setDelegate( MyDelegate('pulse1') )


        # Setup to turn pulse1 notifications on
        svc1 = pulse1.getServiceByUUID("49535343-fe7d-4ae5-8fa9-9fafd205e455")
        ch1 = svc1.getCharacteristics("49535343-1e4d-4bd9-ba61-23c647249616")[0]
        pulse1.writeCharacteristic(ch1.valHandle+1, SETUP_DATA, withResponse=True)


        # Initialisation for pulse oximeter 2 -------

        pulse2 = btle.Peripheral("00:A0:50:C8:CB:3A") #### Pulse oximeter #2
        pulse2.setDelegate( MyDelegate('pulse2') )


        # Setup to turn pulse2 notifications on 
        svc2 = pulse2.getServiceByUUID("49535343-fe7d-4ae5-8fa9-9fafd205e455")
        ch2 = svc2.getCharacteristics("49535343-1e4d-4bd9-ba61-23c647249616")[0]
        setup_data = b"\x01\00"
        pulse2.writeCharacteristic(ch1.valHandle+1, SETUP_DATA, withResponse=True)


        # Main loop --------

        while True:
            if pulse1.waitForNotifications(2.0) and pulse2.waitForNotifications(2.0):
                # handleNotification() was called for pulse1 and pulse2. Iterates counter and outputs when counter limit met
                continue
            
            
    except Exception as error:
        db.show_connecting()
        traceback.print_exc()
        print("Waiting for connection...")
        main()


if __name__ == '__main__':
    main()
    
    




