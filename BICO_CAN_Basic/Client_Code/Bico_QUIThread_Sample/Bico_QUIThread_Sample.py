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

class BICO_CAN_Basic(Bico_QUIThread):
    i = 0
    ex_data_obj = Example_Data_Object()
    def MainTask(self):
        continue_to_run = 1
        
        i = 0
        input, result = self.qinDequeue()

        if result:
            mess = input.mess()
            data = input.data()
            if (mess == "terminate"):            
                continue_to_run = 0
            elif (mess == "num1"):
                print(self.objectName() + " " + mess + " " + str(self.ex_data_obj.getData_1()))
            elif (mess == "num2"):
                print(self.objectName() + " " + mess + " " + str(self.ex_data_obj.getData_2()))
            elif (mess == "text"):
                print(self.objectName() + " " + mess + " " + data)
                self.toUI.emit(mess, data)
            elif (mess == "size"):
                print(self.objectName() + " " + mess + " " + str(data.width()) + str(data.height()))
                self.toUI.emit(mess, data)
            elif (mess == "from_another_thread"):
                print(self.objectName() + " " + mess + ": "  + input.src() + " - " + str(data))

        print("Hello from " + self.objectName())
        print("Num of running thread: " + str(len(Bico_QUIThread.getThreadHash())))
        self.msleep(1000)

        if ((self.objectName() == "task_1") and (Bico_QUIThread.getThreadHash().get("task_0") != None)):
            self.i += 1
            mess_data = Bico_QMessData("from_another_thread", self.i)
            mess_data.setSrc(self.objectName())
            Bico_QUIThread.getThreadHash().get("task_0").qinEnqueue(mess_data)
            self.msleep(2365)

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
