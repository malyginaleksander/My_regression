#If a rule for pt or qa in aws s3 changes in any way, warn the user about the type of change with a message box.  If the user is okay with the change, they can just reset their rule expectations textfile(.jsons) by
#running python AWSRuleDescriptionGenerator.py.
import tkinter as tk
from tkinter import messagebox
import os
import json
import time
import sys
import GenericSettings

def ruleCheck(myString, myJSONObject, myExpectedJSONObject, ruleName):
    if(myString not in myJSONObject):
        if(myString in myExpectedJSONObject):
            warningString = "For " + ruleName + " a field named " + myString + " isn't in the rule description currently, but is in the expected rule description from when the AWSRuleDescriptionGenerator was run.\n"
            messagebox.showwarning("Rule Warning!", warningString)
            return False
    elif(myString not in myExpectedJSONObject):
        if(myString in myJSONObject):
            warningString = "For " + ruleName + " a field named " + myString + " is in the rule description currently, but is not in the expected rule description from when the AWSRuleDescriptionGenerator was run.\n"
            messagebox.showwarning("Rule Warning!", warningString)
            return False
    elif(myJSONObject[myString] != myExpectedJSONObject[myString]):
        warningString = ruleName + " is not in desired " + myString + ": " + myExpectedJSONObject[myString] + ".  To turn off this warning, TEMPORARILY remove the rule from the AWSRulesFile.txt or kill the AWSRulesWarningSystem Python program."
        messagebox.showwarning("Rule Warning!", warningString)
        return False
    return True
    
def overallRuleCheck():
    root = tk.Tk()
    root.withdraw()
    #Run forever until killed, continuously checking to make sure the rules in the AWSRulesFile look the way in AWS we expect them to.
    #All the expected rule descriptions are stored in .json textfile formed from a command like os.system("aws events describe-rule --name " + ruleName + " > " + myJSONInputFileName)
    #The user is expected to set these up before the program starts.  They can do so by running python AWSRuleDescriptionGenerator.py if they'd like.
    while(True):
        if(GenericSettings.internet_connected()):
            myJSONInputFileName = "myRuleStatus.json"
            myRuleFile = open("AWSRulesFile.txt", "r")
            ruleFileLines = myRuleFile.readlines()
            myRuleFile.close()
            for l in ruleFileLines:
                ruleName = l.strip()
                myList = l.split()
                cmdString = "aws events describe-rule --name " + ruleName + " > " + myJSONInputFileName
                os.system(cmdString)
                myJSONExpectedInputFileName = "expectedRuleStatus_" + myList[0] + ".json"
                if not os.path.exists(myJSONExpectedInputFileName):
                    warningString = "For " + ruleName + " the rule description (.json) file " + myJSONExpectedInputFileName + " was not found.  Either run python AWSRuleDescriptionGenerator.py or if you've previously generated the description file, grab it" +\
                                    " from wherever you've stored it, put it in the AWSRulesWarningSystem.pyw's directory and relaunch the program.\n"
                    messagebox.showwarning("Rule Description File Missing!", warningString)
                    sys.exit()
                if(not GenericSettings.fileHashComparison(myJSONInputFileName, myJSONExpectedInputFileName)):
                    myJSONFile = open(myJSONInputFileName, "r")
                    myJ = json.load(myJSONFile)
                    myJSONFile.close()
                    myExpectedJSONFile = open(myJSONExpectedInputFileName, "r")
                    myExpectedJ = json.load(myExpectedJSONFile)
                    myExpectedJSONFile.close()
                    #problematicFields is to track fields that already generated warnings to the user, so they're not hit with duplicates.
                    problematicFields = []
                    for f in myExpectedJ:
                        if(f not in myJ):
                            ruleCheck(f, myJ, myExpectedJ, ruleName)
                            problematicFields.add(f)
                    for g in myJ:
                        if (g not in myExpectedJ):
                            if(g not in problematicFields):
                                ruleCheck(g, myJ, myExpectedJ, ruleName)
                                problematicFields.add(g)
                    for h in myExpectedJ:
                        if(h not in problematicFields):
                            ruleCheck(h, myJ, myExpectedJ, ruleName)
        time.sleep(600)

def main():
    overallRuleCheck()
    
if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()