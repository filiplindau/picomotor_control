'''
Created on 31 okt 2014

@author: Filip Lindau
'''
import sys
import PyTango
import picomotor_control as pc
import threading
import time
import numpy as np
from socket import gethostname
import Queue


class PicomotorCommand:
    def __init__(self, command, data=None):
        self.command = command
        self.data = data

class PicomotorDriver:
    def __init__(self):
        self.pos = [0, 0, 0]
        self.vel = [0, 0, 0]
        self.moving = [False, False, False]

#==================================================================
#   PicomotorDS Class Description:
#
#         Control of a NewFocus (Newport) Picomotor
#
#==================================================================
#     Device States Description:
#
#   DevState.ON :       Connected to picomotor driver
#   DevState.OFF :      Disconnected from picomotor
#   DevState.FAULT :    Error detected
#   DevState.UNKNOWN :  Communication problem
#   DevState.MOVING :  Motor moving
#   DevState.INIT :     Initializing picomotor driver.
#==================================================================


class PicomotorDS(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------

#------------------------------------------------------------------
#     Device constructor
#------------------------------------------------------------------
    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self, cl, name)
        PicomotorDS.init_device(self)

#------------------------------------------------------------------
#     Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        with self.streamLock:
            self.info_stream(''.join(("[Device delete_device method] for device", self.get_name())))
        self.stopThread()


#------------------------------------------------------------------
#     Device initialization
#------------------------------------------------------------------
    def init_device(self):
        self.streamLock = threading.Lock()
        with self.streamLock:
            self.info_stream(''.join(("In ", self.get_name(), "::init_device()")))
        self.set_state(PyTango.DevState.UNKNOWN)
        self.get_device_properties(self.get_device_class())

        # Try stopping the stateThread if it was started before. We fail if this
        # is the initial start.
        try:
            self.stopThread()

        except Exception, e:
            pass

        self.attrLock = threading.Lock()
        self.eventIdList = []
        self.stateThread = threading.Thread()
        threading.Thread.__init__(self.stateThread, target=self.stateHandlerDispatcher)

        self.commandQueue = Queue.Queue(100)

        self.stateHandlerDict = {PyTango.DevState.ON: self.onHandler,
                                PyTango.DevState.MOVING: self.onHandler,
                                PyTango.DevState.ALARM: self.onHandler,
                                PyTango.DevState.FAULT: self.faultHandler,
                                PyTango.DevState.INIT: self.initHandler,
                                PyTango.DevState.UNKNOWN: self.unknownHandler,
                                PyTango.DevState.OFF: self.offHandler}

        self.stopStateThreadFlag = False

        self.stateThread.start()


    def stateHandlerDispatcher(self):
        """Handles switch of states in the state machine thread.
        Each state handled method should exit by setting the next state,
        going back to this method. The previous state is also included when
        calling the next state handler method.
        The thread is stopped by setting the stopStateThreadFlag.
        """
        prevState = self.get_state()
        while self.stopStateThreadFlag == False:
            try:
                self.stateHandlerDict[self.get_state()](prevState)
                prevState = self.get_state()
            except KeyError:
                self.stateHandlerDict[PyTango.DevState.UNKNOWN](prevState)
                prevState = self.get_state()

    def stopThread(self):
        """Stops the state handler thread by setting the stopStateThreadFlag
        """
        self.stopStateThreadFlag = True
        self.stateThread.join(3)
        self.picomotorDevice.close()
#        self.unsubscribeEvents()


    def unknownHandler(self, prevState):
        """Handles the UNKNOWN state, before communication with the master device
        has been established. Tries to create a deviceproxy object.
        """
        with self.streamLock:
            self.info_stream('Entering unknownHandler')
        connectionTimeout = 1.0

        self.motorDriverDict = {}
        self.currentMotor = 0
        self.startMovePosition = 0

        while self.stopStateThreadFlag == False:
