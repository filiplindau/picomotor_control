'''
Created on 30 okt 2014

@author: Filip Lindau
'''
import sys
import serial
import socket
import time
import logging
from picomotor_form import Ui_Dialog

logging.basicConfig(level=logging.WARN)

class PicomotorControl(object):
    def __init__(self, address, interface='ethernet'):
        '''Initialize the picomotor control object.
        address: IP address for ethernet OR com port for serial
        interface: ethernet OR serial
        '''
        self.port = address
        self.connected = False
        self.device = None
        self.interface = interface
        self.timeout = 0.3
        self.currentMotor = 0


    def moveMotorRelative(self, steps, motor=-1, driver='a1'):
        '''Move motor a number of steps starting immediately

        steps: number of steps to move
        motor: Motor number (0-2) (default value = -1 reads current motor)
        drive: Driver number (a1-a31)
        '''
        # Some value checking of the driver argument:
        if type(driver) == int:
            driver = ''.join(('a', str(driver)))
        elif type(driver) == str:
            if (driver[0] == 'a' and driver[1:].isdigit()) == False:
                driver = 'a1'
        else:
            driver = 'a1'
        if motor in range(0, 3):
            self.setCurrentMotor(motor, driver)
        cmd = ''.join(('REL ', str(driver), '=', str(steps), ' g'))
        self.sendCommand(cmd)

    def getMotorPositionChange(self, motor=-1, driver='a1'):
        ''' Return motor position in steps

        motor: Motor number (0-2) (default value = -1 reads current motor)
        driver: Driver number (a1-a31)
        '''
        # Some value checking of the driver argument:
        if type(driver) == int:
            driver = ''.join(('a', str(driver)))
        elif type(driver) == str:
            if (driver[0] == 'a' and driver[1:].isdigit()) == False:
                driver = 'a1'
        else:
            driver = 'a1'
        if motor in range(0, 3):
            self.setCurrentMotor(motor, driver)
        cmd = ''.join(('POS ', str(driver)))
        data = self.sendReceiveCommand(cmd)
        try:
            pos = int(data[data.find('=') + 1 : data.find('\r')])
        except ValueError:
            pos = data
        return pos

    def setMotorSpeed(self, speed, motor=-1, driver='a1'):
        '''Set speed in steps/s for motor

        speed: steps/s (1-2000)
        motor: Motor number (0-2) (default value = -1 reads current motor)
        drive: Driver number (a1-a31)
        '''
        # Some value checking of the driver argument:
        if type(driver) == int:
            driver = ''.join(('a', str(driver)))
        elif type(driver) == str:
            if (driver[0] == 'a' and driver[1:].isdigit()) == False:
                driver = 'a1'
        else:
            driver = 'a1'
        if motor not in range(0, 3):
            motor = self.currentMotor
        cmd = ''.join(('VEL ', str(driver), ' ', str(motor), '=', str(speed)))
        self.sendCommand(cmd)

    def getMotorSpeed(self, motor=-1, driver='a1'):
        ''' Return motor speed in steps/s

        motor: Motor number (0-2) (default value = -1 reads current motor)
        driver: Driver number (a1-a31)
        '''
        # Some value checking of the driver argument:
        if type(driver) == int:
            driver = ''.join(('a', str(driver)))
        elif type(driver) == str:
            if (driver[0] == 'a' and driver[1:].isdigit()) == False:
                driver = 'a1'
        else:
            driver = 'a1'
        if motor not in range(0, 3):
            motor = self.currentMotor
        cmd = ''.join(('VEL ', str(driver), ' ', str(motor)))
        data = self.sendReceiveCommand(cmd)
        try:
            vel = int(data[data.find('=') + 1 : data.find('\r')])
        except ValueError:
            vel = data
        return vel

    def stopMotors(self, driver='a1'):
        ''' Immediately stop all motors of driver
        '''
        # Some value checking of the driver argument:
        if type(driver) == int:
            driver = ''.join(('a', str(driver)))
        elif type(driver) == str:
            if (driver[0] == 'a' and driver[1:].isdigit()) == False:
                driver = 'a1'
        else:
            driver = 'a1'
        cmd = ''.join(('STO ', str(driver)))
        self.sendCommand(cmd)

    def haltMotors(self, driver='a1'):
        ''' Smooth stop of motors (deceleration)
        '''
        # Some value checking of the driver argument:
        if type(driver) == int:
            driver = ''.join(('a', str(driver)))
        elif type(driver) == str:
            if (driver[0] == 'a' and driver[1:].isdigit()) == False:
                driver = 'a1'
        else:
            driver = 'a1'
        cmd = ''.join(('HAL ', str(driver)))
        self.sendCommand(cmd)

    def getCurrentMotor(self):
        ''' Returns currently selected motor
        '''

        return self.currentMotor

    def setCurrentMotor(self, motor, driver='a1'):
        ''' Sets currently selected motor. Zeros position counter.

        motor: Motor number (0-2)
        driver: Driver number (a1-a31)
        '''
        # Some value checking of the driver argument:
        if type(driver) == int:
            driver = ''.join(('a', str(driver)))
        elif type(driver) == str:
            if (driver[0] == 'a' and driver[1:].isdigit()) == False:
                driver = 'a1'
        else:
            driver = 'a1'
        if motor in range(0, 3):
            cmd = ''.join(('CHL ', str(driver), '=', str(motor)))
            self.sendCommand(cmd)
            self.currentMotor = motor


    def getStatus(self, driver='a1'):
        ''' Return status byte.

        driver: Driver number (a1-a31)
        '''
        # Some value checking of the driver argument:
        if type(driver) == int:
            driver = ''.join(('a', str(driver)))
        elif type(driver) == str:
            if (driver[0] == 'a' and driver[1:].isdigit()) == False:
                driver = 'a1'
        else:
            driver = 'a1'
        cmd = ''.join(('STA ', str(driver)))
        data = self.sendReceiveCommand(cmd)
        return data

    def getVersion(self):
        ''' Return firmware version
        '''
        cmd = 'VER'
        data = self.sendReceiveCommand(cmd)
        return data[data.find('Version'):data.find('\r')]

    def countAttachedDrivers(self):
        i = 0
        present = True
        cmd = 'DRT'
        data = self.sendReceiveCommand(cmd)
        while ''.join(('A', str(i + 1))) in data:
            i += 1
        return i


    def connect(self):
        '''Establish a connection to the picomotor hardware according to the selected interface.
        First attempts to close the previous connection.
        '''
        if self.interface == 'serial':
            try:
                if self.device != None:
                    self.close()
                self.device = serial.Serial(self.port, baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=self.timeout)
                self.connected = True
            except IOError, e:
                self.device = None
                logging.exception(''.join(('Connect serial: ', str(e))))
                raise
        elif self.interface == 'ethernet':
            try:
                if self.device != None:
                    self.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.port, 23))
                s.settimeout(self.timeout)
                self.device = s
                self.connected = True
            except IOError, e:
                self.device = None
                logging.exception(''.join(('Connect ethernet: ', str(e))))
                raise
        self.getVersion()

    def close(self):
        '''If connected to the hardware, close the connection
        '''
        if self.interface == 'serial':
            if self.device != None:
                if self.device.isOpen() == True:
                    self.device.close()
                    self.connected = False
                    self.device = None
        elif self.interface == 'ethernet':
            if self.device != None:
                if self.connected == True:
                    self.device.close()
                    self.connected = False
                    self.device = None

    def sendReceiveCommand(self, command):
        logging.info('Entering sendReceiveCommand')
        t0 = time.clock()
        if self.device == None:
            logging.info('Device not initialized, connecting')
            self.connect()
        if self.interface == 'serial':
            logging.info('Sending serial message')
            if self.device != None:
                try:
                    if self.device.isOpen() == False:
                        self.device.open()
                    cmd = ''.join((command, '\r\n'))
                    length = 256
                    self.device.write(cmd)
                    t1 = time.clock()
                    logging.info(''.join(('Sending ', command)))
                    logging.info(''.join(('Write time: ', str(t1 - t0), ' s')))
                    data = self.device.readline(length)
                    t2 = time.clock()
                    logging.info(''.join(('Read 1: ', repr(data))))
                    logging.info(''.join(('Read time 1: ', str(t2 - t1), ' s')))
                    data2 = self.device.read(1)
                    t3 = time.clock()
                    logging.info(''.join(('Read 2: ', repr(data2))))
                    data2
                    logging.info(''.join(('Read time 2: ', str(t3 - t2), ' s')))
                    if data2 == '>':
                        logging.info('Command successful')
                    elif data2 == '?':
                        logging.error(''.join(('Error sending command ', str(command), ': ', str(data))))
                        errMsg = self.device.readline(length)
                        logging.error(''.join(('Additional  data read: ', str(errMsg))))
                    else:
                        logging.error(''.join(('Error receiving response: ', str(data2))))
                except serial.SerialTimeoutException, e:
                    logging.exception(''.join(('sendCommand: ', cmd, str(e))))
                    raise
            else:
                logging.exception('Could not connect to device.')
                raise IOError('Could not connect to device.')
        elif self.interface == 'ethernet':
            if self.device != None:
                try:
                    cmd = ''.join((command, '\r\n'))
                    length = 256
                    self.device.send(cmd)

                    try:
                        data = self.device.recv(1)
                    except socket.timeout:
                        data = 'timeout'

                    try:
                        line = self.device.recv(length)
                    except socket.timeout:
                        line = 'Timeout'

                    data += line


                except Exception, e:
                    logging.exception(''.join(('sendCommand: ', cmd, str(e))))
                    raise
            else:
                logging.exception('Could not connect to device.')
                raise IOError('Could not connect to device.')

        return data

    def sendCommand(self, command):
        if self.device == None:
            self.connect()
        if self.interface == 'serial':
            if self.device != None:
                try:
                    if self.device.isOpen() == False:
                        self.device.open()
                    cmd = ''.join((command, '\r\n'))
                    length = 256
                    self.device.write(cmd)
                    data = self.device.readline(length)
                    data2 = self.device.readline(length)
                except serial.SerialTimeoutException, e:
                    logging.exception(''.join(('sendCommand: ', cmd, str(e))))
                    raise
            else:
                logging.exception('Could not connect to device.')
                raise IOError('Could not connect to device.')
        elif self.interface == 'ethernet':
            if self.device != None:
                try:
                    cmd = ''.join((command, '\r\n'))
                    length = 256
                    self.device.send(cmd)

                    try:
                        data = self.device.recv(1)
                    except socket.timeout:
                        data = 'timeout'
                except Exception, e:
                    logging.exception(''.join(('sendCommand: ', cmd, str(e))))
                    raise
            else:
                logging.exception('Could not connect to device.')
                raise IOError('Could not connect to device.')

        return data
