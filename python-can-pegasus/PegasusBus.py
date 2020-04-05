
import can
import logging
import time

import pegasus


log = logging.getLogger(__name__)

PEGASUS_DEVICE = None


def _get_pegasus_device():
    global PEGASUS_DEVICE
    if PEGASUS_DEVICE is not None:
        return PEGASUS_DEVICE
    pcreq = pegasus.get_a_pcreq_iface()
    PEGASUS_DEVICE = pegasus.PegasusUsbInterface(pcreq)
    return PEGASUS_DEVICE


class PegasusBus(can.BusABC):
    def __init__(self, channel, **kwargs):
        super().__init__(channel=channel, **kwargs)
        self._channel = channel
        self._pegasus = _get_pegasus_device()
        self._pegasus.can_open(self._channel)
        self._pegasus.can_bus_on(self._channel)

    def shutdown(self):
        self._pegasus.can_bus_off(self._channel)
        self._pegasus.can_close(self._channel)

    def send(self, msg: can.Message, timeout=None):
        flags = 0
        if msg.is_extended_id:
            flags = flags | pegasus.kvCAN_MSG_EXT
        if msg.is_error_frame:
            flags = flags | pegasus.kvCAN_MSG_ERROR_FRAME
        if msg.is_remote_frame:
            flags = flags | pegasus.kvCAN_MSG_RTR
        frameId = msg.arbitration_id
        payload = msg.data
        self._pegasus.can_write(self._channel, flags, frameId, payload)

    def _recv_internal(self, timeout=None):
        start = time.clock_gettime(time.CLOCK_MONOTONIC)
        while True:
            filtering_done = False
            ts, flags, id, data = self._pegasus.can_read(self._channel)
            if ts is not None:
                ext = (flags & pegasus.kvCAN_MSG_EXT) != 0
                err = (flags & pegasus.kvCAN_MSG_ERROR_FRAME) != 0
                rtr = (flags & pegasus.kvCAN_MSG_RTR) != 0
                dlc = len(data)
                msg = can.Message(arbitration_id=id, is_extended_id=ext,
                                  is_remote_frame=rtr, is_error_frame=err,
                                  channel=self._channel, dlc=dlc, data=data,
                                  timestamp=ts/1000)
                return (msg, filtering_done)
            if timeout is not None:
                if time.clock_gettime(time.CLOCK_MONOTONIC) > start + timeout:
                    return (None, filtering_done)
                time.sleep(0.01)


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    bus = PegasusBus(0)
