import visa



class VISAInstrument(object):
    """docstring for VISAInstrument."""

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

    @property
    def identity(self):
        self.session.write('*IDN?')
        return self.session.read()


    def close(self):
        self.session.close()
        self.resourceManager.close()
        print('Connection closed...')

    def do_command(self, cmd, hide_params=False):
        if hide_params:
            (header, data) = cmd.split(' ',1)
            if self.debug:
                print('\nCmd = {}'.format(header))
        else:
            if self.debug:
                print('\nCmd = {}'.format(cmd))

        self.session.write(cmd)

        if hide_params:
            self.check_instrument_errors(header)
        else:
            self.check_instrument_errors(cmd)

    def do_command_ieee_block(self, cmd, values):
        if self.debug:
            print('Cmd = {}'.format(cmd))
        self.session.write_binary_values(cmd+' ', values, datatype='B')
        self.check_instrument_errors(cmd)

    def do_query_string(self, query):
        if self.debug:
            print('Qys = {}'.format(query))
        result = self.session.query(query)
        self.check_instrument_errors(query)
        return result

    def do_query_number(self, query):
        if self.debug:
            print("Qyn = {}". format(query))
        results = self.session.query(query)
        self.check_instrument_errors(query)
        return float(results)

    def do_query_ieee_block(self, query):
        if self.debug:
            print('Qyb = {}'.format(query))
        result = self.session.query_binary_values(query, datatype='s')
        self.check_instrument_errors(query)
        return result[0]

    def check_instrument_errors(self, cmd):

        while True:
            error_string = self.session.query(":SYSTem:ERRor? STRing")
            if error_string: # If there is an error string value
                if error_string.find('0,',0,2) == -1:
                    print('ERROR: {}, command: {}'.format(error_string, cmd))
                    print('Exited because of error.')
                    sys.exit(1)
                else:
                    break

            else:
                print('ERROR: :SYSTem:ERRor? STRing returned nothing, command: {}'.format(cmd))
                print('Exited because of error.')
                sys.exit(1)
