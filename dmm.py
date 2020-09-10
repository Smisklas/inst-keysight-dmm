from VISAInstrument import VISAInstrument
from time import sleep

class DMM(VISAInstrument):
    def __init__(self, TCPIP):
        super().__init__(TCPIP)


    @property
    def value(self):
        return self.query('DATA:LAST?')

    def do_command(self, cmd, debug = False):
        self.session.write(cmd)
        sleep(self.SLEEP_TIME)
        if debug:
            self.check_instrument_errors()

    def do_query_number(self, query):
        if self.debug:
            print("Qyn = {}". format(query))
        results = self.query(query)
        self.check_instrument_errors()
        return float(results)

    def check_instrument_errors(self):

        while True:
            code, msg = self.query('SYST:ERR?').split(',')
            if int(code) == 0:
                break
            print('ERROR: {} ==> {}'.format(code, msg))



    def capture_data(self, samples, sampleRate):
        #capture a block of data
        sampleInterval = 1/sampleRate
        self.do_command('SAMPle:COUNt {}'.format(samples))
        #self.do_command('SAMPle:TIMer {}'.format(sampleInterval))
        self.do_command('INIT')
        self.do_command('*TRG')
        print('Measuring voltage...')
        sleep(samples*0.02)

        data = self.query('FETCH?')
        data = data.split(',')
        data = [float(value) for value in data]
        self.data = data

    def conf_volt(self, acdc, range, resolution):
        write_string = 'CONF:VOLT:{} {},{}'.format(acdc, range, resolution)
        self.do_command(write_string)

    def set_trigger(self, trigger_type):
        write_string = 'TRIG:SOUR {}'.format(trigger_type)
        self.do_command(write_string)

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
