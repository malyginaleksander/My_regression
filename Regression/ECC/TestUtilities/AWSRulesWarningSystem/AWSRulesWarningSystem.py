#If a rule for pt or qa in aws s3 changes in any way, warn the user about the type of change with a message box.  If the user is okay with the change, they can just reset their rule expectations textfile(.jsons) by
#running python AWSRuleDescriptionGenerator.py.
import os
import json
import time
import sys
import GenericSettings

def warnUser(heading, body):
    GenericSettings.initializeConn()
    messageBoxCreatorFullPath = GenericSettings.getTheBasePath() + "UtilitySupportModules" + os.sep + "MessageBoxCreator.py "
    myCmd = "python " + messageBoxCreatorFullPath + heading.replace(" ", "_") + " " + body.replace(" ", "_")
    os.system(myCmd)

def ruleCheck(myString, myJSONObject, myExpectedJSONObject, ruleName):
    if(myString not in myJSONObject):
        if(myString in myExpectedJSONObject):
            warningString = "For " + ruleName + " a field named " + myString + " isn't in the rule description currently, but is in the expected rule description from when the AWSRuleDescriptionGenerator was run.\n"
            warnUser("Rule Warning!", warningString)
            return False
    elif(myString not in myExpectedJSONObject):
        if(myString in myJSONObject):
            warningString = "For " + ruleName + " a field named " + myString + " is in the rule description currently, but is not in the expected rule description from when the AWSRuleDescriptionGenerator was run.\n"
            warnUser("Rule Warning!", warningString)
            return False
    elif(myJSONObject[myString] != myExpectedJSONObject[myString]):
        warningString = ruleName + " is not in desired " + myString + ": " + myExpectedJSONObject[myString] + ".  To turn off this once per run warning, TEMPORARILY remove the rule from the AWSRulesFile.txt " \
        "or run AWSRuleDescriptionGenerator if you're fine with the rule change for now.  Just don't forget it's set that way!!!"
        warnUser("Rule Warning!", warningString)
        return False
    return True
    
def overallRuleCheck():
    #Run forever until killed, continuously checking to make sure the rules in the AWSRulesFile look the way in AWS we expect them to.
    #All the expected rule descriptions are stored in .json textfile formed from a command like subprocess.call("aws events describe-rule --name " + ruleName + " > " + myJSONInputFileName, shell=True)
    #The user is expected to set these up before the program starts.  They can do so by running python AWSRuleDescriptionGenerator.py if they'd like.
    #problematicFields is to track fields that already generated warnings to the user, so they're not hit with duplicates.
    problematicFields = []
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
                    warnUser("Rule Warning!", warningString)
                    sys.exit()
                if(not GenericSettings.fileHashComparison(myJSONInputFileName, myJSONExpectedInputFileName)):
                    myJSONFile = open(myJSONInputFileName, "r")
                    myJ = json.load(myJSONFile)
                    myJSONFile.close()
                    myExpectedJSONFile = open(myJSONExpectedInputFileName, "r")
                    myExpectedJ = json.load(myExpectedJSONFile)
                    myExpectedJSONFile.close()
                    #For uneven textfile(more rules in one than the other, part one:
                    for f in myExpectedJ:
                        if(f not in myJ):
                            if([f,ruleName] not in problematicFields):
                                if(not ruleCheck(f, myJ, myExpectedJ, ruleName)):
                                    problematicFields.append([f, ruleName])
                    # For uneven textfile(more rules in one than the other, part two:
                    for g in myJ:
                        if(g not in myExpectedJ):
                            if([g, ruleName] not in problematicFields):
                                if(not ruleCheck(g, myJ, myExpectedJ, ruleName)):
                                    problematicFields.append([g, ruleName])
                    for h in myExpectedJ:
                        if([h, ruleName] not in problematicFields):
                            if(not ruleCheck(h, myJ, myExpectedJ, ruleName)):
                                problematicFields.append([h, ruleName])
        time.sleep(600)

def main():
    overallRuleCheck()
    
if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()