import openpyxl
import sys
import os
import requests

#Slightly modified from https://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter
def arrayIndexToExcelColumnLetters(n):
    n = n + 1
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

#e.g. insertValues("BrandSlug", "brand_slug", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
def insertValues(columnName, stringColumnName, rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates):
    #arrayIndexToExcelColumnLetters(...) will take care of this.
    #myColumnNum = columnHeaderValues.index(columnName) + 1
    myColumnNum = columnHeaderValues.index(columnName)
    myIndex = columnCandidates.index(stringColumnName)
    myValue = valueCandidates[myIndex]
    cellIndex = arrayIndexToExcelColumnLetters(myColumnNum) + str(rowTarget)
    sheet[cellIndex] = myValue
    
#e.g. altInsertValues("BrandSlug", "brand_slug", rowTarget, sheet, columnHeaderValues)
def altInsertValues(myJSON, columnName, suppliedValue, rowTarget, sheet, columnHeaderValues):
    #arrayIndexToExcelColumnLetters(...) will take care of this.
    #myColumnNum = columnHeaderValues.index(columnName) + 1
    myColumnNum = columnHeaderValues.index(columnName)
    cellIndex = arrayIndexToExcelColumnLetters(myColumnNum) + str(rowTarget)
    sheet[cellIndex] = myJSON['results'][0][suppliedValue]

