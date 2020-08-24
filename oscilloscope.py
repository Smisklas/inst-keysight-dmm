import visa
from VISAInstrument import VISAInstrument
from time import sleep
import struct
import sys

class SCOPE(VISAInstrument):
    def __init__(self, TCPIP):
        super().__init__(TCPIP)

    def store_setup(self, filename):
        sSetup = self.do_query_ieee_block(':SYSTem:SETup?')
        with open(filename, 'wb') as f:
            f.write(sSetup)

        print('Setup bytes saved: {}'.format(len(sSetup)))


    def restore_setup(self, filename):
        with open(filename, 'rb') as f:
            sSetup = f.read()
        self.do_command_ieee_block(':SYSTem:SETup', sSetup)
        print('Setup bytes restored: {}'.format(len(sSetup)))

    def save_display(self, filename):
        sDisplay = self.do_query_ieee_block(":DISPlay:DATA? PNG")
        with open(filename, 'wb') as f:
            f.write(sDisplay)
        print('Screen image written to {}'.format(filename))

    def acquire(self, numPoints):
        self.do_command(':ACQuire:POINts {}'.format(numPoints))
        self.do_command(':DIGitize')

    def get_frequency(self, source):
        #set SOURce
        self.do_command(":MEASure:SOURce CHANnel{}".format(source))
        return float(self.do_query_string(':MEASure:FREQuency?'))

    def get_amplitude(self, source):
        self.do_command(":MEASure:SOURce CHANnel{}".format(source))
        return float(self.do_query_string(':MEASure:VAMPlitude?'))

    def get_spectrum(self, channel, filename):
        #Set measurement channel
        self.do_command(":WAVeform:SOURce CHANnel{}".format(channel))
        self.do_command(":WAVeform:FORMat BYTE")
        #Get numeric values for waveform axes
        x_increment = self.do_query_number(":WAVeform:XINCrement?")
        x_origin=0
        #x_origin = self.do_query_number(':WAVeform:XORigin?')
        #y_increment = self.do_query_number(':WAVeform:YINCrement?')
        #y_origin = self.do_query_number(":WAVeform:YORigin?")

        #get waveform data
        self.do_command(":WAVeform:STReaming OFF")
        sData = self.do_query_ieee_block(":WAVeform:DATA?")

        #unpack signed byte data.
        values = struct.unpack('%db' % len(sData), sData)
        print('Number of data values: {}'.format(len(values)))

        with open(filename, 'w') as f:
            for i in range(0, len(values)-1):
                time_val = x_origin + (i * x_increment)
                voltage = (values[i]) #* y_increment) + y_origin
                f.write('%E, %f\n' % (time_val, voltage))

        print('Waveform format BYTE data written to {}'.format(filename))


if __name__ == '__main__':
    test = SCOPE('192.168.20.165')
    try:
        test.get_spectrum(4,'test.csv')
    except Exception:
        print('Something went wrong...')
    finally:
        test.close()
