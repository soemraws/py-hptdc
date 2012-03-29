#!/usr/bin/env python

import ctypes
import numpy



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

hptdc_wrapper.tdc_manager_blocking_read.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)
hptdc_wrapper.tdc_manager_blocking_read.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_read_tdc_hit.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)
hptdc_wrapper.tdc_manager_read_tdc_hit.restype = ctypes.c_int

hptdc_wrapper.tdc_manager_blocking_read_tdc_hit.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)
hptdc_wrapper.tdc_manager_blocking_read_tdc_hit.restype = ctypes.c_int


# TDC Exceptions

class TDCConfigException(Exception):
    def __init__(self, errorString):
        self.strerror = errorString

    def __str__(self):
        return self.strerror

    def __repr__(self):
        return 'TDCConfig Exception: %s' % self.strerror


def CHK(value):
    if value is None or value == -1:
        raise TDCConfigException(hptdc_wrapper.tdc_strerror())
    else:
        return value



# TDC manager

states = ['uninitialized',
          'not configured',
          'configured',
          'running',
          'paused',
          'shutdown']

class TDCManager(object):
    def __init__(self, vendor_id=0x1A13, device_id=0x0001):
        self.manager = CHK(hptdc_wrapper.tdc_manager_create(vendor_id,
                                                            device_id))

    def __del__(self):
        if self.manager is not None:
            state = self._get_state()
            if state == 3 or state == 4:
                hptdc_wrapper.tdc_manager_stop(self.manager)
            if state > 0 and state != 5:
                hptdc_wrapper.tdc_manager_cleanup(self.manager)
            hptdc_wrapper.tdc_manager_destroy(self.manager)
            self.manager = None

    def init(self):
        CHK(hptdc_wrapper.tdc_manager_init(self.manager))

    def _get_state(self):
        return CHK(hptdc_wrapper.tdc_manager_get_state(self.manager))

    def get_state(self):
        return states[self._get_state()]

    def read_config_file(self, file):
        CHK(hptdc_wrapper.tdc_manager_read_config_file(self.manager,file))

    def clean_up(self):
        CHK(hptdc_wrapper.tdc_manager_cleanup(self.manager))
        
    def start(self):
        CHK(hptdc_wrapper.tdc_manager_start(self.manager))

    def pause(self):
        CHK(hptdc_wrapper.tdc_manager_pause(self.manager))
        
    def stop(self):
        CHK(hptdc_wrapper.tdc_manager_stop(self.manager))

    # Python is retarded because it doesn't allow a method named continue
    def continu(self):
        CHK(hptdc_wrapper.tdc_manager_continue(self.manager))

    def read(self, buffer,block=False):
        assert buffer.dtype == numpy.dtype('uint32')
        if block:
            return CHK(hptdc_wrapper.tdc_manager_blocking_read(self.manager,
                                                               buffer.ctypes.data,
                                                               buffer.size))
        else:
            return CHK(hptdc_wrapper.tdc_manager_read(self.manager,
                                                      buffer.ctypes.data,
                                                      buffer.size))

    def get_parameter(self, parameter):
        return CHK(hptdc_wrapper.tdc_manager_get_parameter(self.manager,
                                                                 parameter))

    def set_parameter(self, config_or_parameter, value=None):
        if value is None:
            return CHK(hptdc_wrapper.tdc_manager_set_parameter_config(self.manager,
                                                               config_or_parameter))
        else:
            return CHK(hptdc_wrapper.tdc_manager_set_parameter(self.manager,
                                                               config_or_parameter,
                                                               value))

    def get_parameter_names(self):
        count = ctypes.c_int(0)
        retval = CHK(hptdc_wrapper.tdc_manager_get_parameter_names(self.manager,
                                                                   ctypes.byref(count)))
        names = ctypes.cast(retval, ctypes.POINTER(ctypes.c_char_p * count.value))
        return list(names.contents)

    def read_tdc_hit_with_numpy_array(self, buffer):
        assert buffer.dtype == numpy.dtype('uint64')
        return CHK(hptdc_wrapper.tdc_manager_read_tdc_hit(self.manager,
                                                          buffer.ctypes.data,
                                                          buffer.size))

    def read_tdc_hit(self, buffer, block=False):
        if block:
            return CHK(hptdc_wrapper.tdc_manager_blocking_read_tdc_hit(self.manager,
                                                                  ctypes.byref(buffer),
                                                                  len(buffer)))
        else: 
            return CHK(hptdc_wrapper.tdc_manager_read_tdc_hit(self.manager,
                                                              ctypes.byref(buffer),
                                                              len(buffer)))

    def get_driver_version(self):
        return CHK(hptdc_wrapper.tdc_manager_get_driver_version(self.manager))
        

class TDCHit(ctypes.Structure):
    _fields_ = [('time', ctypes.c_longlong),
                ('channel', ctypes.c_ubyte),
                ('type', ctypes.c_ubyte),
                ('bin', ctypes.c_ushort)]


def make_hit_buffer(size):
    return numpy.empty(size, dtype='uint32', order='C')

def make_tdc_hit_buffer(size):
    return (TDCHit * size) ()
    # return numpy.empty(size, dtype='uint64', order='C')

# Below is the C++ example program from the manual, converted to python
if __name__ == '__main__':
    import struct
    
    manager = TDCManager(0x1a13, 0x0001)

    manager.init()
    #manager.read_config_file('myexperiment.cfg')
    manager.set_parameter('GroupingEnable','false')
    manager.start()

    of = open('test.dat', 'wb')
    of.write(struct.pack('<L', 0x200061a8))
    
    amount_to_read = 10
    buffer = numpy.empty(2000, dtype='uint32', order='C')
#    buffer = make_hit_buffer(2000)
    while (amount_to_read > 0):
        count = manager.read(buffer)
        print 'Read: %d' % count
        for i in range(min(count,amount_to_read)):
            of.write(struct.pack('<L', int(buffer[i])))
        amount_to_read -= count
    
    of.close()
    manager.stop()
    manager.clean_up()
