#!/usr/bin/env python

import ctypes
import numpy


# class TDCInfo(ctypes.Structure):
#     _fields_ = [('index', ctypes.c_int),
#                 ('channelStart', ctypes.c_int),
#                 ('channelCount', ctypes.c_int),
#                 ('highResChannelCount', ctypes.c_int),
#                 ('highResChannelStart', ctypes.c_int),
#                 ('lowResChannelCount', ctypes.c_int),
#                 ('lowResChannelStart', ctypes.c_int),
#                 ('resolution', ctypes.c_double),
#                 ('serialNumber', ctypes.c_ulong),
#                 ('version', ctypes.c_int),
#                 ('fifoSize', ctypes.c_int),
#                 ('INLCorrection', POINTER(ctypes.c_int)),
#                 ('DNLData', POINTER(ctypes.c_ushort)),
#                 ('flashValid', ctypes.c_bool),
#                 ('bufferSize', ctypes.c_int),
#                 ('boardConfiguration', ctypes.c_ubyte)]



# Library wrapper stuff

hptdc_wrapper = ctypes.cdll.hptdc_wrapper

hptdc_wrapper.tdc_strerror.restype = ctypes.c_char_p



hptdc_wrapper.tdc_manager_create.argtypes = (ctypes.c_ushort, ctypes.c_ushort)
hptdc_wrapper.tdc_manager_create.restype = ctypes.c_void_p

hptdc_wrapper.tdc_manager_destroy.argtypes = (ctypes.c_void_p, )



hptdc_wrapper.tdc_manager_init.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_init.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_cleanup.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_cleanup.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_get_tdc_count.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_get_tdc_count.restype = ctypes.c_int



hptdc_wrapper.tdc_manager_set_parameter_config.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
hptdc_wrapper.tdc_manager_set_parameter_config.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_read_config_string.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
hptdc_wrapper.tdc_manager_read_config_string.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_set_parameter.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p)
hptdc_wrapper.tdc_manager_set_parameter.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_read_config_file.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
hptdc_wrapper.tdc_manager_read_config_file.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_reconfigure.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_reconfigure.restype = ctypes.c_int



hptdc_wrapper.tdc_manager_get_parameter.argtypes = (ctypes.c_void_p, ctypes.c_char_p)
hptdc_wrapper.tdc_manager_get_parameter.restype = ctypes.c_char_p

hptdc_wrapper.tdc_manager_get_parameter_names.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
hptdc_wrapper.tdc_manager_get_parameter_names.restype = ctypes.c_void_p

hptdc_wrapper.tdc_manager_get_driver_version.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_get_driver_version.restype = ctypes.c_int

# hptdc_wrapper.tdc_manager_get_tdc_info.argtypes = (ctypes.c_void_p, )
# hptdc_wrapper.tdc_manager_get_tdc_info.restype = ctypes.POINTER(TDCInfo)

hptdc_wrapper.tdc_manager_get_state.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_get_state.restype = ctypes.c_int



hptdc_wrapper.tdc_manager_start.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_start.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_stop.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_stop.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_pause.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_pause.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_continue.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_continue.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_clear_buffer.argtypes = (ctypes.c_void_p, )
hptdc_wrapper.tdc_manager_clear_buffer.restype = ctypes.c_int



hptdc_wrapper.tdc_manager_read.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)
hptdc_wrapper.tdc_manager_read.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_read_tdc_hit.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)
hptdc_wrapper.tdc_manager_read_tdc_hit.restype = ctypes.c_int


# TDC Exceptions

class TDCConfigException(Exception):
    def __init__(self, errorString):
        self.strerror = errorString

    def __repr__(self):
        return 'TDCConfigException: %s' % self.strerror


def CHK(value):
    if value is None or value == -1:
        raise TDCConfigException(hptdc_wrapper.tdc_strerror())
    else:
        return value


#TDC manager states

STATE_UNINITIALIZED = 0
STATE_NOT_CONFIGURED = 1
STATE_CONFIGURED = 2
STATE_RUNNING = 3
STATE_PAUSED = 4
STATE_SHUTDOWN = 5

TDCHIT_FALLING = 0
TDCHIT_RISING = 1
TDCHIT_ERROR = 2


# TDC manager

