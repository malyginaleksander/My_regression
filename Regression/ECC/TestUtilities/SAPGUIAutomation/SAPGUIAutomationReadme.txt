Setup:
To use this, you'll need to be connected to an NRG-privileged network, like with a Philadelphia or Princeton office ethernet cable, or over the VPN at home.  Get on a network like that.

Part 1: Password Setup
In the SAPGUIAutomation directory, open service.txt and replace the number in the file with your SAP username(usually an 8 digit number).
Open a terminal, go to the SAPGUIAutomation directory and enter Python PasswordMaker.py.
It'll ask you if the new username you entered is your password.  Press 'y'.  It'll then prompt you for your SAP password, to encrypt it and securely store it on your computer's KEYRING.  Enter your SAP password and hit enter.

Part 2: GUI Calibration
The first mouse coordinate will need to be changed for every different user, but ideally the rest should be fine.  So move every mouse coordinate file currently in the SAPGUIAutomation directory except for mouse coordinate 1
into a separate folder.  KEEP IN MIND that if in between uses of the SAP automation feature, you move the initial SAP Logon window, its position tends to be saved by the computer on program shutdown,
so if you move it from where it was during the GUI calibration, you'll have to redo the GUI calibration; however, you should only have to do the first mouse coordinate after the you've seen the SAPGUIAutomation program
work on your machine before, and the dev also hopes that coordinates beyond the first just work right out of the box from what the dev set up.  That's what you'll have to test.

Open a terminal, go to the SAPGUIAutomation directory and enter python MouseRecordingLauncher.py.
It will open the SAPLogon.exe program for you, then it will wait(sleep for 10 seconds).
Then you will see:
"The program will now track and collect the last mouse position.  To use it, first click on the command prompt window.  Then move your mouse to the position you want to record to a numbered lastMouseCoord file.  Then
press ctrl-C for Windows or your operating system's keyboard interrupt combination.  If the first press doesn't take, press it again; sometimes the operating system needs to sort out what the interrupt is being applied to."
Move your mouse cursor over RPM: Retail Production Maintenance- to where you COULD click on it, but don't click.  Press Ctrl-c or your operating system's keyboard interrupt combination.
If you don't see the text, "Last mouse coordinates..." in the command prompt window, press ctrl-C again.  Then you should see:
"Last mouse coordinates just saved.  To record an additional entry, press Y.  To quit, press any other key."
Hopefully you'll only need to record that first mouse coordinate!  Now move all the other mouse coordinate files- the ones numbered above one- back into the SAPGUIAutomation directory.

Part 3: Editing and Running SAPGUIAutomationLauncher.py.
Open SAPGUIAutomationLauncher.py and edit this line: 
s.automate_SAP_GUI_Manipulation("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\SAPGUIAutomation\\", "0000005693305938", "1838964789", True)
Change the first parameter to your SAPGUIAutomation directory.  Change the second to a SAPEnrollmentConfirmation number of a SAP account
you've recently run through INITIAL enrollment, but not the SAP RPM stuff with processing the idoc and all that.  This program is intended as a tool so that other programs can call it with this information automatically.  Today we'll
just be demonstrating the manual operation.  Change the the third parameter to the UAN of the account.  Keep the fourth parameter as True- it will only be False if we're leaving the SAP programs open to perform more operations;
and in that case we'd have to put those additional operations before this line in the launcher: os.kill(pid, signal.SIGTERM) #or signal.SIGKILL
Save the SAPGUIAutomationLauncher.py file.

In a terminal, make sure you're in SAPGUIAutomationLauncher's directory then enter python SAPGUIAutomationLauncher.py.

Observe the results.  At the end of all the clicking and processing, the program should generate a text file called ContractAndContractAccountID that should contain, surprise, the Contract ID and the Contract Account ID.
You should be able to put that in an email to the SAP team requesting an RDI file, and then you can take the RDI file they give you and run it, completing the enrollment.

IF THE GUI AUTOMATION DIDN'T GO AS PLANNED, and you don't have a Contract ID and Contract Account ID result, someone(ideally the dev, Matt Hissong) will have to run the mouse recording program again for your specific
monitor setup to record all the mouse coordinates that the overall sap gui enrollment process should contain.  A remote desktop session might work.  But individual users aren't the primary setup objective for this program- see below.

Part 4: Future Plans
THE PLAN IS TO PUT THIS GUI ENROLLMENT SERVICE ON A CENTRAL MACHINE, like a server, that we could just send requests to and it would automatically enroll them.
That way we wouldn't need to automate the mouse positions for each individual user.  BUT.  Hopefully the initial mouse position is the only thing a user needs to change, and the rest of the program just works.
As far as the POSSIBLE FUTURE ROADMAP for this central machine enrollment automation, it goes: SAPGUIAutomationLauncher -> AutoEmailAListOfContractAndContractAccountIDs,
maybe by sending to the user's own Outlook account with an autoforwarding rule in Outlook so that the email to the SAP team has a valid, recognizable sender -> PollForAnExpectedRDIFileName in the RDI Output directory ->
AutomaticRDIRuns in CCC.
