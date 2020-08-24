from VISAInstrument import VISAInstrument
from time import sleep

class DMM(VISAInstrument):
    def __init__(self, TCPIP):
        super().__init__(TCPIP)


    @property
    def configuration(self):
        return self.do_query_string('CONF?')

    @configuration.setter
    def configuration(self, command):
        self.do_command(command)

    @property
    def function(self):
        #voltage range of the dmm
        return self.__function

    @voltage_range.setter
    def voltage_range(self, voltageRange):
        self.__voltage_range = voltageRange

    @property
    def samples(self):
        return do_query_number('SAMPle:COUNt?')

    @samples.setter
    def samples(self, num_samples):
        self.do_command('SAMPLe:COUNt {}'.format(num_samples))

    @property
    def trigger(self):
        return 0

    @property
    def value(self):
        return self.do_query_string('DATA:LAST?')


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
