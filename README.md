Pegasus on Linux: Proof of Concept

TL-DW;
```
$ # Plug pegasus, find bus/dev id and fix permissions
$ lsusb -d 1cda:03e8
Bus 008 Device 011: ID 1cda:03e8
$ sudo chown $(id -un).$(id -gn) /dev/bus/usb/008/011
$ # Setup virtual env
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ # Output is time stamp, flags, frame ID, payload.
$ # CTRL-C to stop
$ # 1 NSS evo3 and 1 Naiad on CAN bus
$ python pegasus.py
Firmware version: v0.13
Serial number:    0xFFFFFFFF
PlatformId:       0x03EC
BoardId:          0x0000
023702 04 010209F8 C0 66 09 EA 04 FD 0E 68
023753 04 010109F8 FF FF FF 7F FF FF FF 7F
023804 04 020109F8 55 FF FF FF FF FF FF FF
023854 04 020209F8 7E FC 73 1A 19 00 FF FF
023905 04 1A011DF1 55 FF FF FF D6 FC FF FF
023956 04 21061CFF 13 99 FF 7F FF FF FF FF
024007 04 21071CFF 13 99 FF 7F FF FF FF FF
024057 04 10020DF0 7E F0 AC 47 00 B6 88 07
024108 04 010209F8 BA 66 09 EA C4 FC 0E 68
024159 04 000008FF 13 99 04 05 00 00 02 00
024209 04 010109F8 FF FF FF 7F FF FF FF 7F
024260 04 010209F8 BC 66 09 EA C6 FC 0E 68
024311 04 010109F8 FF FF FF 7F FF FF FF 7F
024361 04 020109F8 55 FF FF FF FF FF FF FF
024412 04 010209F8 C1 66 09 EA CB FC 0E 68
024463 04 020209F8 7F FC B9 1A 24 00 FF FF
^C
Counters: Rx=1204, Tx=0, Err=0
$ 
```

Notes:
 - USB packets can be dumped using `--debug-usb`.
 - This script should work on Windows too! Thanks to pyUSB.

For reference:
```
$ lsusb -v -d 1cda:03e8
Bus 008 Device 011: ID 1cda:03e8  
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               2.00
  bDeviceClass            0 (Defined at Interface level)
  bDeviceSubClass         0 
  bDeviceProtocol         0 
  bMaxPacketSize0        64
  idVendor           0x1cda 
  idProduct          0x03e8 
  bcdDevice            0.13
  iManufacturer           1 Navico Asia Pacific Ltd
  iProduct                2 Navico USB IO Computer
  iSerial                 3 SN-03EC-FFFFFFFF
  bNumConfigurations      1
  Configuration Descriptor:
    bLength                 9
    bDescriptorType         2
    wTotalLength           82
    bNumInterfaces          3
    bConfigurationValue     1
    iConfiguration          0 
    bmAttributes         0x80
      (Bus Powered)
    MaxPower              100mA
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        0
      bAlternateSetting       0
      bNumEndpoints           1
      bInterfaceClass         3 Human Interface Device
      bInterfaceSubClass      1 Boot Interface Subclass
      bInterfaceProtocol      1 Keyboard
      iInterface              4 Virtual Keyboard
        HID Device Descriptor:
          bLength                 9
          bDescriptorType        33
          bcdHID               1.01
          bCountryCode            0 Not supported
          bNumDescriptors         1
          bDescriptorType        34 Report
          wDescriptorLength      63
         Report Descriptors: 
           ** UNAVAILABLE **
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x81  EP 1 IN
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0008  1x 8 bytes
        bInterval              10
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        1
      bAlternateSetting       0
      bNumEndpoints           1
      bInterfaceClass         3 Human Interface Device
      bInterfaceSubClass      1 Boot Interface Subclass
      bInterfaceProtocol      2 Mouse
      iInterface              5 Virtual Mouse
        HID Device Descriptor:
          bLength                 9
          bDescriptorType        33
          bcdHID               1.01
          bCountryCode            0 Not supported
          bNumDescriptors         1
          bDescriptorType        34 Report
          wDescriptorLength      50
         Report Descriptors: 
           ** UNAVAILABLE **
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x84  EP 4 IN
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0008  1x 8 bytes
        bInterval              10
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        2
      bAlternateSetting       0
      bNumEndpoints           2
      bInterfaceClass       255 Vendor Specific Class
      bInterfaceSubClass    255 Vendor Specific Subclass
      bInterfaceProtocol    255 Vendor Specific Protocol
      iInterface              6 Client Application Interface
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x82  EP 2 IN
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0040  1x 64 bytes
        bInterval               0
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x02  EP 2 OUT
        bmAttributes            2
          Transfer Type            Bulk
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0040  1x 64 bytes
        bInterval               0
Device Status:     0x0000
  (Bus Powered)
```
