#coding=utf-8

import os
from cffi import FFI


__all__ = ['init_model', 'get_model']

__Model__ = None


class AMRDecoder(object):
    ffi = FFI()
    decoder = None

    def init_model(self, config):
        so_file = config['amr']['so_file']
        if not os.path.exists(so_file):
            return False
        self.decoder = self.ffi.dlopen(so_file)
        self.ffi.cdef('''
                typedef struct AMRRet {
                    const char *ret;
                    unsigned int size;
                } AMRRet;
                AMRRet* LittleAmrwb(const char *, const int);
                AMRRet* LittleAmrnb(const char *, const int);
                void FreeAMRRet(const AMRRet *);
            ''')
        return True

    def read_amr(self, filename):
        data = bytes(open(filename, 'rb').read())
        return data

    def LittleAmrwb(self, data):
        try:
            pcm_ptr = self.decoder.LittleAmrwb(data, len(data))
            pcm_gc = self.ffi.gc(pcm_ptr, self.decoder.FreeAMRRet)
            pcm_length = pcm_ptr.size
            pcm = bytes(self.ffi.buffer(pcm_ptr.ret, pcm_length)[:])
            return pcm, pcm_length
        except:
            return b'', 0

    def LittleAmrnb(self, data):
        try:
            pcm_ptr = self.decoder.LittleAmrnb(data, len(data))
            pcm_gc = self.ffi.gc(pcm_ptr, self.decoder.FreeAMRRet)
            pcm_length = pcm_ptr.size
            pcm = bytes(self.ffi.buffer(pcm_ptr.ret, pcm_length)[:])
            return pcm, pcm_length
        except:
            return b'', 0

def init_model(config):
    global __Model__
    __Model__ = AMRDecoder()
    status = __Model__.init_model(config)
    return status

def get_model():
    global __Model__
    return __Model__

