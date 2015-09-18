'''
Created on 15 aug 2014

@author: Filip
'''
# -*- coding:utf-8 -*-
import sys
import serial
import time
import logging
from PyQt4 import QtCore, QtGui
from picomotor_form import Ui_Dialog

logging.basicConfig(level=logging.DEBUG)

class dlgPicomotor(QtGui.QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(dlgPicomotor, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

#         self.picomotor_host = '128.100.101.204'
#         self.picomotor_port = 23

        self.device = None
        self.port = 'COM11'
        self.closeFlag = False

        self.m1_pos = 0
        self.m2_pos = 0

        self.sendCommand('ver')
        self.sendCommand('pos')

        self.m1_changeStep()
        self.m2_changeStep()

        self.unit = 33333  # Calibration in steps / mm (approximate)
        self.unit = 1
        self.selectUnit()
        self.speedChanged(250)


    def m1_move(self):
        newpos = self.ui.Pos_m1_SpinBox.value()
        relpos = newpos - self.m1_pos
        if abs(relpos) > 0:
            self.sendCommand('chl a1=0')
            string = ''.join(['abs a1=', str(int(self.unit * relpos)), ' g'])
            self.sendCommand(string)

        self.m1_pos = newpos

    def m2_move(self):
        newpos = self.ui.Pos_m2_SpinBox.value()
        relpos = newpos - self.m2_pos
        if abs(relpos) > 0:
            self.sendCommand('chl a1=1')
            string = ''.join(['abs a1=', str(int(self.unit * relpos)), ' g'])
            self.sendCommand(string)

        self.m2_pos = newpos

    def m1_step_right(self):
        relpos = self.ui.Step_m1_SpinBox.value()
        newpos = self.ui.Pos_m1_SpinBox.value() + relpos
        self.sendCommand('chl a1=0')
        string = ''.join(['abs a1=', str(int(self.unit * relpos)), ' g'])
        self.sendCommand(string)

        self.m1_pos = newpos
        self.ui.Pos_m1_SpinBox.setValue(newpos)

    def m1_step_left(self):
        relpos = -self.ui.Step_m1_SpinBox.value()
        newpos = self.ui.Pos_m1_SpinBox.value() + relpos
        self.sendCommand('chl a1=0')
        string = ''.join(['abs a1=', str(int(self.unit * relpos)), ' g'])
        self.sendCommand(string)

        self.m1_pos = newpos
        self.ui.Pos_m1_SpinBox.setValue(newpos)

    def m2_step_right(self):
        relpos = self.ui.Step_m2_SpinBox.value()
        newpos = self.ui.Pos_m2_SpinBox.value() + relpos
        self.sendCommand('chl a1=1')
        string = ''.join(['abs a1=', str(int(self.unit * relpos)), ' g'])
        self.sendCommand(string)

        self.m1_pos = newpos
        self.ui.Pos_m2_SpinBox.setValue(newpos)

    def m2_step_left(self):
        relpos = -self.ui.Step_m2_SpinBox.value()
        newpos = self.ui.Pos_m2_SpinBox.value() + relpos
        self.sendCommand('chl a1=1')
        string = ''.join(['abs a1=', str(int(self.unit * relpos)), ' g'])
        self.sendCommand(string)

        self.m2_pos = newpos
        self.ui.Pos_m2_SpinBox.setValue(newpos)

    def m1_changeStep(self):
        step = self.ui.Step_m1_SpinBox.value()
        self.ui.Pos_m1_SpinBox.setSingleStep(step)

    def m2_changeStep(self):
        step = self.ui.Step_m2_SpinBox.value()
        self.ui.Pos_m2_SpinBox.setSingleStep(step)

    def manual_Command(self):
        command = str(self.ui.manual_Command_lineEdit.text())
        self.sendCommand(command)

    def selectUnit(self):
        if self.ui.radioButtonSteps.isChecked():
            if self.unit != 1:
                self.unit = 1
                self.ui.Step_m1_SpinBox.setValue(self.ui.Step_m1_SpinBox.value() * 33333)
                self.ui.Pos_m1_SpinBox.setValue(self.ui.Pos_m1_SpinBox.value() * 33333)
                self.ui.Step_m1_SpinBox.setSuffix(' steps')
                self.ui.Pos_m1_SpinBox.setSuffix(' steps')
                self.ui.Step_m1_SpinBox.setDecimals(0)
                self.ui.Pos_m1_SpinBox.setDecimals(0)
                self.ui.Step_m1_SpinBox.setSingleStep(10)
                self.ui.Step_m2_SpinBox.setValue(self.ui.Step_m2_SpinBox.value() * 33333)
                self.ui.Pos_m2_SpinBox.setValue(self.ui.Pos_m2_SpinBox.value() * 33333)
                self.ui.Step_m2_SpinBox.setSuffix(' steps')
                self.ui.Pos_m2_SpinBox.setSuffix(' steps')
                self.ui.Step_m2_SpinBox.setDecimals(0)
                self.ui.Pos_m2_SpinBox.setDecimals(0)
                self.ui.Step_m2_SpinBox.setSingleStep(10)
        else:
            if self.unit != 33333:
                self.unit = 33333
                self.ui.Step_m1_SpinBox.setDecimals(4)
                self.ui.Pos_m1_SpinBox.setDecimals(4)
                self.ui.Step_m1_SpinBox.setValue(self.ui.Step_m1_SpinBox.value() / 33333.0)
                self.ui.Pos_m1_SpinBox.setValue(self.ui.Pos_m1_SpinBox.value() / 33333)
                self.ui.Step_m1_SpinBox.setSuffix(' mm')
                self.ui.Pos_m1_SpinBox.setSuffix(' mm')
                self.ui.Step_m1_SpinBox.setSingleStep(0.1)
                self.ui.Step_m2_SpinBox.setDecimals(4)
                self.ui.Pos_m2_SpinBox.setDecimals(4)
                self.ui.Step_m2_SpinBox.setValue(self.ui.Step_m2_SpinBox.value() / 33333.0)
                self.ui.Pos_m2_SpinBox.setValue(self.ui.Pos_m2_SpinBox.value() / 33333)
                self.ui.Step_m2_SpinBox.setSuffix(' mm')
                self.ui.Pos_m2_SpinBox.setSuffix(' mm')
                self.ui.Step_m2_SpinBox.setSingleStep(0.1)
        self.m1_changeStep()
        self.m2_changeStep()

    def stopMotors(self):
        self.sendCommand('stop')

    def speedChanged(self, speed):
        self.speed = self.ui.speedSpinBox.value()
        self.sendCommand('chl a1=1')
        string = ''.join(['vel a1 1=', str(int(self.speed))])
        self.sendCommand(string)
        string = ''.join(['vel a1 2=', str(int(self.speed))])
        self.sendCommand(string)


    def reset_positions(self):
        self.m1_pos = 0
        self.m2_pos = 0
        self.ui.Pos_m1_SpinBox.setValue(0)
        self.ui.Pos_m2_SpinBox.setValue(0)

    def updateStatus(self, statusString):
        self.ui.textEdit.append(statusString)

    def connect(self, port):
        self.port = port
        ptmp = port
        if type(ptmp) == str:
            ptmp = ''.join(('//./', port))
        try:
            if self.device != None:
                self.close()
            self.device = serial.Serial(port, baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.3)
        except IOError, e:
            self.device = None
            logging.exception(''.join(('Connect: ', str(e))))
            raise

    def close(self):
        if self.device != None:
            if self.device.isOpen() == True:
                self.device.close()


    def sendCommand(self, command):

        if self.device == None:
            self.connect(self.port)
        if self.device != None:
            try:
                if self.device.isOpen() == False:
                    self.device.open()
                cmd = ''.join((command, '\r\n'))
                length = 256
                self.device.write(cmd)
                data = self.device.readline(length)
                if self.closeFlag == True:
                    self.device.close()
            except serial.SerialTimeoutException, e:
                logging.exception(''.join(('sendCommand: ', cmd, str(e))))
                raise
        else:
            logging.exception('Could not connect to device.')
            raise IOError('Could not connect to device.')



        time.sleep(0.1)
        self.updateStatus(command)
        self.updateStatus(data)

        return data



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = dlgPicomotor()
    myapp.show()
    sys.exit(app.exec_())