#            self.unsubscribeEvents()
            try:
                self.picomotorDevice = pc.PicomotorControl(self.address, self.interface)
            except Exception, e:
                with self.streamLock:
                    self.error_stream(''.join(('Could not create picomotor device ', self.address, self.interface)))
                with self.streamLock:
                    self.error_stream(str(e))
                self.checkCommands(blockTime=connectionTimeout)
                continue
            self.set_state(PyTango.DevState.INIT)
            break

    def initHandler(self, prevState):
        """Handles the INIT state. Query picomotor device to see if it is alive.
        """
        with self.streamLock:
            self.info_stream('Entering initHandler')
        waitTime = 1.0

        while self.stopStateThreadFlag == False:
            try:
                with self.streamLock:
                    self.info_stream('Trying to connect...')
                self.picomotorDevice.connect()
                # Check how many driver are connected to the controller:
                with self.streamLock:
                    self.debug_stream('Connected')
                with self.attrLock:
                    drivers = self.picomotorDevice.countAttachedDrivers()
                # Populate the list of drivers with motors:
                with self.streamLock:
                    self.debug_stream(''.join(('Found ', str(drivers), ' drivers')))
                for d in range(drivers):
                    pd = PicomotorDriver()
                    self.debug_stream(''.join(('Driver ', str(d), ' created')))
                    with self.attrLock:
                        pd.pos[0] = 0
                        pd.pos[1] = 0
                        pd.pos[2] = 0
                        self.debug_stream(''.join(('Driver ', str(d), ' positions read')))
                        pd.vel[0] = self.picomotorDevice.getMotorSpeed(0, d + 1)
                        pd.vel[1] = self.picomotorDevice.getMotorSpeed(1, d + 1)
                        pd.vel[2] = self.picomotorDevice.getMotorSpeed(2, d + 1)
                        self.debug_stream(''.join(('Driver ', str(d), ' speeds read')))
                        self.debug_stream(''.join(('Driver ', str(d), ' added')))
                        drName = ''.join(('a', str(d + 1)))
                        self.debug_stream(str(self.motorDriverDict.has_key(drName)))
                    # Add dynamic attribute creation here...
                        if self.motorDriverDict.has_key(drName) == False:
                            self.info_stream(''.join(('Adding picomotor driver ', drName, ' to list.')))
                            self.motorDriverDict[drName] = pd

                            attrInfo = [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ_WRITE],
                                {
                                    'description':"Motor position in steps",
                                    'Memorized':"false",
                                    'unit': "steps"
                                } ]
                            attrName = ''.join(('MotorPosition0A', str(d + 1)))
                            attrData = PyTango.AttrData(attrName, self.get_name(), attrInfo)
                            self.add_attribute(attrData, r_meth=self.read_MotorPosition, w_meth=self.write_MotorPosition, is_allo_meth=self.is_MotorPosition_allowed)

                            attrInfo = [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ_WRITE],
                                {
                                    'description':"Motor position in steps",
                                    'Memorized':"false",
                                    'unit': "steps"
                                } ]
                            attrName = ''.join(('MotorPosition1A', str(d + 1)))
                            attrData = PyTango.AttrData(attrName, self.get_name(), attrInfo)
                            self.add_attribute(attrData, r_meth=self.read_MotorPosition, w_meth=self.write_MotorPosition, is_allo_meth=self.is_MotorPosition_allowed)

                            attrInfo = [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ_WRITE],
                                {
                                    'description':"Motor position in steps",
                                    'Memorized':"false",
                                    'unit': "steps"
                                } ]
                            attrName = ''.join(('MotorPosition2A', str(d + 1)))
                            attrData = PyTango.AttrData(attrName, self.get_name(), attrInfo)
                            self.add_attribute(attrData, r_meth=self.read_MotorPosition, w_meth=self.write_MotorPosition, is_allo_meth=self.is_MotorPosition_allowed)

                            attrInfo = [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ_WRITE],
                                {
                                    'description':"Motor speed in steps/s",
                                    'Memorized':"false",
                                    'unit': "steps/s"
                                } ]
                            attrName = ''.join(('MotorSpeed0A', str(d + 1)))
                            attrData = PyTango.AttrData(attrName, self.get_name(), attrInfo)
                            self.add_attribute(attrData, r_meth=self.read_MotorSpeed, w_meth=self.write_MotorPosition, is_allo_meth=self.is_MotorSpeed_allowed)

                            attrInfo = [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ_WRITE],
                                {
                                    'description':"Motor speed in steps/s",
                                    'Memorized':"false",
                                    'unit': "steps/s"
                                } ]
                            attrName = ''.join(('MotorSpeed1A', str(d + 1)))
                            attrData = PyTango.AttrData(attrName, self.get_name(), attrInfo)
                            self.add_attribute(attrData, r_meth=self.read_MotorSpeed, w_meth=self.write_MotorPosition, is_allo_meth=self.is_MotorSpeed_allowed)

                            attrInfo = [[PyTango.DevDouble, PyTango.SCALAR, PyTango.READ_WRITE],
                                {
                                    'description':"Motor speed in steps/s",
                                    'Memorized':"false",
                                    'unit': "steps/s"
                                } ]
                            attrName = ''.join(('MotorSpeed2A', str(d + 1)))
                            attrData = PyTango.AttrData(attrName, self.get_name(), attrInfo)
                            self.add_attribute(attrData, r_meth=self.read_MotorSpeed, w_meth=self.write_MotorPosition, is_allo_meth=self.is_MotorSpeed_allowed)

                            

            except Exception, e:
                with self.streamLock:
                    self.error_stream(''.join(('Error when initializing device')))
                    self.error_stream(str(e))
                self.checkCommands(blockTime=waitTime)
                continue

            self.set_state(PyTango.DevState.ON)
            break

    def onHandler(self, prevState):
        """Handles the ON state. Connected to the picomotor driver.
        Waits in a loop checking commands.
        """
        with self.streamLock:
            self.info_stream('Entering onHandler')
        handledStates = [PyTango.DevState.ON, PyTango.DevState.ALARM, PyTango.DevState.MOVING]
        waitTime = 0.1

