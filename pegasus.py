# See https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst

import usb.core
import usb.util
import time
import sys

# From PegasusPcSw/PegasusIntf/PegasusReqCodec.h
# tReqType enums related to CAN, there are plenty more!
PRT_GET_DESCRIPTOR = 1
PRT_CANOPEN = 9
PRT_CANCLOSE = 10
PRT_CANBUSON = 11
PRT_CANBUSOFF = 12
PRT_CANREAD = 13
PRT_CANWRITE = 14
PRT_GET_CANERRORCTRS = 22


# From Firwmware/Source/CAN/HAL/kvcanhw.h
# status is simply the return code of the KVaser API
kvCAN_OK = 0                   # /* successful routine call */
kvCAN_ERR_PARAM = -1           # /* Error in parameter */
kvCAN_ERR_NOMSG = -2           # /* No messages available */
kvCAN_ERR_NOTFOUND = -3        # /* Specified hw not found */
kvCAN_ERR_NOMEM = -4           # /* Out of memory */
kvCAN_ERR_NOCHANNELS = -5      # /* No channels available */
kvCAN_ERR_RESERVED_6 = -6
kvCAN_ERR_TIMEOUT = -7         # /* Timeout ocurred */
kvCAN_ERR_NOTINITIALIZED = -8  # /* Library not initialized */
kvCAN_ERR_NOHANDLES = -9       # /* Can't get handle */
kvCAN_ERR_INVHANDLE = -10      # /* Handle is invalid */
kvCAN_ERR_RESERVED_11 = -11
kvCAN_ERR_DRIVER = -12         # /* CAN driver type not supported */
kvCAN_ERR_TXBUFOFL = -13       # /* Transmit buffer overflow */
kvCAN_ERR_RESERVED_14 = -14
kvCAN_ERR_HARDWARE = -15       # /* Generic hardware error */


# From Firwmware/Source/CAN/HAL/kvcanhw.h
# Message flags
kvCAN_MSG_RTR = 0x01          # /* Msg is a remote request */
kvCAN_MSG_STD = 0x02          # /* Msg has a standard (11-bit) id */
kvCAN_MSG_EXT = 0x04          # /* Msg has an extended (29-bit) id */
kvCAN_MSG_ERROR_FRAME = 0x20  # /* Msg represents an error frame */


# Navico pegasus USB Ids
NAVICO_VENDOR_ID = 0x1cda
PEGASUS_PRODUCT_ID = 0x03e8


