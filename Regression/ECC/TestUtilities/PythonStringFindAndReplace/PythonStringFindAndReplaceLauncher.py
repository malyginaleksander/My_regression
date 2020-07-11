import GenericSettings

def main():
    #GenericSettings.findAndReplaceInDirectoryWRecursiveSearchPyTxt(myDir,myString,myReplacementString)
    GenericSettings.findAndReplaceInDirectoryWRecursiveSearchPyTxt("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\UnverifiedTestUtilities", "TestUtilities", "UnverifiedTestUtilities")
    
if __name__ == '__main__':
    # sys.settrace(trace_calls)
    main()