#        self.eventThread.start()

        nDrivers = self.motorDriverDict.__len__()
        nMotors = 3
        driver = 1
        motor = 0

        while self.stopStateThreadFlag == False:
            with self.attrLock:
                state = self.get_state()
            if state not in handledStates:
                break
            with self.attrLock:
                # Read position and speed of all motors in a sequentially when the queue is empty
                if self.commandQueue.empty() == True:
                    motor += 1
                    if motor >= nMotors:
                        motor = 0
                        driver += 1
                        if driver > nDrivers:
                            driver = 1
                    drName = ''.join(('a', str(driver)))
                    data = (drName, motor)
                    cmdMsg = PicomotorCommand('readMotorSpeed', data)
                    self.commandQueue.put(cmdMsg)
#                     data = (drName, self.currentMotor)
#                     cmdMsg = PicomotorCommand('readMotorPosition', data)
#                     self.commandQueue.put(cmdMsg)
            self.checkCommands(blockTime=waitTime)


    def faultHandler(self, prevState):
        """Handles the FAULT state. A problem has been detected.
        """
        with self.streamLock:
            self.info_stream('Entering faultHandler')
        handledStates = [PyTango.DevState.FAULT]
        waitTime = 0.1

        while self.stopStateThreadFlag == False:
            if self.get_state() not in handledStates:
                break
            self.checkCommands(blockTime=waitTime)

    def offHandler(self, prevState):
        """Handles the OFF state. Does nothing, just goes back to ON.
        """
        with self.streamLock:
            self.info_stream('Entering offHandler')
        self.set_state(PyTango.DevState.ON)



    def checkCommands(self, blockTime=0):
        """Checks the commandQueue for new commands. Must be called regularly.
        If the queue is empty the method exits immediately.
        """
