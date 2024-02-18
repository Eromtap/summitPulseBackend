import threading
import time


import sensor_1 as one
import sensor_2 as two


'''
While loop inside main checks to see if processes are alive.
This is to handle the 'BrokenPipeLine' error.
I can't figure out another way to handle it. A better programmer could...
In this case it's fine, if the process is dead, while loop just restarts it.
It's ugly, but it works.
'''


def main():
    
    p1 = threading.Thread(target=one.sensor_1, args = ())
    p1.start()
    print("Initializing Sensor 1...")
    
    p2 = threading.Thread(target=two.sensor_2, args = ())
    p2.start()
    print("Initializing Sensor 2...")

    
    while 1:
        if not p1.is_alive():
            p1 = threading.Thread(target=one.sensor_1, args = ())
            p1.start()
            print("Initializing Sensor 1...")            
        if not p2.is_alive():
            p2 = threading.Thread(target=two.sensor_2, args = ())
            p2.start()
            print("Initializing Sensor 2...")
            
            time.sleep(.5)


if __name__ == '__main__':
    main()



