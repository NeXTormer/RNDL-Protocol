import serial
import time
import encoder
from serialutil import write
from serialutil import receive

s = serial.Serial()
s.port = "COM7"
s.baudrate = 57600
s.parity = serial.PARITY_NONE
s.timeout = None

s.open()

#test
s.write(b"sys get ver\r\n")
r = s.read_until(terminator=b"\n")
print(r)

write("mac pause", s)
receive(s)

sentence = []

while True:
    write("radio rx 0", s)
    receive(s) #ok

    value = receive(s).decode()

    value = value.replace("b", "")
    value = value.replace("'", "")
    value = value.replace("r", "")
    value = value.replace("n", "")
    value = value.replace("\\", "")
    value = value.replace("  ", " ")
    value = value.split(" ");
    
    if len(value) == 2:

        value[1] = value[1].replace("\\r\\n", "")
        valueint = 1
        try:
            valueint = int(value[1])
        except ValueError:
            pass
        
        value = encoder.decodehex(value[1])
        print("Received packet (" + str(len(value)) + ")")
        
    else:
        value = None

    if value != None:
        if valueint == 0:
            print("".join(sentence))
            sentence = []
        else:
            sentence.append(value)
        
s.close()
