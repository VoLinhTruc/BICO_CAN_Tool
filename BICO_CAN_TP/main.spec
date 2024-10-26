# build command: pyinstaller main.spec

# -*- mode: python ; coding: utf-8 -*-

import sys, os
from cx_Freeze import Executable, setup

path0 = os.path.abspath(os.path.join(os.getcwd(),"../Common/Template_Material"))
path1 = os.path.abspath(os.path.join(os.getcwd(),"Template_Material"))
path2 = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/BICO_CAN_TP"))
path3 = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/BICO_CAN_TP/Data_Object"))
path4 = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/Bico_QUIThread_Sample"))
path5 = os.path.abspath(os.path.join(os.getcwd(),"Client_Code/Bico_QUIThread_Sample/Data_Object"))

block_cipher = None

a = Analysis(['main.py'],
             pathex=[path0, path1, path2, path3, path4, path5],
             binaries=[],
             datas=[],
             hiddenimports=["can", "can.interfaces.serial", "bico_qmessdata", "bico_qmutexqueue", "bico_qthread", "bico_quithread", "BICO_CAN_TP", "Bico_QUIThread_Sample", "resource", "Example_Data_Object"],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# in case of hiddenimports not work
# add_imports=['can', 'can.interfaces.serial', 'bico_qmessdata', 'bico_qmutexqueue', 'bico_quithread', 'BICO_CAN_TP', 'Bico_QUIThread_Sample', 'resource'],



# onefile ----------------------------------------------------------------
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
#          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='icon.ico' )
# onefile ----------------------------------------------------------------



# not onefile ----------------------------------------------------------------
# exe = EXE(pyz,
#           a.scripts, 
#           [],
#           exclude_binaries=True,
#           name='main',
#           debug=False,
#           bootloader_ignore_signals=False,
#           strip=False,
#           upx=True,
#           console=True,
#           disable_windowed_traceback=False,
#           target_arch=None,
#           codesign_identity=None,       
#           entitlements_file=None )
          
# coll = COLLECT(exe,
#                a.binaries,
#                a.zipfiles,
#                a.datas, 
#                strip=False,
#                upx=True,
#                upx_exclude=[],
#                name='main')
# not onefile ----------------------------------------------------------------