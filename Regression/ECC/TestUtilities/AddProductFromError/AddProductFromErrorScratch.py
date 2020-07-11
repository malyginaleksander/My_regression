excelColumnNames = "Action	SKU	BrandSlug	ChannelSlug	SubChannel	Ranking	ProductSlug	ProductName	ProductDescription	ProductPath	ExpirationDate	StateSlug	Commodity	UtilitySlug	UtilityZone	PremiseType	PricingTerm	PricingEngineLockType" \
                   "TermsOfServiceType	UtilityRate	Rate	UtilityOnPeakRate	OnPeakRate	UtilityOffPeakRate	OffPeakRate	PenaltyType	EarlyCancellationFee	DailyServiceCharge	MonthlyServiceCharge	VASCode	ProductEligibilityClass	Adder" \
                   "PartnerCode	PromoCode	MerchandiseText	MerchandiseSlug	MerchandiseVesting	SignupBonus	SignupVesting	OngoingValue	OngoingFrequency	PriorityLevel	TermsOfServiceTemplate	RequiresPriceChangeNotice	RateCategory"

# Product API Info
productAPIInfo = """
altInsertValues("BrandSlug", "brand_slug", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "channel", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "adder", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "backend_source", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "commodity", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "daily_service_charge", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "early_cancellation_fee", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "early_cancellation_fee_cap", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "effective_date", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "expiration_date", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "green_text", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "groupings", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "ista_product_code", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "line_of_business", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "merchandise", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "merchandise_slug", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "merchandise_vesting", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "monthly_service_charge", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "ongoing_frequency", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "ongoing_value", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "partner_code", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "pe_lock_type", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "penalty_type", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "premise_type", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "pricing_term", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "priority_level", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "product_description", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "product_name", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "product_path", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "product_slug", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "promo_code", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "promo_description", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "promo_switch_kitcode", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "rate", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "off_peak_rate", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "rate_category", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "rate_code", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "rate_subclass_code", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "ranking", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "requires_price_change_notice", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "product_eligibility_class", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "signup_bonus", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "signup_vesting", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "state_slug", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "sub_channel", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "terms_of_service_type", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "tos_template", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "utility_rate", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "utility_slug", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "utility_zone", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "vas_code", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "utility_on_peak_rate", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "on_peak_rate", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "utility_off_peak_rate", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "active", rowTarget, sheet, columnHeaderValues)
altInsertValues("BrandSlug", "status", rowTarget, sheet, columnHeaderValues)
"""

# altInsertValues("BrandSlug", "brand_slug", rowTarget, sheet, columnHeaderValues)

# {
#    "count": 1,
#    "next": null,
#    "previous": null,
#    "results": [
#        {
#            "sku": "gbeb96b38c940362",


# redo = True
##print("\nGot to 1\n")
# while(redo):
#    redo = False
#    strIndex = strIndex + 1
#    if (SKUSkipList is None):
#        #Shouldn't ever happen.  Means that SKUSkipList was not initialized correctly.  Just set it to an empty list- [] - or whatever list of forbidden sku's you want before passing it to generateDataForRow.
#        sys.exit("\nSKUSkipList is None.\n")
#    #if(len(SKUSkipList) == 0):
#        #print("\nSKUSkipList has a length of zero.\n")
#    if(strIndex == 100):
#        if (myJ['next'] != "null"):
#            tempJ = requests.get(myJ['next']).json()
#            myJ = tempJ
#            strIndex = 0
#            myJResultsLen = len(myJ['results'])
#        else:
#            aTempList = (someOrderedDict, SKUSkipList, uniqueUANSet, uniqueUIDSet, False)
#            failFile.write("Unable to find a product in the Published Products List that fit user-supplied constraints. failNum =" + str(failNum) + " failed because: Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
#            failFile.close()
#            # print("\ngetRow main loop has ended.  About to return aTempList.\n")
#            return (aTempList)
#            #return "Unable to find a product in the Published Products List that fit user-supplied constraints.\n"
#            #sys.exit("Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
#    if(strIndex >= myJResultsLen):
#        aTempList = (someOrderedDict, SKUSkipList, uniqueUANSet, uniqueUIDSet, False)
#        failFile.write("Unable to find a product in the Published Products List that fit user-supplied constraints. failNum =" + str(failNum) + " failed because: Unable to find a product in the Published Products List that fit user-supplied constraints.\n")
#        failFile.close()
#        # print("\ngetRow main loop has ended.  About to return aTempList.\n")
#        return (aTempList)
#        #return "Unable to find a product in the Published Products List that fit user-supplied constraints.\n"
#        #sys.exit("Unable to find a product in the Published Products List that fit user-supplied constraints.\n")

# wb = openpyxl.Workbook()

# wb.save(excelFile)

# wb.save(excelFileName)

# excelFile.save()
# excelFile.save('text2.xlsx')

# Here's how to deal with column names in openpyxl.
# https://stackoverflow.com/questions/34296132/how-to-use-field-name-or-column-header-in-openpyxl
# https://stackoverflow.com/questions/51975912/get-column-names-of-excel-worksheet-with-openpyxl-in-readonly-mode?rq=1

# Modify the below to set data in your spreadsheet.
# sheet['A1'] = 'hello world'

# sheet.append()

# sheet['A1'] = 'hello world'

# The error
# Product: Product API lookup failure: no products found -- http://products.pt.nrgpl.us/api/v1/products/?active=0&brand_slug=nrg_residential&channel=retention&commodity=electric&partner_code=nrr&pe_lock_type=intro&premise_type=residential&pricing_term=1&priority_level=&product_slug=retention_no_frills_24m&promo_code=524&rate=0.09600&state_slug=pa&terms_of_service_type=variable&utility_slug=penelec&vas_code=006",

# For this run: http://ccc.qa.nrgpl.us/dashboard-pricing-run/e0107d8d-2f6c-4835-9367-9a3a93a8ad48/
# From this Postman call: http://ccc.qa.nrgpl.us/pricing/sync_from_irw/2020-03-24?jobtype=cen&contract_ids=0055680664

# process

# What about sku numbers?

# Have to make sure the sku doesn't preexist, so I might have to do some kind of lookup, too. Or... use the sku that already exists in the product response...

# I'm just going to go with an add one algorithm for now.

# addProductNotFoundToTheBuilderSpreadsheet(file)
# print(os.path.join("/mydir", file))

# should the program download the worksheet for you, too?

# could just have an input file with
# the (usually two letter) environment... though there might be a prod version of this, too, for all I know.
# the api error

# Maybe I'll have an interactive dialogue where it tells you to grab the environment and the product api error, and then where to download the product and where to put it.
# Well... if the environment is part of the api call, maybe I don't have to ask about the environment.

#def reproduceProduct(myJSON):
#    for i in myJSON['results'][0]:
#        altInsertValues(myJSON['results'][0][i])

#Should we have a flag to automatically create products if they're not found?  Just so testers have one less thing to deal with?

# input("The campaign id)
# input("and the offer id so that we can look up the rest of the product info needed for the product builder.\n")

# myJResultsLen = len(myJ['results'])
# strIndex = 0

# myBool = (myJ['results'][strIndex]['sku'] == "null")

# Spaces inbetween lines indicate a column we've already input from the error message.
# This collection will be all excel column names first, then I can filter by what's been done elsewhere if I want.
# Column Names don't have campaign or offer, but they do have promo.