class PegasusInterface:
    PRIMARY_CHANNEL = 0
    SECONDARY_CHANNEL = 1

    def __init__(self, usb_device, debug=False):
        # No set_configuration(), conflicts with usb-hid (virtual
        # keyboard/mouse)
        # 3rd interface is CAN, choose the first (and only) alternate setting
        iface = usb_device.get_active_configuration()[(2, 0)]
        # Get r/w end points
        self._out_ep = iface[1]
        self._in_ep = iface[0]
        self._packet_id = 0
        self._debug = debug

    # Type: 9, Req: channel8 flags8, Ans: handle8 status16
    # Apparently the API doesn't use handle, have to pass channel number when
    # a handle is needed (!?!)
    def can_open(self, channel):
        self._usb_bulk(PRT_CANCLOSE, [channel], 2)  # blind close
        flags = 0  # TBD: what to do with these flags
        self._usb_bulk(PRT_CANOPEN, [channel, flags], 3)
        handle = self._usb_u8(0)
        status = self._usb_s16(1)
        assert status == kvCAN_OK
        return handle

    # Type 10, Req: handle8, Ans: status16
    def can_close(self, channel):
        self._usb_bulk(PRT_CANCLOSE, [channel], 2)
        status = self._usb_s16(0)
        assert status == kvCAN_OK

    # Type: 11, Req: handle8, Ans: status16
    def can_bus_on(self, channel):
        self._usb_bulk(PRT_CANBUSON, [channel], 2)
        status = self._usb_s16(0)
        assert status == kvCAN_OK

    # Type: 12, Req: handle8, Ans: status16
    def can_bus_off(self, channel):
        self._usb_bulk(PRT_CANBUSOFF, [channel], 2)
        status = self._usb_s16(0)
        assert status == kvCAN_OK

    # Type: 13, Req: handle8, Ans: status16 flags8 id32 len8 data* ts16
    def can_read(self, channel):
        self._usb_bulk(PRT_CANREAD, [channel], 18)
        status = self._usb_s16(0)
        if status == kvCAN_ERR_NOMSG:
            return (0, 0, 0, b'')  # No msg avail.
        flags = self._usb_u8(2)
        id_high = self._usb_u16(3)
        id_low = self._usb_u16(5)
        id = id_low + 65536*id_high
        count = self._usb_u8(7)
        data = self._reply[8:8+count]
        ts = self._usb_u16(8+count)
        assert status == kvCAN_OK
        return (ts, flags, id, data)

    # Type: 14, Req: handle8 flags8 id32 len8 data*, Ans: status16
    def can_write(self, channel, frameId, payload):
        # FIXME: FramId is 2 u16
        buf = [channel, kvCAN_MSG_EXT] + \
              list(frameId) + [len(payload)] + list(payload)
        self._usb_bulk(PRT_CANWRITE, buf, 2)
        status = self._usb_u16(0)
        assert status == kvCAN_OK

    # Type: 22, Req: handle8, Ans: tx32 rx32 err32 status16
    def get_can_stats(self, channel):
        self._usb_bulk(PRT_GET_CANERRORCTRS, [channel], 14)
        tx = self._usb_u32(0)
        rx = self._usb_u32(4)
        err = self._usb_u32(8)
        status = self._usb_u16(12)
        assert status == kvCAN_OK
        return (tx, rx, err)

    def _usb_bulk(self, type, params, reply_length):
        self._write_usb_packet(type, params)
        self._read_usb_packet(type, reply_length)

    def _usb_u8(self, index):
        return int.from_bytes(self._reply[index:index+1], byteorder='little')

    def _usb_u16(self, index):
        return int.from_bytes(self._reply[index:index+2], byteorder='little')

    def _usb_u32(self, index):
        return int.from_bytes(self._reply[index:index+4], byteorder='little')

    def _usb_s16(self, index):
        return int.from_bytes(self._reply[index:index+2], byteorder='little',
                              signed=True)

    def _write_usb_packet(self, type, payload):
        self._packet_id = self._packet_id + 1
        if self._packet_id == 0xFFFF:
            self._packet_id = 0
        count = 4 + len(payload)
        track_id = self._packet_id.to_bytes(2, byteorder='little')
        req = bytearray([count, type]) + track_id + bytearray(payload)
        if self._debug:
            print("USB > ", req.hex())
        assert self._out_ep.write(req) == count

    def _read_usb_packet(self, type, payload_length):
        ans = self._in_ep.read(4+payload_length)
        if self._debug:
            print("USB < ", bytearray(ans).hex())
        assert len(ans) == 4+payload_length
        assert ans[0] == 4+payload_length
        assert ans[1] == type
        assert int.from_bytes(ans[2:4], byteorder='little') == self._packet_id
        self._reply = ans[4:]


if __name__ == "__main__":
    debug_usb = len(sys.argv) > 1 and sys.argv[1] == "--debug-usb"
    # Find the device
    usb_device = usb.core.find(idVendor=NAVICO_VENDOR_ID,
                               idProduct=PEGASUS_PRODUCT_ID)
    assert usb_device is not None
    channel = PegasusInterface.PRIMARY_CHANNEL
    pegasus = PegasusInterface(usb_device, debug=debug_usb)
    pegasus.can_open(channel)
    pegasus.can_bus_on(channel)
    while True:
        ts, flags, id, data = pegasus.can_read(channel)
        try:
            if ts > 0:
                part1 = "{:06} {:02X} {:08X}".format(ts, flags, id)
                part2 = " ".join("{:02X}".format(d) for d in data)
                print(part1, part2)
            else:
                time.sleep(0.01)
        except KeyboardInterrupt:
            break
    tx, rx, err = pegasus.get_can_stats(channel)
    print("\nCounters: Rx={}, Tx={}, Err={}".format(rx, tx, err))
    pegasus.can_bus_off(channel)
    pegasus.can_close(channel)
