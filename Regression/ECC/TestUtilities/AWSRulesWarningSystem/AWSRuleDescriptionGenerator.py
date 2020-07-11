import os

def generateRuleDescriptions():
    myRuleFile = open("AWSRulesFile.txt", "r")
    ruleFileLines = myRuleFile.readlines()
    myRuleFile.close()
    for l in ruleFileLines:
        ruleName = l.strip()
        myList = l.split()
        myJSONExpectedInputFileName = "expectedRuleStatus_" + myList[0] + ".json"
        cmdString = "aws events describe-rule --name " + ruleName + " > " + myJSONExpectedInputFileName
        os.system(cmdString)
        
def main():
    generateRuleDescriptions()
    
if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()
