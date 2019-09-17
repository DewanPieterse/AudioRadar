import serial
import time

s = serial.Serial('COM5', 500000) # ttyACM1 for Arduino board

connected = False
samples = 1000

s.reset_input_buffer()

s.write(str(samples).encode())
time.sleep(1)
a = []

while(len(a) != samples):
    
    while s.inWaiting() > 0:
        
        x = s.readline()
        try:
            dec = float(x[0:len(x)-2].decode("ascii"))
        except:
            pass
        a.append(dec)


print(a)   

s.reset_input_buffer()
s.reset_output_buffer()
s.close()