class TDCManager(object):
    def __init__(self, vendor_id=0x1A13, device_id=0x0001):
        self._ptr = CHK(hptdc_wrapper.tdc_manager_create(vendor_id,
                                                         device_id))
        driver_version = self.get_driver_version()
        self._driver_version = map(lambda x: driver_version & x,
                                   (0x00ff0000, 0x0000ff00, 0x000000ff))

    def __del__(self):
        if self._ptr is not None:
            state = self.get_state()
            if state == 3 or state == 4:
                hptdc_wrapper.tdc_manager_stop(self._ptr)
            if state > 0 and state != 5:
                hptdc_wrapper.tdc_manager_cleanup(self._ptr)
            hptdc_wrapper.tdc_manager_destroy(self._ptr)
            self._ptr = None


    ## Startup and cleanup

    def init(self):
        """Should be called once before using the TDCManager. init()
        detects all present TDC devices, acquires all available information
        on the those devices and maps the address space for PCI access. It
        also reads the "global.cfg" configuration file if present in the
        current directory.

        Can throw all exceptions that are related to parsing the
        configuration file."""
        CHK(hptdc_wrapper.tdc_manager_init(self._ptr))

    def clean_up(self):
        """Should be called once before exiting the program."""
        CHK(hptdc_wrapper.tdc_manager_cleanup(self._ptr))

    def get_tdc_count(self):
        """Returns the number of HPTDC boards found in the
        system. From 0 to 3."""
        return CHK(hptdc_wrapper.tdc_manaager_get_tdc_count(self._ptr))


    ## Configuration

    def read_config_string(self, parameter):
        """Read in a string with the syntax of a configuration file
        line as described in the previous section. The string might
        contain multiple lines.
        
        Can only be called if the TDC is stopped (states 0, 1 and
        2). Throws an exception otherwise.

        Returns false if there were illegal parameters or syntax
        errors. True otherwise."""
        return (CHK(hptdc_wrapper.tdc_manager_read_config_string(self._ptr,
                                                                 parameter)) == 1)
    
    def set_parameter(self, config_or_property, value=None):
        """When value is None, read in a string, given in
        config_or_property, with the syntax of a configuration file
        line as described in the manual. The string might contain
        multiple lines.

        When value is not None, set the value of a parameter
        identified by the parameter name in config_or_property.
        
        Can only be called if the TDC is stopped (states 0, 1 and
        2). Throws an exception otherwise.

        Returns false if there were illegal parameters or syntax
        errors. True otherwise."""
        if value is None:
            return (CHK(hptdc_wrapper.tdc_manager_set_parameter_config(self._ptr,
                                                                       config_or_property)) == 1)
        else:
            return (CHK(hptdc_wrapper.tdc_manager_set_parameter(self._ptr,
                                                                config_or_property,
                                                                value)) == 1)

    def read_config_file(self, file):
        """Read in a configuration file.
        
        Can only be called if the TDC is stopped (states 0, 1 and
        2). Throws an exception otherwise.

        Can also throw exceptions generated while opening or reading
        the file.

        Returns True if successful, False if there was an error."""
        return (CHK(hptdc_wrapper.tdc_manager_read_config_file(self._ptr,file)) == 1)

    def reconfigure(self):
        """Writes configuration data to the device. Use after
        configuration has been changed. This operation is slow.

        Can only be called if the TDC is stopped (states 0, 1 and
        2). Throws an exception otherwise.

        Throws an exception if a parameter cannot be parsed."""
        CHK(hptdc_wrapper.tdc_manager_reconfigure(self._ptr))


    ## Reflection

    def get_parameter(self, parameter):
        """Get the value of a parameter. If the parameter does not
        exist or has not been set an empty string is returned."""
        return CHK(hptdc_wrapper.tdc_manager_get_parameter(self._ptr,
                                                                 parameter))

    def get_parameter_names(self):
        """Get the names of all parameters that are set."""
        count = ctypes.c_int(0)
        retval = CHK(hptdc_wrapper.tdc_manager_get_parameter_names(self._ptr,
                                                                   ctypes.byref(count)))
        names = ctypes.cast(retval, ctypes.POINTER(ctypes.c_char_p * count.value))
        return list(names.contents)

    def get_driver_version(self):
        """The lowest three bytes returned are the three digits of the driver version."""
        return CHK(hptdc_wrapper.tdc_manager_get_driver_version(self._ptr))

    
    ## Control
    
    def start(self):
        """Configure all TDCs with the parameters set by the methods
        described in the previous section and start all TDCs. This
        method can require several milliseconds to complete when
        called from state "NOT_CONFIGURED". To precisely time the
        start of the data acquisition call reconfigure() first.

        If called from state NOT_CONFIGURED exceptions thrown from
        reconfigure() can occur.  Also throws an exception if called
        from state UNINITIALIZED."""

        CHK(hptdc_wrapper.tdc_manager_start(self._ptr))
        
    def stop(self):
        """Stop taking data and turn off TDCs. The state of the
        hardware and software queues is undefined after this
        operation. No additional data should be read out. To get all
        data in the queues call pause() and empty the buffers before
        calling this method.

        The TDC is put into a low power state that can only be
        recovered by a Start() operation.

        Throws an exception if called in states UNINITIALIZED or
        SHUTDOWN."""
        CHK(hptdc_wrapper.tdc_manager_stop(self._ptr))

    def pause(self):
        """Stop taking data. Data already in the hardware and software
        buffers is left intact and can be read out. The TDC hardware
        is kept in a state that allows to resume data acquisition
        immediately.  Frame counters continue to count.

        Throws an exception when called from a state other then PAUSED
        or RUNNING."""
        CHK(hptdc_wrapper.tdc_manager_pause(self._ptr))

    # Python is retarded because it doesn't allow a method named continue
    def continu(self):
        """Quickly continue taking data after a pause(). Buffers are
        left intact and frame counters are left unaltered.  It is
        legal to use start() to resume operation instead.

        Throws an exception when called from a state other then PAUSED
        or RUNNING."""

        CHK(hptdc_wrapper.tdc_manager_continue(self._ptr))

    def clear_buffer(self):
        """Clears all buffers. Only meaningful in state PAUSED.
        
        Throws an exception if called in state RUNNING. Has no effect
        in other states."""
        CHK(hptdc_wrapper.tdc_manager_clear_buffer(self._ptr))

    def get_tdc_info(self):
        """Get the information on TDC card number index.
        Throws an exception if called in state UNINITIALIZED."""
        # Not implemented yet
        pass

    def get_state(self):
        """Returns the current state of the TDCManager.
        
        STATE_UNINITIALIZED = 0
        STATE_NOT_CONFIGURED = 1
        STATE_CONFIGURED = 2
        STATE_RUNNING = 3
        STATE_PAUSED = 4
        STATE_SHUTDOWN = 5"""
        return CHK(hptdc_wrapper.tdc_manager_get_state(self._ptr))

    def get_tdc_status_register(self):
        """Returns a 64 bit number that can be sent to the
        manufacturer for debugging purposes."""
        return hptdc_wrapper.tdc_manager_get_tdc_status_register(self._ptr)

    
    ## Readout
    
    def read(self, buffer):
        """Copy TDC data into a numpy array with data type uint32 and
        C ordering, i.e., use:

          buffer = numpy.empty(count, dtype='uint32', order='C')

        to create a buffer of size count.  If grouping is enabled one
        group is read. Otherwise all available data up to the size of
        the buffer is read. The number of data words that were read is
        re- turned as an integer.

        If grouping is enabled and no group is found within a certain
        time interval read() returns 0.

        The data returned hast the format described in the manual. To
        get the absolute time multiply the integer values reported by
        resolution as specified in the TDCInfo structure."""
        return CHK(hptdc_wrapper.tdc_manager_read(self._ptr,
                                                  buffer.ctypes.data,
                                                  buffer.size))

    def read_tdc_hit(self, buffer):
        """Copy TDC data into a TDCHit buffer, i.e. use:

          buffer = (TDCHit * count)()

        to create a buffer of size count. All available data up to the
        size of the buffer is read.

        Uses a data format that is easier to use and provides a better
        DNL and INL than read().

        Uses more memory and CPU cycles.
        
        Does not support grouping.

        Output data is sorted by timestamp.

        The data returned uses a structure that obsoletes
        rollovers. Also, times are reported in multiples of one
        picosecond, independently of the TDCs native resolution. A
        more fine-grained INL correction is used in this mode slightly
        reduce the measurement error of the TDC.

        The TDCHit struct contains:

        time -- The timestamp in picoseconds
        channel -- The channel where the event occurred
        type -- The type of event (TDCHIT_FALLING=0, TDCHIT_RISING=1, TDCHIT_ERROR=2)
        bin -- auxilliary information that can be ignored in normal operation.

        If type is set to 2 an error word in the format described on
        page 6 of the manual will be copied into the lower 32 bits of
        time."""
        return CHK(hptdc_wrapper.tdc_manager_read_tdc_hit(self._ptr,
                                                          ctypes.byref(buffer),
                                                          len(buffer)))



