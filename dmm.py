import visa
from time import sleep

class DMM(object):
    def __init__(self, TCPIP):
        #The session will be contained within the self.session object, the other methods
        #facilitates the communication with the DMM in a more compact manner.

        #VISA_ADDRESS = 'USB0::10893::5633::MY59018505::0::INSTR' #USB type adress
        self.VISA_ADDRESS = 'TCPIP::{}::5025::SOCKET'.format(TCPIP)
        try:
            self.resourceManager = visa.ResourceManager()
            self.session = self.resourceManager.open_resource(self.VISA_ADDRESS)
            self.session.read_termination = '\n' #termination for TCP/IP

            #SERIAL SETTINGS ******* NOT USED FOR TCPIP
            #self.session.set_visa_attribute(visa.constants.VI_ATTR_ASRL_BAUD, 9600)
            #self.session.set_visa_attribute(visa.constants.VI_ATTR_ASRL_DATA_BITS, 8)
            #self.session.set_visa_attribute(visa.constants.VI_ATTR_ASRL_PARITY, visa.constants.VI_ASRL_PAR_NONE)
            #self.session.set_visa_attribute(visa.constants.VI_ATTR_ASRL_FLOW_CNTRL, visa.constants.VI_ASRL_FLOW_DTR_DSR)
            self.session.timeout=None #No timeout, just to acommocade for long measurements. (might cause errors....)
        except visa.Error as ex:
            print("Couldn't connect to '{}', exiting now...".format(VISA_ADDRESS))

    def get_id(self):
        self.session.write('*IDN?')
        return self.session.read()

    def conf_volt(self, acdc, range, resolution):
        write_string = 'CON:VOLT:{} {},{}'.format(acdc, range, resolution)
        self.session.write(write_string)

    def set_trigger(self, samples):
        self.samples = samples
        write_string = 'SAMP:COUN {};TRIG: SOUR BUS;INIT'.format(samples)
        self.session.write(write_string)

    def fetch_data(self):
        write_string = '*TRG;FETCH?'
        self.session.write(write_string)
        return self.session.read()

    def read(self):
        # Initiate a measurement and return the data
        self.session.write('READ?')
        data = self.session.read()
        data = data.strip('\n').split(',')
        data = [float(x) for x in data]
        
        return data

    def clear_data(self):
        write_string = 'DATA:REM'
        self.session.write(write_string)

    def abort(self):
        write_string = 'ABOR'
        self.session.write(write_string)

    def close(self):
        self.session.close()
        self.resourceManager.close()

    def debug(self, cmd):
        self.session.write(cmd)
        print(self.session.read())
