from dmm import DMM
from datetime import datetime
import time
from os import path


def main():

    TCPIP = "" #device adress.
    dmm = DMM(TCPIP)
    dmm_samples = 1
    time_format = '%Y%m%d_%H%M%S'
    #configure dmm
    acdc = 'DC'
    range = '100'
    resolution = 0.01
    dmm.conf_volt(acdc,range,resolution)
    dmm.set_trigger(dmm_samples)
    cycle = 0
    log_file = 'dmm_log.csv'

    if path.exists(log_file):
        pass

    else:

        with open('dmm_log.csv','w') as f:
            write_string = 'Date;'+';'.join(['data'+str(x) for x in range(dmm_samples)])
            f.write(write_string+'\n')

    print('Starting test')
    try:
        while True:
            time = datetime.now()
            time = time.strftime(time_format)
            print('Reading voltages')
            volt = dmm.read()
            dmm_data = ';'.join([str(v) for v in volt])
            write_line = time+';'+dmm_data

            with open(loggFile,'a') as f:
                f.write(write_line+'\n')

            print('Just finnished cycle {}, sleeping'.format(cycle))
            time.sleep(10)
    except KeyboardInterrupt:
        print('Experiment finnished.')

if __name__ == '__main__':
    main()
