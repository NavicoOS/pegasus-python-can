import can

bus = can.Bus(interface='pegasus', channel=0)

while True:
    print(bus.recv())
