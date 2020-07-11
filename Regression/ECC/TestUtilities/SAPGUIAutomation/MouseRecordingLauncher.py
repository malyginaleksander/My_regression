import MouseRecording as m
import GenericSettings
import os
#import signal
#import time
#import subprocess

#import asyncio
#
#async def myRun(cmd):
#    proc = await asyncio.create_subprocess_shell(
#        cmd,
#        stdout=asyncio.subprocess.PIPE,
#        stderr=asyncio.subprocess.PIPE)
#
#    stdout, stderr = await proc.communicate()
#    
#    print(f'[{cmd!r} exited with {proc.returncode}]')
#    if stdout:
#        print(f'[stdout]\n{stdout.decode()}')
#    if stderr:
#        print(f'[stderr]\n{stderr.decode()}')
#
#asyncio.run(myRun('"cmd C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"'))

#https://docs.python.org/3/library/subprocess.html#subprocess-replacements
#Replacing the os.spawn family
#P_NOWAIT example:
#
#pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
#==>
#pid = Popen(["/bin/mycmd", "myarg"]).pid

#Commenting that out for now, otherwise I should probably grab the cwd first to restore it afterwards.
#os.chdir('C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\')
#pid = subprocess.Popen(['C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe']).pid
#pid = subprocess.Popen(['C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\OUTLOOK.exe']).pid

#pid = subprocess.Popen(['"cmd C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"'], cwd='"C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\"').pid
#pid = subprocess.Popen(['"C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"'], executable='"C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"').pid
#os.system('"cmd C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"')
#time.sleep(10)
#m.recordTheMouse(absoluteRecordingBoolean, initialCalibrationBoolean, sourceFileDir)
GenericSettings.initializeConn()
m.recordTheMouse(True, False, GenericSettings.getTheBasePath() + os.sep + "SAPGUIAutomation" + os.sep)
#m.recordTheMouse(False, False, "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SAPGUIAutomation\\")
#os.kill(pid, signal.SIGTERM) #or signal.SIGKILL 