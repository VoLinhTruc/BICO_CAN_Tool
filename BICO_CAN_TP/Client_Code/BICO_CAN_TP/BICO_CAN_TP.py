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
import isotp
from typing import Optional
import threading


class BICO_CAN_TP(Bico_QUIThread):
    i = 0
    ex_data_obj = Example_Data_Object()
    
    bus = None
    addr = None
    params = {
    'blocking_send' : True,
    'tx_padding': 0xFF
    }
    tp_layer = None
    
    init_done = False
    current_ports = None
    
    # List all running threads
    threads = threading.enumerate()
    
    def getComPorts(self):
        return [port.device for port in serial.tools.list_ports.comports()]
    
    def nofityUIComPortsUpdate(self):
        new_ports = self.getComPorts()
        if new_ports != self.current_ports:
            self.current_ports = new_ports
            self.toUI.emit("com_port_list", self.current_ports)
            
    def generateCanLog(self, can_id, is_29bits, can_msg):
        dlc = len(can_msg)
        hex_string = ""
        can_id_as_hex_str = hex(can_id)[2:].upper()
        if (is_29bits == True):
            can_id_as_hex_str = can_id_as_hex_str + "x"
        for i in range(0, dlc):
            if (i != 0) and ((i % 8) == 0):
                hex_string = hex_string + '\n'
                hex_string = hex_string + ''.ljust(40, " ")
                hex_string = hex_string + f'[{i}]'.ljust(10, " ")
                hex_string = hex_string + f"{can_msg[i]:02X}"
            else:
                hex_string = hex_string + '   ' + f"{can_msg[i]:02X}"
        can_log = f'{str(datetime.now()).ljust(29, " ")}{can_id_as_hex_str.ljust(11, " ")}{str(dlc).ljust(7, " ")}{hex_string.upper()}'
        return can_log
    
    
    def my_error_handler(self, error):
        # Called from a different thread, needs to be thread safe
        print('IsoTp error happened : %s - %s' % (error.__class__.__name__, str(error)))


    # def my_rxfn(self, timeout:float) -> Optional[isotp.CanMessage]:
    #     # All my_hardware_something and get_something() function are fictive of course.
    #     msg = self.bus.recv(0.01) # Blocking read are encouraged for better timing.
    #     if msg is None:
    #         return None # Return None if no message available
    #     if msg.arbitration_id <= 0x7FF:
    #         msg.arbitration_id &= 0x7FF
    #         msg.is_extended_id = False
    #     else:
    #         msg.is_extended_id = True
    #     print(f'{msg}')
    #     return isotp.CanMessage(arbitration_id=msg.arbitration_id, data=msg.data, dlc=msg.dlc, extended_id=msg.is_extended_id)
    
    def my_rxfn(self, timeout:float) -> Optional[isotp.CanMessage]:
        ret = isotp.CanMessage()
        try:
            # All my_hardware_something and get_something() function are fictive of course.
            msg = self.bus.recv(0.01) # Blocking read are encouraged for better timing.
            if msg is not None:
                print(f'{msg}')
                ret = isotp.CanMessage(arbitration_id=msg.arbitration_id, data=msg.data, dlc=msg.dlc, extended_id=msg.is_extended_id)
        except:
            print("Error, but I don't know what it is >_<")
        finally:
            return ret


    def my_txfn(self, isotp_msg:isotp.CanMessage):
        try:
            # all set_something functions and my_hardware_something are fictive.
            msg = can.Message()
            msg.arbitration_id = isotp_msg.arbitration_id
            msg.data = (isotp_msg.data)
            msg.dlc = (isotp_msg.dlc)
            msg.is_rx = False
            msg.is_extended_id = (isotp_msg.is_extended_id)
            self.bus.send(msg)
            print(f'{msg}')
        except:
            print("Error, but I don't know what it is >_<")
        finally:
            pass
    
    
    
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
                try:
                    print("terminate")
                    if (self.tp_layer != None):
                        self.tp_layer.stop()
                        self.tp_layer = None
                        print("terminate tp_layer")
                    if (self.bus != None):
                        self.bus.shutdown()
                        self.bus = None        
                        print("terminate bus")
                except:
                    print("Error, but I don't know what it is >_<")
                finally:
                    pass
                continue_to_run = 0
                
            elif (mess == "Connect"):
                try:
                    json_data = json.loads(data)
                    if (json_data["serial_port"] != "") and (json_data["serial_port"] != None):
                        print(self.objectName() + " " + mess + ": ")
                        # print(data)
                        print(f'serial_port: {json_data["serial_port"]}')
                        print(f'can_baudrate: {json_data["can_baudrate"]}')
                        print(f'rxid: {json_data["rxid"]}')
                        print(f'txid: {json_data["txid"]}')
                        rxid = 0
                        txid = 0
                        address_mode = None
                        filters = []
                        is_rx_extended = False
                        is_tx_extended = False
                        
                        if (json_data["rxid"][-1] == "x"):
                            is_rx_extended = True
                            rxid = int(json_data["rxid"][:-1], 16)
                        else:
                            is_rx_extended = False
                            rxid = int(json_data["rxid"], 16)
                            
                        if (json_data["txid"][-1] == "x"):
                            is_tx_extended = True
                            txid = int(json_data["txid"][:-1], 16)
                        else:
                            is_tx_extended = False
                            txid = int(json_data["txid"], 16)
                            
                        if (is_rx_extended == False) and (is_tx_extended == False):
                            address_mode = isotp.AddressingMode.Normal_11bits
                            filters = [
                                {"can_id": rxid, "can_mask": 0x7FF, "extended": False},
                            ]
                        elif (is_rx_extended == True) and (is_tx_extended == True):
                            address_mode = isotp.AddressingMode.Normal_29bits
                            filters = [
                                {"can_id": rxid, "can_mask": 0x1FFFFFFF, "extended": True},
                            ]
                        if (address_mode != None):
                            self.bus = can.Bus(interface="serial", channel=json_data["serial_port"], can_filters=filters)
                            self.addr = isotp.Address(address_mode, rxid=rxid, txid=txid)
                            # self.tp_layer = isotp.TransportLayer(address=addr, params=params, error_handler=my_error_handler, rxfn=my_rxfn, txfn=my_txfn)
                            self.tp_layer = isotp.TransportLayer(address=self.addr, params=self.params, error_handler=self.my_error_handler, rxfn=self.my_rxfn, txfn=self.my_txfn)
                            if (self.tp_layer != None):
                                self.tp_layer.start()
                except:
                    print("Error, but I don't know what it is >_<")
                finally:
                    pass
                
            elif (mess == "Disconnect"):
                try:
                    json_data = json.loads(data)
                    if (json_data["serial_port"] != "") and (json_data["serial_port"] != None):
                        print(self.objectName() + " " + mess + ": ")
                        # print(data)
                        print(f'serial_port: {json_data["serial_port"]}')
                        print(f'can_baudrate: {json_data["can_baudrate"]}')
                        if (self.tp_layer != None):
                            self.tp_layer.stop()
                            self.tp_layer = None
                            print("terminate tp_layer")
                        if (self.bus != None):
                            self.bus.shutdown()
                            self.bus = None         
                            print("terminate bus")
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
                    hex_string = hex_string[0:4095*2]
                    hex_list = []
                    for i in range(0, len(hex_string), 2):
                        hex_value = int(hex_string[i:i+2], 16)  # Convert each pair to hex
                        hex_list.append(hex_value)
                    if (self.tp_layer != None) and (self.bus != None):
                        self.tp_layer.send(hex_list, send_timeout=40)
                        print("send done")
                        can_log = self.generateCanLog(self.tp_layer.address.get_tx_arbitration_id(), self.tp_layer.address.is_tx_29bits(), hex_list)
                        print("send generate can log done")
                        self.toUI.emit("can_log", can_log)
                        print("emit to UI done")
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



        try:
            if (self.tp_layer != None) and (self.bus != None):
                payload = self.tp_layer.recv(timeout=1)
                if payload is not None:
                    print(payload)
                    # if (rx_msg.arbitration_id == 0x18DA10F1) or (rx_msg.arbitration_id == 0x18DAF110):
                    can_log = self.generateCanLog(self.tp_layer.address.get_rx_arbitration_id(), self.tp_layer.address.is_rx_29bits(), payload)
                    self.toUI.emit("can_log", can_log)
        except:
            print("Error, but I don't know what it is >_<")
        finally:
            pass
                
             

        # print("Hello from " + self.objectName())
        # print("Num of running thread: " + str(len(Bico_QUIThread.getThreadHash())))
        # self.msleep(10)
           
        # print(f"---Thread Name: {threading.current_thread().name}, Thread ID: {threading.current_thread().ident}, Is Daemon: {threading.current_thread().daemon}")
        # self.threads = threading.enumerate()
        # for thread in self.threads:
        #     print(f"Thread Name: {thread.name}, Thread ID: {thread.ident}, Is Daemon: {thread.daemon}")
        # print("Hello from " + self.objectName())
        # print("Num of running thread: " + str(len(Bico_QUIThread.getThreadHash())))
                    
        self.msleep(100)
    
        return continue_to_run
















if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    Bico_QUIThread.setMainApp(app)

    Bico_QUIThread.create(
        BICO_CAN_TP(Bico_QMutexQueue(), 1, Bico_QMutexQueue(), 1, "task_0", os.path.join(current_path, "", "BICO_CAN_TP.qml"))
    )
    Bico_QUIThread.getThreadHash()["task_0"].start()

    Bico_QUIThread.create(
        BICO_CAN_TP(Bico_QMutexQueue(), 1, Bico_QMutexQueue(), 1, "task_1", os.path.join(current_path, "", "BICO_CAN_TP.qml"))
    )
    Bico_QUIThread.getThreadHash()["task_1"].start()

    sys.exit(app.exec())
