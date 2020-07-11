from traceback import print_stack

class allMethods(object):

    def strContains(self, actualText, expectedText):

        if expectedText.lower() in actualText.lower():
            return True
        else:
            return False

    def strEquals(self,actualText,expectedText):
       if actualText.lower() == expectedText.lower():
           return True
       else:
           return False




        #Reading and writing data from/to excel
        #so on