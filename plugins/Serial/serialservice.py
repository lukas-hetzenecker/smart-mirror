import asyncio
import serial_asyncio
import serial

from PySide2.QtCore import Property, Signal, Slot, QObject


class SerialService(QObject):

    deviceChanged = Signal(str)
    displayOn = Signal()
    displayOff = Signal()
    displayStandby = Signal()
    movementDetected = Signal()
    movementEnded = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._device = None
        self._transport = None

    def getDevice(self):
        return self._device

    def setDevice(self, device):
        self._device = device
        self.deviceChanged.emit(device)

    device = Property(str, getDevice, setDevice, notify=deviceChanged)

    @Slot()
    def open(self):
        class Connection(asyncio.Protocol, QObject):
            dataReceived = Signal(str)

            def __init__(self, parent=None):
                asyncio.Protocol.__init__(self)
                QObject.__init__(self, parent)
                self._transport = None

            def connection_made(self, transport):
                self._transport = transport
                print('port opened', self._transport)

            def data_received(self, data):
                data = data.strip().decode('ascii')
                print('data received', repr(data))
                self.dataReceived.emit(data)

            def connection_lost(self, exc):
                print('port closed')
                self._transport.loop.stop()

        if self._device is None:
            return False

        print("Opening device: " + self._device)
        loop = asyncio.get_event_loop()
        coro = serial_asyncio.create_serial_connection(loop, Connection, self._device, baudrate=9600)
        try:
            self._transport, protocol = loop.run_until_complete(coro)
            protocol.dataReceived.connect(self._handle_data)
        except serial.SerialException as e:
            print(e)

    def _write(self, cmd):
        if not self._transport:
            return False

        try:
            self._transport.write(cmd + b'\r\n')
        except serial.SerialException as e:
            print(e)

    @Slot(str)
    def _handle_data(self, data):
        if data == 'PIR ON':
            self.movementDetected.emit()
        elif data == 'PIR OFF':
            self.movementEnded.emit()
        elif data == 'DISP ON':
            self.displayOn.emit()
        elif data == 'DISP OFF':
            self.displayOff.emit()


    @Slot()
    def turnDisplayOn(self):
        self._write(b'ON')

    @Slot()
    def turnDisplayOff(self):
        self._write(b'OFF')

    @Slot()
    def pressPowerButton(self):
        self._write(b'PWR')

    @Slot()
    def pressVolumeUpButton(self):
        self._write(b'VOL+')

    @Slot()
    def pressVolumeDownButton(self):
        self._write(b'VOL-')

    @Slot()
    def pressAutoButton(self):
        self._write(b'AUTO')

    @Slot()
    def pressMenuButton(self):
        self._write(b'MENU')

    @Slot()
    def pressExitButton(self):
        self._write(b'EXIT')