def addProductNotFoundToTheBuilderSpreadsheet():
    print("\nMoving preexisting .xlsx textfile to the backup folder ")
    for file in os.listdir("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\AddProductFromError"):
        if file.endswith(".xlsx"):
            #Move old .xlsx textfile to a backup folder.
            os.rename(file, os.path.join("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\AddProductFromError\\Backup_XLSX_Files\\", file))

    print("\nThis is the error-to-product converter for errors of type: \"Product API lookup failure: no products found\" \n")
    print("\nHere is a complete sample error message.  What you paste should look similar, except for the environment and parameters perhaps changing.\n")
    print("\n\"error_message\": \"Product: Product API lookup failure: no products found -- http://products.pt.nrgpl.us/api/v1/products/?active=0&brand_slug=nrg_residential&channel=retention&commodity=electric&partner_code=nrr&pe_lock_type=intro&premise_type=residential&pricing_term=1&priority_level=&product_slug=retention_no_frills_24m&promo_code=524&rate=0.09600&state_slug=pa&terms_of_service_type=variable&utility_slug=penelec&vas_code=006\",")
    myErrorText = input("\nPaste the complete text of the error you found into the window and press enter: \n").strip()
    
    productString = myErrorText.split("?")[1]
    productString = productString.strip(',')
    productString = productString.strip('"')
    pairList = productString.split("&")
    columnCandidates = []
    valueCandidates = []
    for i in pairList:
        tempList = i.split("=")
        columnCandidates.append(tempList[0])
        if (len(tempList) == 1):
            valueCandidates.append("")
        else:
            valueCandidates.append(tempList[1])
            
    myIndex = columnCandidates.index("brand_slug")
    myBrandSlug = valueCandidates[myIndex]
    
    #The campaign id is referred to as the promo in IRW.
    myCampaignID = input("\nCopy the IRW \"Promo\" value(known as the campaign id outside of IRW) for the account and paste it in the window: ").strip()
    myOfferID = input("\nCopy the IRW \"Offer\" value(known as the offer id outside of IRW) for the account and paste it in the window: ").strip()
    
    myEnv = None
    if("products.pt.nrgpl.us" in myErrorText):
        myEnv = "pt"
        print("\nIn your browser, navigate to http://manage.products.pt.nrgpl.us/Builder/#/download    and select the appropriate brand for your brand_slug which is: " + myBrandSlug + ".\n")
    elif("products.qa.nrgpl.us" in myErrorText):
        myEnv = "qa"
        print("\nIn your browser, navigate to http://manage.products.qa.nrgpl.us/Builder/#/download    and select the appropriate brand for your brand_slug which is: " + myBrandSlug + ".\n")
    print("\nThen download and place the file in: C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\AddProductFromError.")

    #print("\nProcessing error string.\n")
    # Loop and wait for the spreadsheet to be placed in the directory?  Nah, wait for user input.

    myResponse = input("\nWhen the spreadsheet file is in the location, press Y, or press any other key to quit: ").strip().upper()
    if (myResponse != "Y"):
        sys.exit("The user's response was: " + myResponse + " so the program is now exiting.\n")

    excelFile = None
    excelFileName = None
    # find a .xlsx file.
    for file in os.listdir("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\AddProductFromError"):
        if file.endswith(".xlsx"):
            #copy the file with my vb script, then rename it back to its original name.
            #How the VBScript works is it does a simple copy of an xlsx file, but in copying it, somehow the file becomes standardized(maybe converted from Mac-internal format or decorrupted or something.
            #If you don't perform this operation first, openpyxl will error out when it tries to save later.
            fileName2 = "B" + file
            myPath = "C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\AddProductFromError\\"
            full_1 = os.path.join("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\AddProductFromError\\", file)
            full_2 = os.path.join("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\AddProductFromError\\", fileName2)
            myString = "xlsxStandardizer.vbs \"" + myPath + "\" \"" + file + "\""
            os.system(myString)
            os.remove(full_1)
            os.rename(full_2, full_1)
            
            excelFile = openpyxl.load_workbook(full_1)
            excelFileName = full_1
            #there should only be one .xlsx file.
            break

    sheet = excelFile.get_sheet_by_name('NRP Product Catalog')
    rowTarget = sheet.max_row + 1
    sheet.insert_rows(rowTarget)

    columnHeaderValues = []
    for cell in sheet[1]:
        columnHeaderValues.append(cell.value)

    #The important piece of a sample error:
    # http://products.pt.nrgpl.us/api/v1/products/?active=0&brand_slug=nrg_residential&channel=retention&commodity=electric&partner_code=nrr&pe_lock_type=intro&premise_type=residential&pricing_term=1&priority_level=
    # &product_slug=retention_no_frills_24m&promo_code=524&rate=0.09600&state_slug=pa&terms_of_service_type=variable&utility_slug=penelec&vas_code=006",

    insertValues("BrandSlug", "brand_slug", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("ChannelSlug", "channel", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("Commodity", "commodity", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("PartnerCode", "partner_code", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("PricingEngineLockType", "pe_lock_type", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("PremiseType", "premise_type", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("PricingTerm", "pricing_term", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("PriorityLevel", "priority_level", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("ProductSlug", "product_slug", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("PromoCode", "promo_code", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("Rate", "rate", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("StateSlug", "state_slug", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("TermsOfServiceType", "terms_of_service_type", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("UtilitySlug", "utility_slug", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    insertValues("VASCode", "vas_code", rowTarget, sheet, columnHeaderValues, columnCandidates, valueCandidates)
    
    #myReqString = "http://products.pt.nrgpl.us/api/v1/products/?campaign_id=U-00001947&offer_id=1000012547"
    myReqString = "http://products.%s.nrgpl.us/api/v1/products/?campaign_id=%s&offer_id=%s" % (myEnv, myCampaignID, myOfferID)

    myJ = requests.get(myReqString).json()
    
    #Handling the "Action" column name.
    myColumnNum = columnHeaderValues.index("Action")
    cellIndex = arrayIndexToExcelColumnLetters(myColumnNum) + str(rowTarget)
    sheet[cellIndex] = "Add"
    
    #productAPIProductDescription = """
    #######SPECIAL CASE- THIS LINE HAS NO PRODUCT INFO EQUIVALENT, IT'S ONLY IN THE PRODUCT BUILDER SPREADSHEET.  "None" is literal here, handled in the three lines above.  altInsertValues(myJ, "Action", "None", rowTarget, sheet, columnHeaderValues)
    #The commented out lines below have to do with insertions into the spreadsheet we've already made above.  They're left here so that anyone else can grab this block as a shorthand for taking a block of product info and putting it in a product
    #builder spreaddsheet- with the caveat that the Action column, usually having the value None, would have to be dealt with, too.
    altInsertValues(myJ, "SKU", "sku"                                 , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "BrandSlug", "brand_slug"                   , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "ChannelSlug", "channel"                      , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "SubChannel", "sub_channel"                      , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "Ranking", "ranking"                      , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "ProductSlug", "product_slug"                     , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "ProductName", "product_name"                      , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "ProductDescription", "product_description"        , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "ProductPath", "product_path"                      , rowTarget, sheet, columnHeaderValues)
    
    #This date needs to be 04_formated to fit in MM/DD/YYYY... and obviously to drop the date.
    #sample original date: 9999-12-31T12:00:00Z
    myColumnNum = columnHeaderValues.index("ExpirationDate")
    cellIndex = arrayIndexToExcelColumnLetters(myColumnNum) + str(rowTarget)
    mySubString = str(myJ['results'][0]["expiration_date"]).split("T")[0]
    myDateList = mySubString.split("-")
    myFinalDateString = myDateList[1] + "/" + myDateList[2] + "/" + myDateList[0]
    sheet[cellIndex] = myFinalDateString
    
    ###############SPECIAL CASE TO HANDLE THE DATES HERE, ABOVE. altInsertValues(myJ, "ExpirationDate", "expiration_date"                , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "StateSlug", "state_slug"                      , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "Commodity", "commodity"                     , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "UtilitySlug", "utility_slug"                     , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "UtilityZone", "utility_zone"                      , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "PremiseType", "premise_type"                      , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "PricingTerm", "pricing_term"                      , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "PricingEngineLockType", "pe_lock_type"                      , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "TermsOfServiceType", "terms_of_service_type"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "UtilityRate", "utility_rate"                   , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "Rate", "rate"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "UtilityOnPeakRate", "utility_on_peak_rate"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "OnPeakRate", "on_peak_rate"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "UtilityOffPeakRate", "utility_off_peak_rate"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "OffPeakRate", "off_peak_rate"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "PenaltyType", "penalty_type"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "EarlyCancellationFee", "early_cancellation_fee"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "DailyServiceCharge", "daily_service_charge"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "MonthlyServiceCharge", "monthly_service_charge"                   , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "VASCode", "vas_code"                  , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "ProductEligibilityClass", "product_eligibility_class"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "Adder", "adder"                   , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "PartnerCode", "partner_code"                  , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "PromoCode", "promo_code"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "MerchandiseText", "merchandise"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "MerchandiseSlug", "merchandise_slug"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "MerchandiseVesting", "merchandise_vesting"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "SignupBonus", "signup_bonus"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "SignupVesting", "signup_vesting"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "OngoingValue", "ongoing_value"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "OngoingFrequency", "ongoing_frequency"                   , rowTarget, sheet, columnHeaderValues)
    #altInsertValues(myJ, "PriorityLevel", "priority_level"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "TermsOfServiceTemplate", "tos_template"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "RequiresPriceChangeNotice", "requires_price_change_notice"                   , rowTarget, sheet, columnHeaderValues)
    altInsertValues(myJ, "RateCategory", "rate_category"                   , rowTarget, sheet, columnHeaderValues)
    #"""

    excelFile.save(excelFileName)

    print("\nSuccess.  The spreadsheet has been modified and saved with the new product corresponding to the error you encountered.\n")
