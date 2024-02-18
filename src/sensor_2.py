from bluepy import btle
import traceback

import db_operations as db



SETUP_DATA = b"\x01\00" #bytes sent to pulse oximeter handle to turn on notifications
DEFAULT_PULSE = '127'   # Default pulse sent by sensors when connecting. We need to remove this unless it's the actual pulse
CONNECTING = '143'      # This value is sent in the first byte of data whenever connecting. Except sometimes, hence the logic of 'last flag' below
                        # This looks for the last flag. Someties the first byte value drops one cycle before the pulse is read. Silly Chinese crap

class Sensor_2(btle.DefaultDelegate):
    def __init__(self, name):
        btle.DefaultDelegate.__init__(self)
        self.counter = 0 ## counter to slow down output. 
        self.name = name
        self.last_pulse = ''
        self.last_flag = ''
    
    def handleNotification(self, cHandle, data):
        if self.counter == 50:
            pulse_data = str(data[3])
            connecting_flag = str(data[0])
            if pulse_data == DEFAULT_PULSE and connecting_flag == CONNECTING:
                self.last_pulse = pulse_data
                self.last_flag = connecting_flag
                db.show_connecting(self.name)
            else:
                if pulse_data == DEFAULT_PULSE and self.last_flag == CONNECTING:
                    db.show_connecting(self.name)
                    self.last_pulse = pulse_data
                    self.last_flag = connecting_flag
                else:
                    db.update_heart_rate(self.name, pulse_data)
            
            # Printing heart rates to console to make sure backend is working
            # 3rd index in data object is the heart rate.
            print(f"{self.name}: {pulse_data}:{connecting_flag}            ", end='\r')
            print(end="\x1b[2K")
            self.counter = 0
        else:
            self.counter += 1
# Main function all wrapped in try/except
# This is to handle sensors being connected or waiting for connection
def sensor_2():
    try:
        db.show_connecting()

    # Initialisation for pulse oximeter 2 -------
        # print("\nInitializing sensor 2...")
        pulse2 = btle.Peripheral("00:A0:50:C8:CB:3A") #### Pulse oximeter #2
        pulse2.setDelegate( Sensor_2('pulse2') )


        # Setup to turn pulse2 notifications on 
        svc = pulse2.getServiceByUUID("49535343-fe7d-4ae5-8fa9-9fafd205e455")
        ch = svc.getCharacteristics("49535343-1e4d-4bd9-ba61-23c647249616")[0]
        pulse2.writeCharacteristic(ch.valHandle+1, SETUP_DATA, withResponse=True)

        

        # Main loop --------

        while True:

            if pulse2.waitForNotifications(2.0):
                # handleNotification() was called for pulse2. Iterates counter and outputs when counter limit met
                continue
            else:
                raise Exception
            
    except Exception as error:
        db.show_connecting()
        # traceback.print_exc() -------------------------uncomment to print traceback
        print("\nSensor 2 waiting for connection...")
        
        if 'pulse2' in locals():
            pulse2.disconnect()
        
        sensor_2()


#sensor_2()
    







