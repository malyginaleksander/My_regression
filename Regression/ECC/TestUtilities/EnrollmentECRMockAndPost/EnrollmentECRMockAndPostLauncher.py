import EnrollmentECRMockAndPost

#region=us-east-1
def ECRMockingHelper(ECRFileName, myEnvironment):
    if(myEnvironment.strip().upper() == "QA"):
        EnrollmentECRMockAndPost.mockECRAndPostIt(ECRFileName, "QA", "qa", "us-east-1")
        #mockECRAndPostIt(myFullFilename, suppliedEnvironment, myProfileName, myRegion):
    elif(myEnvironment.strip().upper() == "PT"):
        EnrollmentECRMockAndPost.mockECRAndPostIt(ECRFileName, "PT", "prod", "us-east-1")
    else:
        print("\nEnvironment not recognized.\n")
        
def main():
    ECRMockingHelper("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\EnrollmentECRMockAndPost\\9a2458ae-e179-4ed8-b65f-e8c558833249.json", "PT")

if __name__ == '__main__':
    #sys.settrace(trace_calls)
    main()