#         with self.streamLock:
#             self.debug_stream('Entering checkCommands')
        try:
            if blockTime == 0:
#                 with self.streamLock:
#                     self.debug_stream('checkCommands: blockTime == 0')
                cmd = self.commandQueue.get(block=False)
            else:
#                 with self.streamLock:
#                     self.debug_stream('checkCommands: blockTime != 0')
                cmd = self.commandQueue.get(block=True, timeout=blockTime)
#             with self.streamLock:
#                 self.info_stream(str(cmd.command))
            if cmd.command == 'writeMotorPosition':
                with self.attrLock:
                    driver = (cmd.data[0]).lower()
                    motor = cmd.data[1]
                    steps = cmd.data[2] - self.motorDriverDict[driver].pos[motor]
                    if motor != self.currentMotor:
                        self.picomotorDevice.setCurrentMotor(motor, driver)
#                        self.currentMotor = motor
                    self.picomotorDevice.moveMotorRelative(steps, -1, driver)
                    self.motorDriverDict[driver].pos[motor] += steps
#                    self.motorDriverDict[driver].pos[motor] = cmd.data[2]
            elif cmd.command == 'moveCurrentMotorRelative':
                with self.attrLock:
                    driver = 'a1'
                    motor = self.currentMotor
                    steps = cmd.data
                    self.picomotorDevice.setCurrentMotor(motor, driver)
                    self.picomotorDevice.moveMotorRelative(steps, -1, driver)
                    self.motorDriverDict[driver].pos[motor] += steps
            elif cmd.command == 'readMotorPosition':
                with self.attrLock:
                    driver = (cmd.data[0]).lower()
                    motor = cmd.data[1]
                    if motor != self.currentMotor:
                        self.picomotorDevice.setCurrentMotor(motor, driver)
#                        self.currentMotor = motor
                    readPos = self.picomotorDevice.getMotorPositionChange(-1, driver)
                    self.motorDriverDict[driver].pos[motor] = readPos
                    with self.streamLock:
                        self.info_stream(''.join((str(cmd.command), ': ', str(driver), ' motor ', str(motor), ' = ', str(readPos))))
            elif cmd.command == 'writeMotorSpeed':
                with self.attrLock:
                    driver = (cmd.data[0]).lower()
                    motor = cmd.data[1]
                    speed = cmd.data[2]
                    self.picomotorDevice.setMotorSpeed(speed, motor, driver)
            elif cmd.command == 'readMotorSpeed':
                with self.attrLock:
                    driver = (cmd.data[0]).lower()
                    motor = cmd.data[1]
                    self.motorDriverDict[driver].vel[motor] = self.picomotorDevice.getMotorSpeed(motor, driver)

#             elif cmd.command == 'on' or cmd.command == 'start':
#                 if self.get_state() not in [PyTango.DevState.INIT, PyTango.DevState.UNKNOWN]:
#                     self.masterDevice.command_inout('StartSpectrometer', self.Serial)

            elif cmd.command == 'stop' or cmd.command == 'standby':
                if self.get_state() not in [PyTango.DevState.INIT, PyTango.DevState.UNKNOWN]:
                    with self.attrLock:
                        for i, dr in enumerate(self.motorDrivers):
                            self.picomotorDevice.stopMotors(i + 1)

            elif cmd.command == 'off':
                if self.get_state() not in [PyTango.DevState.INIT, PyTango.DevState.UNKNOWN]:
                    self.setState(PyTango.DevState.OFF)

            elif cmd.command == 'init':
                if self.get_state() not in [PyTango.DevState.UNKNOWN]:
                    self.setState(PyTango.DevState.UNKNOWN)

        except Queue.Empty:
#             with self.streamLock:
#                 self.debug_stream('checkCommands: queue empty')

            pass

#------------------------------------------------------------------
#     Always excuted hook method
#------------------------------------------------------------------
    def always_executed_hook(self):
        pass

