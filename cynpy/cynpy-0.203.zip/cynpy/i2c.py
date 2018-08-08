
TRUE  = 1 # ACK, YES
FALSE = 0 # NAK, NO

class i2c:
    '''
    i2c class hierarchy
    -------------------
         i2c
             \
               aardvark_i2c
             / (aardv.py)
    aardvark
    
    '''
    def enum (me): raise NotImplementedError()
    def baud (me, ask): raise NotImplementedError()
    def i2cw (me, wdat): raise NotImplementedError()
    def read (me, dev, adr, rcnt, rpt=FALSE): raise NotImplementedError()

    def write (me, dev, adr, wdat): # SMB write
        return me.i2cw ([dev,adr]+wdat)

    def probe (me):
        print 'Searching I2C slave.....'
        hit = []
        for dev in range(0x80):
            if me.i2cw ([dev]):
                print 'device 0x%02x found' % (dev)
                hit += [dev]
        return hit



def choose_i2cmst (rpt=TRUE):
    from cynpy.aardv import aardvark_i2c
    i2cmst = 0
    if aardvark_i2c().enum (rpt) > 0:
        i2cmst = aardvark_i2c(0)

    return i2cmst



if __name__ == '__main__':

    i2cmst = choose_i2cmst ()

    from cynpy.basic import *
    if not no_argument ():
        if i2cmst!=0:
            if   sys.argv[1]=='probe' : print i2cmst.probe ()
            elif sys.argv[1]=='baud'  : print i2cmst.baud (argv_dec[2])
            elif sys.argv[1]=='write' : print i2cmst.i2cw (argv_hex[2:])
            elif sys.argv[1]=='read'  : print '0x%02X' % i2cmst.read (argv_hex[2], argv_hex[3], 2, TRUE)[0]
            else: print "command not recognized"