class TDCHit(ctypes.Structure):
    _fields_ = [('time', ctypes.c_longlong),
                ('channel', ctypes.c_ubyte),
                ('type', ctypes.c_ubyte),
                ('bin', ctypes.c_ushort)]



def test_read_tdc_hit(output='myexperiment.csv',config='myexperiment.cfg'):
    '''This is a translation to python of the C# example on page 24 of the manual.'''
    manager = TDCManager(0x1a13, 0x0001)

    manager.init()
    manager.read_config_file(config)
    manager.start()

    amount_to_read = 1000000
    buffer = (TDCHit * 2000)()

    of = open(output, 'w')

    while amount_to_read > 0:
        count = manager.read_hptdc_hit(buffer)
        for i in range(count):
            of.write('%d, %d, %d\n' % (buffer[i].channel, buffer[i].type, buffer[i].time)
        amount_to_read -= count

    of.close()
    manager.stop()
    manager.clean_up()


def test_read(output='test.dat', config='myexperiment.cfg')
    '''This is a translation to python of the C++ example on page 24 of the manual.'''
    import struct
    
    manager = TDCManager(0x1a13, 0x0001)

    manager.init()
    manager.read_config_file('myexperiment.cfg')
    manager.start()

    amount_to_read = 1000000
    buffer = numpy.empty(2000, dtype='uint32', order='C')
    of = open('test.dat', 'wb')
    of.write(struct.pack('<L', 0x200061a8))
    
    while amount_to_read > 0:
        count = manager.read(buffer)
        for i in range(min(count,amount_to_read)):
            of.write(struct.pack('<L', int(buffer[i])))
        amount_to_read -= count
    
    of.close()
    manager.stop()
    manager.clean_up()


# If run as a script, then run the C++ example.
if __name__ == '__main__':
    test_read()