#------------------------------------------------------------------
#     CurrentMotor attribute
#------------------------------------------------------------------
    def read_CurrentMotor(self, attr):
        with self.streamLock:
            self.info_stream(''.join(('Reading current motor')))
        with self.attrLock:
            attr_read = self.currentMotor
            if attr_read == None:
                attr.set_quality(PyTango.AttrQuality.ATTR_INVALID)
                attr_read = 0.0
            attr.set_value(attr_read)

    def write_CurrentMotor(self, attr):
        with self.streamLock:
            self.info_stream(''.join(('Writing current motor')))
        data = (attr.get_write_value())
        cmdMsg = PicomotorCommand('writeCurrentMotor', data)
        self.commandQueue.put(cmdMsg)

    def is_CurrentMotor_allowed(self, req_type):
        if self.get_state() in []:
            #     End of Generated Code
            #     Re-Start of Generated Code
            return False
        return True


#------------------------------------------------------------------
#     MotorPosition attribute
#------------------------------------------------------------------
    def read_MotorPosition(self, attr):
        with self.streamLock:
            self.info_stream(''.join(('Reading motor position for ', attr.get_name())))
        motor = int(attr.get_name().rsplit('MotorPosition')[1][0])
        driver = attr.get_name().rsplit('MotorPosition')[1][1:]
        with self.streamLock:
            self.info_stream(''.join(('Driver ', str(driver), ', motor ', str(motor))))
        with self.attrLock:
            attr_read = self.motorDriverDict[driver.lower()].pos[motor]
            if attr_read == None:
                attr.set_quality(PyTango.AttrQuality.ATTR_INVALID)
                attr_read = 0.0
            attr.set_value(attr_read)

    def write_MotorPosition(self, attr):
        self.info_stream(''.join(('Writing motor position for ', attr.get_name())))
        motor = int(attr.get_name().rsplit('MotorPosition')[1][0])
        driver = attr.get_name().rsplit('MotorPosition')[1][1:]
        data = (driver, motor, attr.get_write_value())
        cmdMsg = PicomotorCommand('writeMotorPosition', data)
        self.commandQueue.put(cmdMsg)

    def is_MotorPosition_allowed(self, req_type):
        if self.get_state() in [PyTango.DevState.INIT,
                                PyTango.DevState.UNKNOWN]:
            #     End of Generated Code
            #     Re-Start of Generated Code
            return False
        return True

#------------------------------------------------------------------
#     MotorSpeedattribute
#------------------------------------------------------------------
    def read_MotorSpeed(self, attr):
        with self.streamLock:
            self.info_stream(''.join(('Reading motor speed for ', attr.get_name())))
        motor = int(attr.get_name().rsplit('MotorSpeed')[1][0])
        driver = attr.get_name().rsplit('MotorSpeed')[1][1:]
        with self.attrLock:
            attr_read = self.motorDriverDict[driver.lower()].vel[motor]
            if attr_read == None:
                attr.set_quality(PyTango.AttrQuality.ATTR_INVALID)
                attr_read = 0.0
            attr.set_value(attr_read)

    def write_MotorSpeed(self, attr):
        self.info_stream(''.join(('Writing motor speed for ', attr.get_name())))
        motor = int(attr.get_name().rsplit('MotorSpeed')[1][0])
        driver = attr.get_name().rsplit('MotorSpeed')[1][1:]
        data = (driver, motor, attr.get_write_value())
        cmdMsg = PicomotorCommand('writeMotorSpeed', data)
        self.commandQueue.put(cmdMsg)

    def is_MotorSpeed_allowed(self, req_type):
        if self.get_state() in [PyTango.DevState.INIT,
                                PyTango.DevState.UNKNOWN]:
            #     End of Generated Code
            #     Re-Start of Generated Code
            return False
        return True

#==================================================================
#
#     PicomotorDS command methods
#
#==================================================================

