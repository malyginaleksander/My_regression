Program Purpose: Modify the data file to make it unique and then check to see if the UID / Conf # generated off the start of a file enrollment collides with a preexisting UID in dev / prod.
As recently as 8/2018 that was 100% the case, collisions every time, meaning the preexisting UID in dev / prod would cause various systems to rely on the prod record data for things.

Author: Matt Hissong

User instructions:
Have the standard Python 3.5 environment.

Download the ProdUIDConfNumCollisionCheckOffFileEnrollment.py to your local environment.  Open ProdUIDConfNumCollisionCheckOffFileEnrollment.py in a text editor and change:

All references to PT to QA or vice versa.

Change the filenum to the current number after the base file name you're starting on:
    currentFileNum = "235"
    Change the base file name to your preference, so long as you have a corresponding data file of the same name to start with.
    currentInputBaseFileName = "PPIU"
    Change the input path to the one where your data files are.
    currentInputPath = "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestScripts\\"

There are soft and hard time limits, each of which have flags for whether they cause a program exit.  You'll probably be most interested in softFileLimit.  Set it to something low if you're just looking to see if this program runs,
and to something high if you want to really check to see if you can ever get a unique UID / UAN combo off a file enrollment- that doesn't collide with UID's / UAN's in dev / prod.
    softTimeLimit = 18000
    #5 days
    hardTimeLimit = 432000
    softFileLimit = 10000
    hardFileLimit = 100000

    softTimeLimitFlag = False
    #hardTimeLimit in the limitCheck function is used if this is True.  This flag should probably always be left True as a backstop.
    hardTimeLimitFlag = True
    #Can be enabled for environment concerns.  softFileLimit in the limitCheck function is used if this is True.
    softFileLimitFlag = True
    #hardFileLimit in the limitCheck function is used if this is True.  This flag should probably always be left True as a backstop.
    hardFileLimitFlag = True

To execute: Just enter Python ProdUIDConfNumCollisionCheckOffFileEnrollment.py at the command prompt where the data file is.

Output: The program will modify the UID and UAN, check the UID and UAN against the environment specified AND dev, and determine if the UID / UAN are unique.  If not, the program will repeat itself until the program does find a unique uid / uan combo.

Any possible issues? - Sometimes "the workers are down" - the workers being automated polling processes that look for events / files uploaded and take corresponding actions.  If your enrollment isn't appearing, open up loggly and search:
https://nrgretail.loggly.com/search#terms=%20tag:portal_worker%20tag:qa&from=2018-09-06T15:01:34.124Z&until=2018-09-06T15:31:34.124Z&source_group=
change tag:qa to tag:pt if you're on pt.  If you don't see any / many worker events, they might be down.

Also sometimes the enrollment to backend-received trigger is turned off.  If the workers look fine, ask Chrissy Chimi / the current ECC ScrumMaster about the environment you're on and that trigger.

Alternatively, if you're getting into backend-received but not corrrespondence_request then the backend_received to correspondence_request trigger may be off.
If the workers look fine, ask Chrissy Chimi / the current ECC ScrumMaster about the environment you're on and that trigger.

If Python tells you you don't have a module, type pip install ThatModuleName.  If you don't have pip, download and install it.

To use this, you'll need to be connected to an NRG-privileged network, like with a Philadelphia or Princeton office ethernet cable, or over the VPN at home.

