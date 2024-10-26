# build command: python setup.py build
#  cx_freezed does not support to build single file
# https://cx-freeze.readthedocs.io/en/latest/faq.html (Single-file executables section)

import sys, os
from cx_Freeze import Executable, setup

path0 = os.path.abspath(os.path.join(os.getcwd(),"../Common/Template_Material"))
path1 = os.path.abspath(os.path.join(os.getcwd(),"Template_Material"))
path2 = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/BICO_CAN_TP"))
path3 = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/BICO_CAN_TP/Data_Object"))

executables = [Executable("main.py")]


options = {
    "build_exe": {
        "path": sys.path + [path0, path1, path2, path3],
        "includes": ["bico_qmessdata", "bico_qmutexqueue", "bico_qthread", "bico_quithread", "BICO_CAN_TP", "resource", "Example_Data_Object"],
        # include qml file as pure qml file (not include in Qt resource file -> make qml content to binary)
        # "include_files": ["BICO_CAN_TP.qml"],
        "excludes": [""],
    }
}

setup(
    name="QtQuick_Project_Template",
    version="0.1",
    description="QtQuick_Project_Template",
    options=options,
    executables=executables,
)
