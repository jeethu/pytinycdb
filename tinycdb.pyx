'''
A very simple interface to the tinycdb DBM.

By Jeethu Rao <jeethu@jeethurao.com>
'''
cimport python_string as PS
cimport python_mem as PM

cdef extern from "fcntl.h" :
    int open( char* path, int flag, int mode )
    int O_RDWR, O_RDONLY, O_CREAT
    int S_IRUSR, S_IWUSR

cdef extern from "unistd.h" :
    int close( int fd )

cdef extern from "cdb.h" :
    struct cdb_make :
        pass
    int cdb_make_start( cdb_make* m, int fd )
    int cdb_make_add( cdb_make* m, void *k, unsigned int k_len, void* v, unsigned int v_len )
    int cdb_make_exists( cdb_make* m, void *k, int k_len )
    int cdb_make_finish( cdb_make* m )

cdef extern from "cdb.h" :
    int cdb_seek(int fd, void* key, unsigned int k_len, unsigned int* dlenp)
    int cdb_bread( int fd, void* buf, int len )

cdef int openFile( object file_name, int rw ) except -1 :
    cdef char *buffer
    cdef Py_ssize_t len
    cdef int rez
    rez = PS.PyString_AsStringAndSize(file_name, &buffer, &len)
    if rw :
        rez = open( buffer, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR )
    else :
        rez = open( buffer, O_RDONLY, 0 )
    if rez == -1 :
        raise IOError("Can't open file: \'%s\'"%file_name)
    return rez

class CDBError( Exception ) :
    pass

cdef class tinycdb:
    cdef int fd
    cdef public char mode
    cdef public fname
    cdef cdb_make cdbm
    def __contains__( self, key ) :
        cdef char *buffer
        cdef Py_ssize_t len
        cdef int rez
        cdef unsigned int dlen
        rez = PS.PyString_AsStringAndSize(key, &buffer, &len)
        if self.mode == c'w':
            rez = cdb_make_exists(&self.cdbm, buffer, len)
        else:
            rez = cdb_seek( self.fd, buffer, len, &dlen )
        if rez < 0 :
            raise CDBError("Unknown Error")
        return rez

    def __repr__(self):
        return "TinyCDB('%s', '%s')" % (self.fname, chr(self.mode))

    def close(self):
        if self.fd: close( self.fd )

def TinyCDB(fname, mode="r"):
    if mode == "r":
        return read(fname)
    return create(fname)

cdef class create(tinycdb):
    cdef int finished
    def __init__( self, fname ) :
        self.mode = 'w'
        self.fname = fname
        cdef int rez
        self.fd = openFile( fname, 1 )
        rez = cdb_make_start( &self.cdbm, self.fd )
        if rez != 0 :
            raise CDBError("Unknown Error")

    def __setitem__( self, key, value ) :
        cdef char *buffer1, *buffer2
        cdef Py_ssize_t len1, len2
        cdef int rez
        rez = PS.PyString_AsStringAndSize(key, &buffer1, &len1)
        rez = PS.PyString_AsStringAndSize(value, &buffer2, &len2)
        rez = cdb_make_add( &self.cdbm, buffer1, len1, buffer2, len2 )
        if rez != 0 :
            raise CDBError("Unknown Error")
    
    def close( self ) :
        if not self.finished :
            self.finished = 1
            cdb_make_finish(&self.cdbm)

    def __dealloc__( self ) :
        if not self.finished :
            self.finished = 1
            cdb_make_finish(&self.cdbm)
        if self.fd :
            close( self.fd )

cdef class read(tinycdb):
    def __init__( self, fname ) :
        self.fd = openFile( fname, 0 )
        self.mode = 'r'
        self.fname = fname

    def __getitem__( self, key ) :
        cdef char *buffer
        cdef Py_ssize_t len
        cdef int rez
        cdef unsigned int dlen
        cdef object ret
        rez = PS.PyString_AsStringAndSize(key, &buffer, &len)
        rez = cdb_seek( self.fd, buffer, len, &dlen )
        if rez < 0 :
            raise CDBError("Unknown Error")
        if rez == 0 :
            raise KeyError("Key \'%s\' not found"%key)
        buffer = <char *>PM.PyMem_Malloc(dlen)
        if buffer == NULL :
            raise MemoryError("malloc() failed")
        rez = cdb_bread( self.fd, buffer, dlen )
        if rez == 0 :
            ret = PS.PyString_FromStringAndSize( buffer, dlen )
            PM.PyMem_Free(buffer)
            return ret
        raise CDBError("Unknown Error")
        PM.PyMem_Free(buffer)

    def __dealloc__( self ) :
        self.close()
