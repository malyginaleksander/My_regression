import S3AccountCorrespondenceChecker as s

def main():
    #s.checkS3Console(folderID, epnetOrSAP, resultsFile, twoLetterEnvironment, expectedEmail, expectedPDF)
    folderID = "69982352-15362004"
    epnetOrSAP = "sap"
    
    myResult = s.checkS3Console(folderID, epnetOrSAP, "qa", False, True)
    print(myResult)
    
if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()