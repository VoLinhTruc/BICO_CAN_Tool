import sys, os
module_path = os.path.abspath(os.path.join(os.getcwd(),"../Common/Template_Material"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Template_Material"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/BICO_CAN_TP"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/BICO_CAN_TP/Data_Object"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/Bico_QUIThread_Sample"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/Bico_QUIThread_Sample/Data_Object"))
sys.path.append(module_path)
current_path = os.getcwd()

from PySide6.QtGui import QGuiApplication

from bico_qmutexqueue import Bico_QMutexQueue
from bico_quithread import Bico_QUIThread
from BICO_CAN_TP import BICO_CAN_TP
from Bico_QUIThread_Sample import Bico_QUIThread_Sample

import resource
import threading

if __name__ == "__main__":
    # print(f"***Thread Name: {threading.current_thread().name}, Thread ID: {threading.current_thread().ident}, Is Daemon: {threading.current_thread().daemon}")
    app = QGuiApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    Bico_QUIThread.setMainApp(app)

    Bico_QUIThread.create(
        # # Using pure qml
        # BICO_CAN_TP,
        # Bico_QMutexQueue(), 
        # 1, 
        # Bico_QMutexQueue(), 
        # 1, 
        # "task_0", 
        # os.path.join(current_path, "Client_Code/BICO_CAN_TP/BICO_CAN_TP.qml")
        
        # Using qml which is intergrated to Qt resource
        BICO_CAN_TP,
        Bico_QMutexQueue(),
        1, 
        Bico_QMutexQueue(), 
        1, 
        "task_0", 
        ":/Client_Code/BICO_CAN_TP/BICO_CAN_TP.qml"
    )
    Bico_QUIThread.getThreadHash()["task_0"].start()

    Bico_QUIThread.create(
        # # Using pure qml
        # Bico_QUIThread_Sample,
        # Bico_QMutexQueue(), 
        # 1, 
        # Bico_QMutexQueue(), 
        # 1, 
        # "task_1", 
        # # os.path.join(current_path, "Client_Code/Bico_QUIThread_Sample/Bico_QUIThread_Sample.qml")
        # ""
        
        # Using qml which is intergrated to Qt resource
        Bico_QUIThread_Sample,
        Bico_QMutexQueue(),
        1, 
        Bico_QMutexQueue(), 
        1, 
        "task_1", 
        # ":/Client_Code/BICO_CAN_TP/BICO_CAN_TP.qml"
        ""
    )
    Bico_QUIThread.getThreadHash()["task_1"].start()

    ret = app.exec()    
    sys.exit(ret)
    
    
    print("XXXX")