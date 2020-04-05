# Navico Pegasus driver for python-can

This package will register a plugin to the python-can package, this
plugin will add a 'pegasus' CAN Interface module.
This allows you to use python-can with Pegasus on Linux and Windows.

```
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip install .
$ cat test-me.py
import can

bus = can.Bus(interface='pegasus', channel=0)

while True:
    print(bus.recv())

$ python test-me.py
Timestamp:       47.193000    ID: 19fa0401    X                DLC:  8    6a 07 00 00 00 00 f0 0b     Channel: 0
Timestamp:       47.193000    ID: 19fa0401    X                DLC:  8    6b 2e 08 73 14 00 00 00     Channel: 0
Timestamp:       47.194000    ID: 19fa0401    X                DLC:  8    6c 00 00 00 f0 10 8b 18     Channel: 0
Timestamp:       47.194000    ID: 19fa0401    X                DLC:  8    6d 09 5c e8 03 00 00 00     Channel: 0
Timestamp:       47.195000    ID: 19fa0401    X                DLC:  8    6e 00 f0 1a 74 05 e7 55     Channel: 0
Timestamp:       47.196000    ID: 19fa0401    X                DLC:  8    6f 00 00 00 00 00 00 f0     Channel: 0
Timestamp:       47.196000    ID: 19fa0401    X                DLC:  8    70 1e d1 06 1f ab 00 00     Channel: 0
Timestamp:       47.197000    ID: 19fa0401    X                DLC:  8    71 00 00 00 00 f0 03 00     Channel: 0
Timestamp:       47.197000    ID: 19fa0401    X                DLC:  8    72 00 00 00 08 07 00 00     Channel: 0
Timestamp:       47.213000    ID: 09f80102    X                DLC:  8    ff ff ff 7f ff ff ff 7f     Channel: 0
Timestamp:       47.217000    ID: 19fa0401    X                DLC:  8    73 00 00 f0 4a 7f 07 13     Channel: 0
Timestamp:       47.217000    ID: 19fa0401    X                DLC:  8    74 b8 00 00 00 00 00 00     Channel: 0
Timestamp:       47.218000    ID: 19fa0401    X                DLC:  8    75 f0 ff ff ff ff ff ff     Channel: 0
Timestamp:       47.219000    ID: 15fd0604    X                DLC:  8    ff ff ff ff ff ff ff ff     Channel: 0
Timestamp:       47.219000    ID: 0dff0806    X                DLC:  8    60 02 7d 99 ff ff ff ff     Channel: 0
Timestamp:       47.241000    ID: 0df01001    X                DLC:  8    5f f0 ff ff ff ff ff ff     Channel: 0
Timestamp:       47.242000    ID: 0df50b04    X                DLC:  8    ff ff ff ff ff ff 7f ff     Channel: 0
Timestamp:       47.243000    ID: 09f80101    X                DLC:  8    ff ff ff 7f ff ff ff 7f     Channel: 0
Timestamp:       47.263000    ID: 0df01002    X                DLC:  8    e0 f0 ff ff ff ff ff ff     Channel: 0
Timestamp:       47.263000    ID: 1df11a02    X                DLC:  8    e1 ff ff ff d7 fc ff ff     Channel: 0
Timestamp:       47.313000    ID: 1df11a08    X                DLC:  8    da ff ff ff d7 fc ff ff     Channel: 0
Timestamp:       47.313000    ID: 09f80102    X                DLC:  8    ff ff ff 7f ff ff ff 7f     Channel: 0
Timestamp:       47.316000    ID: 08ff0000    X                DLC:  8    13 99 04 05 00 00 02 00     Channel: 0
^C
```


