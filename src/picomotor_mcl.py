# -*- coding:utf-8 -*-
"""
Created on 3 mar 2010

@author: Filip
"""
import sys
import socket
import time
from PyQt4 import QtCore, QtGui
from picomotor_form import Ui_Dialog

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
        
        self.picomotor_host = 'fel-motor1'
        self.picomotor_port = 23
        
        self.m1_pos = 0
        self.m2_pos = 0
        
        self.sendCommand('ver')
        self.sendCommand('pos')
        
        self.m1_changeStep()
        self.m2_changeStep()
        
        self.unit = 33333   # Calibration in steps / mm (approximate)
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
        
    def sendCommand(self, command):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# test
        s.connect((self.picomotor_host, self.picomotor_port))
        s.send(''.join([command, '\r\n']))
        data = ''
        s.settimeout(0.3)
        
        try:
            data = s.recv(1)
        except socket.timeout:
            data = 'timeout'
        
        try:
            line = s.recv(256)
        except socket.timeout:
            line = 'Timeout'
            
        data += line
            
        
#        data = s.recv(1024)
#        print data.__len__()
#    
#        while 1:
#            line = ''
#            try:
#                line = s.recv(1024)
#                print line.__len__()
#            except socket.timeout:
#                break
#    
#            if line == '':
#                break
#    
#            data += line

# end-test
    
#        s.settimeout(0.5)
#        try:
#            s.connect((self.picomotor_host,self.picomotor_port))
#            s.send(''.join([command, '\r\n']))
#            data=s.recv(1024)                
#        except:
#            data='Sending failed'

        s.close()
        time.sleep(0.1)
        self.updateStatus(command)
        self.updateStatus(data)
        
        return data
        
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = dlgPicomotor()
    myapp.show()
    sys.exit(app.exec_())
