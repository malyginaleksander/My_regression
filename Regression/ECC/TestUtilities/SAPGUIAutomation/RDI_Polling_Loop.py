import pysftp
import time

#specialPrefix is the piece of text inserted at the beginning of an RDI_File name to show that this is the RDI_File we requested.  It should not be present in other filenames.
def poll_For_The_RDI_File(specialPrefix):
    
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    
    dirString = '/usr/app/sap/ccs/work_out/'
    cmdString = 'ls %s' % dirString
    
    #I should specify the special text in the email I send to the SAP team.  And I can strip it before I use it.  This is important so I can track the file my account went into... or I can try to read the RDI myself.
    #just search on the special text and narrow it down by searching the textfile.  But ideally, they should add the special text each time.
    #specialPrefix = "outfac"
    rdiFileNotFound = True
    while(rdiFileNotFound):
        srv = pysftp.Connection(host="saprpm01.reinternal.com", username="nrpftp", password="Bedrock2", port=22, cnopts=cnopts)
        myResponse = srv.execute(cmdString)
        for i in myResponse:
            tempString = i.decode('UTF-8').strip()
            if(specialPrefix in tempString):
                myList = tempString.split(specialPrefix)
                if(myList[0] == ''):
                    srv.get(dirString + tempString)
                    rdiFileNotFound = False
        srv.close()
        if(rdiFileNotFound):
            time.sleep(180)

#The below error seems to happen because either with's object isn't context aware, doesn't have __enter__ and __exit__ methods-
#or there's something else messed up with the with / srv.execute statement.
#getting attribute error __enter__
#Also, cd-ing to the end directory right away will result in an internal overflow error for some reason.
#dirString = '/home/nrpftp'

#cmdString = 'cd %s; pwd' % dirString
#cmdString = 'chdir %s; pwd; ls' % dirString

#Also might need srv.normalize() for the simlink / forwarding link.

#with srv.execute(cmdString):

#For some reason, on this server there is no persistence between commands- at least with changing directories- so you have to do what you need to by referencing absolute paths, like 'ls thePathYouWantToList'.
#Also, responses will give bytes literals instead of string literals... I don't know why, but I'll have to find some way to convert them.
#https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
#I could also normalize the symlink for ls-ing... that's fine as long as you don't try to srv.cd to it(which causes some weird internal overflow, and I don't know why).
#This would prevent an error where the admins change what that symlink points to... I would imagine if they went to the trouble of setting up a symlink, the end destination might change at some point... or even frequently.

#print("\nPutting my data file on nerfsftp.dev.nrgpl.us server through pysftp.\n")
#dirString = '/home/nerf_api/%s/tlp' % GenericSettings.getMyEnvironment().lower()
#dirString = '/home/nrpftp/work_out'

#print("\nConnecting to pysftp nerfsftp.dev.nrgpl.us server\n")
#srv = pysftp.Connection(host="nerfsftp.dev.nrgpl.us", username="sftpinbound", password="standing-desks-034", port=22, cnopts=cnopts)

#import paramiko
#import GenericSettings
#/usr/app/sap/ccs/work_out
#/home/nrpftp/work_out - a symbolic link, I think, to the above address...  Might have to try going to this address first.  It should send you to the above address.
