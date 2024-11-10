import sys, os
module_path = os.path.abspath(os.path.join(os.getcwd(),"../Common/Template_Material"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Template_Material"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/BICO_CAN_Basic"))
sys.path.append(module_path)
module_path = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/BICO_CAN_Basic/Data_Object"))
sys.path.append(module_path)
current_path = os.getcwd()

from PySide6.QtGui import QGuiApplication

from bico_qmutexqueue import Bico_QMutexQueue
from bico_quithread import Bico_QUIThread
from BICO_CAN_Basic import BICO_CAN_Basic

import resource

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    Bico_QUIThread.setMainApp(app)

    Bico_QUIThread.create(
        # # Using pure qml
        # BICO_CAN_Basic,
        # Bico_QMutexQueue(), 
        # 1, 
        # Bico_QMutexQueue(), 
        # 1, 
        # "task_0", 
        # os.path.join(current_path, "Client_Code/BICO_CAN_Basic/BICO_CAN_Basic.qml")
        
        # Using qml which is intergrated to Qt resource
        BICO_CAN_Basic,
        Bico_QMutexQueue(),
        1, 
        Bico_QMutexQueue(), 
        1, 
        "task_0", 
        ":/Client_Code/BICO_CAN_Basic/BICO_CAN_Basic.qml"
    )
    Bico_QUIThread.getThreadHash()["task_0"].start()

    # Bico_QUIThread.create(
    #     # Using pure qml
    #     BICO_CAN_Basic,
    #     Bico_QMutexQueue(), 
    #     1, 
    #     Bico_QMutexQueue(), 
    #     1, 
    #     "task_1", 
    #     os.path.join(current_path, "Client_Code/BICO_CAN_Basic/BICO_CAN_Basic.qml")
        
    #     # # Using qml which is intergrated to Qt resource
    #     # BICO_CAN_Basic,
    #     # Bico_QMutexQueue(),
    #     # 1, 
    #     # Bico_QMutexQueue(), 
    #     # 1, 
    #     # "task_0", 
    #     # ":/Client_Code/BICO_CAN_Basic/BICO_CAN_Basic.qml"
    # )
    # Bico_QUIThread.getThreadHash()["task_1"].start()

    sys.exit(app.exec())
