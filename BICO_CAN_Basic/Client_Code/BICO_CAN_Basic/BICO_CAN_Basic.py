import sys, os
module_path = os.path.abspath(os.path.join(os.getcwd(),"../../../Common/Template_Material"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"../../Template_Material"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Data_Object"))
sys.path.append(module_path)
current_path = os.getcwd()

from PySide6.QtGui import QGuiApplication

from bico_qmessdata import Bico_QMessData
from bico_qmutexqueue import Bico_QMutexQueue
from bico_quithread import Bico_QUIThread
from Example_Data_Object import Example_Data_Object
import json
import can
from datetime import datetime
import serial.tools.list_ports


class BICO_CAN_Basic(Bico_QUIThread):
    i = 0
    ex_data_obj = Example_Data_Object()
    
    bus = None
    init_done = False
    current_ports = None
    
    def getComPorts(self):
        return [port.device for port in serial.tools.list_ports.comports()]
    
    def nofityUIComPortsUpdate(self):
        new_ports = self.getComPorts()
        if new_ports != self.current_ports:
            self.current_ports = new_ports
            self.toUI.emit("com_port_list", self.current_ports)
            
    def generateCanLog(self, can_msg):
        hex_string = '   '.join(f'{byte:02X}' for byte in can_msg.data)
        can_log = f'{datetime.now()}\t{hex(can_msg.arbitration_id).ljust(10, " ").upper()[2:]}    {can_msg.dlc}\t{hex_string.upper()}'
        return can_log
    
    
    def MainTask(self):
        if (self.init_done == False):
            self.nofityUIComPortsUpdate()
            self.init_done = True
            
        continue_to_run = 1
        
        i = 0
        input, result = self.qinDequeue()

        if result:
            mess = input.mess()
            data = input.data()
            if (mess == "terminate"):            
                continue_to_run = 0
                
            elif (mess == "Connect"):
                try:
                    json_data = json.loads(data)
                    print(self.objectName() + " " + mess + ": ")
                    # print(data)
                    print(f'serial_port: {json_data["serial_port"]}')
                    print(f'can_baudrate: {json_data["can_baudrate"]}')
                    self.bus = can.Bus(interface="serial", channel=json_data["serial_port"])
                except:
                    print("Error, but I don't know what it is >_<")
                finally:
                    pass
                
            elif (mess == "Disconnect"):
                try:
                    json_data = json.loads(data)
                    print(self.objectName() + " " + mess + ": ")
                    # print(data)
                    print(f'serial_port: {json_data["serial_port"]}')
                    print(f'can_baudrate: {json_data["can_baudrate"]}')
                    if (self.bus != None):
                        self.bus.shutdown()
                        print(f'BUS: {self.bus}')
                        self.bus = None
                except:
                    print("Error, but I don't know what it is >_<")
                finally:
                    pass
                    
            elif (mess == "Send"):
                try:
                    json_data = json.loads(data)
                    # print(self.objectName() + " " + mess + ": ")
                    # print(data)
                    # print(f'can_id: {json_data["can_id"]}')
                    # print(f'can_data: {json_data["can_data"]}')
                    hex_string = str(json_data["can_data"]).replace(" ", "")
                    hex_list = []
                    for i in range(0, len(hex_string), 2):
                        hex_value = int(hex_string[i:i+2], 16)  # Convert each pair to hex
                        hex_list.append(hex_value)
                    tx_msg = can.Message(
                                arbitration_id=int(json_data["can_id"], 16),
                                data=hex_list,
                            )
                    if self.bus != None:
                        self.bus.send(tx_msg)
                        can_log = self.generateCanLog(tx_msg)
                        self.toUI.emit("can_log", can_log)
                except:
                    print("Error, but I don't know what it is >_<")
                finally:
                    pass
                
                
            elif (mess == "com_port_list_update"):
                self.nofityUIComPortsUpdate()
                
                
            elif (mess == "text"):
                print(self.objectName() + " " + mess + " " + data)
                self.toUI.emit(mess, data)
                
            elif (mess == "size"):
                print(self.objectName() + " " + mess + " " + str(data.width()) + str(data.height()))
                self.toUI.emit(mess, data)
                
            elif (mess == "from_another_thread"):
                print(self.objectName() + " " + mess + ": "  + input.src() + " - " + str(data))

        # print("Hello from " + self.objectName())
        # print("Num of running thread: " + str(len(Bico_QUIThread.getThreadHash())))
        # self.msleep(10)

        try: 
            if (self.bus != None):
                rx_msg = self.bus.recv(0.01)
                if rx_msg is not None:
                    # if (rx_msg.arbitration_id == 0x18DA10F1) or (rx_msg.arbitration_id == 0x18DAF110):
                    if (True):
                        can_log = self.generateCanLog(rx_msg)
                        self.toUI.emit("can_log", can_log)
        except:
            print("Error, but I don't know what it is >_<")
        finally:
            pass
    
        return continue_to_run
















if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    Bico_QUIThread.setMainApp(app)

    Bico_QUIThread.create(
        BICO_CAN_Basic(Bico_QMutexQueue(), 1, Bico_QMutexQueue(), 1, "task_0", os.path.join(current_path, "", "BICO_CAN_Basic.qml"))
    )
    Bico_QUIThread.getThreadHash()["task_0"].start()

    Bico_QUIThread.create(
        BICO_CAN_Basic(Bico_QMutexQueue(), 1, Bico_QMutexQueue(), 1, "task_1", os.path.join(current_path, "", "BICO_CAN_Basic.qml"))
    )
    Bico_QUIThread.getThreadHash()["task_1"].start()

    sys.exit(app.exec())