#------------------------------------------------------------------
#     On command:
#
#     Description: Start picomotor driver
#
#------------------------------------------------------------------
    def On(self):
        with self.streamLock:
            self.info_stream(''.join(("In ", self.get_name(), "::On")))
        cmdMsg = PicomotorCommand('on')
        self.commandQueue.put(cmdMsg)

#---- On command State Machine -----------------
    def is_On_allowed(self):
        if self.get_state() in [PyTango.DevState.UNKNOWN]:
            #     End of Generated Code
            #     Re-Start of Generated Code
            return False
        return True

#------------------------------------------------------------------
#     Stop command:
#
#     Description: Stop movement of all motors
#
#------------------------------------------------------------------
    def Stop(self):
        with self.streamLock:
            self.info_stream(''.join(("In ", self.get_name(), "::Stop")))
        cmdMsg = PicomotorCommand('stop')
        self.commandQueue.put(cmdMsg)

#---- Stop command State Machine -----------------
    def is_Stop_allowed(self):
        if self.get_state() in [PyTango.DevState.UNKNOWN]:
            #     End of Generated Code
            #     Re-Start of Generated Code
            return False
        return True

#------------------------------------------------------------------
#     MoveCurrentMotorRelative command:
#
#     Description: Move the currently selected motor a number of steps relative to current position
#
#------------------------------------------------------------------
    def MoveCurrentMotorRelative(self, steps):
        with self.streamLock:
            self.info_stream(''.join(("In ", self.get_name(), "::MoveCurrentMotorRelative")))
        data = (steps)
        cmdMsg = PicomotorCommand('moveCurrentMotorRelative', data)
        self.commandQueue.put(cmdMsg)

#---- MoveCurrentMotorRelative command State Machine -----------------
    def is_MoveCurrentMotorRelative_allowed(self):
        if self.get_state() in [PyTango.DevState.UNKNOWN]:
            #     End of Generated Code
            #     Re-Start of Generated Code
            return False
        return True

#==================================================================
#
#     PicomotorDSClass class definition
#
#==================================================================
class PicomotorDSClass(PyTango.DeviceClass):

    #     Class Properties
    class_property_list = {
        }


    #     Device Properties
    device_property_list = {
        'address':
            [PyTango.DevString,
            "Address of the picomotor device (IP address or com port",
            [ '128.100.101.204' ] ],
        'interface':
            [PyTango.DevString,
            "Type of interface used (ethernet or serial)",
            [ 'ethernet' ] ],
        }


    #     Command definitions
    cmd_list = {
        'On':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVoid, ""]],
        'Stop':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVoid, ""]],
        'MoveCurrentMotorRelative':
            [[PyTango.DevLong, "Number of steps to move (negative for backwards motion)"],
            [PyTango.DevVoid, ""]],
                
        }


    #     Attribute definitions
    attr_list = {
        'CurrentMotor':
            [[PyTango.DevLong,
              PyTango.SCALAR,
              PyTango.READ_WRITE],
                    {
                        'description':"Currently selected motor",
                        'Memorized':"true",
                        'unit': '',
                    } ],
#         'MotorPosition':
#             [[PyTango.DevDouble,
#               PyTango.SCALAR,
#               PyTango.READ_WRITE],
#                     {
#                         'description':"Motor position in steps",
#                         'Memorized':"false",
#                         'unit': 'steps',
#                     } ],
#         'MotorSpeed':
#             [[PyTango.DevDouble,
#               PyTango.SCALAR,
#               PyTango.READ_WRITE],
#                     {
#                         'description':"Motor speed in steps / s",
#                         'Memorized':"false",
#                         'unit': 'steps/s',
#                     } ],

        }


#------------------------------------------------------------------
#     PicomotorDSClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name);
        print "In PicomotorDSClass  constructor"

#==================================================================
#
#     PicomotorDS class main method
#
#==================================================================
if __name__ == '__main__':
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(PicomotorDSClass, PicomotorDS, 'PicomotorDS')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed, e:
        print '-------> Received a DevFailed exception:', e
    except Exception, e:
        print '-------> An unforeseen exception occured....', e
