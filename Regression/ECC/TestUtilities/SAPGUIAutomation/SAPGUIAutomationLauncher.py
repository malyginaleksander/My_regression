import SAPGUIAutomation as s
#import subprocess
#import signal
import os
import GenericSettings
#import time

#you can get TLP mini-confirmation numbers from a certain Query... with full outer join... in postgres...

#store the old input file and output file from prior runs.
#open the mini-confirmation number file(should have put together the web, inbound and TLP mini confirmation numbers by now.
#readlines, strip each line.
#make sure the dashes don't interfere with the below.  I don't think they should.
#for each mini confirmation number, use this lookup: http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=%s
#given that info, put the uan and the sap enrollment conf(if it has one) in the file, too.  Hopefully you also have some case comment in the file.  That might help for reporting.
#For each line, put the sap enrollment number and uan into the below.
#Modify the SAPGUIAutomation module to record the numbers you find to a copied file of the above with append.

#pid = subprocess.Popen(['C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe']).pid
#os.system('"C:\\Program Files (x86)\\SAP\\FrontEnd\\SAPgui\\saplogon.exe"')
#time.sleep(12)
#s.automate_SAP_GUI_Manipulation(sourceFileDir, SAPEnrollmentConf, myUAN, initialRunBoolean)
#s.automate_SAP_GUI_Manipulation("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SAPGUIAutomation\\", "0000005693305938", "1838964789", True)
#s.automate_SAP_GUI_Manipulation("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SAPGUIAutomation\\", "0000006596143600", "0182617110", True)
basePath = GenericSettings.getTheBasePath()
s.entryPoint(basePath + "SAPGUIAutomation" + os.sep, "0000006596137168", "0182617116", basePath + "SAPGUIAutomation" + os.sep + "ContractAndContractAccountIDs.txt")

#s.justTheEndPart("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SAPGUIAutomation\\", "0000006596142754", "00141480592519592", True)
#s.oldEndOnly("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SAPGUIAutomation\\", "0000006596142754", "00141480592519592", True)
#os.kill(pid, signal.SIGTERM) #or signal.SIGKILL
