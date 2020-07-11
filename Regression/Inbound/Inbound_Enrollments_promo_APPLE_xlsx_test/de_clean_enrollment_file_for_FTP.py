import csv
import os

from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test.InboundPromo_tests_Settings import test_name

directory_for_file_from_zookeeper = './ce_file_from_zookeeper/'
files_dir = os.listdir('./ce_file_from_zookeeper/')
csv_file = './ce_file_from_zookeeper/csv_file_for_cleaning_.csv'
final_file = './ce_file_from_zookeeper/cleaned_filed_in_csv.csv'
directory_for_testing_data_file = "./c_web_test_result/"
testResult_file_dir = os.listdir(directory_for_testing_data_file)
query_files_list = []
for name in os.listdir(directory_for_testing_data_file):
    test_result_file = str(str(directory_for_testing_data_file)+str(name))
test_result_dict = csv.DictReader(open(test_result_file))




def test_formating_files_to_csv():
    print("\nFormating files started...")

    for name in files_dir:
        with open((directory_for_file_from_zookeeper + name), 'r') as infile, open(
                ('./ce_file_from_zookeeper/csv_file_for_cleaning_.csv'), 'w') as outfile:
            stripped = (line.strip() for line in infile)
            lines = (line.split("\t") for line in stripped if line)
            writer = csv.writer(outfile)
            writer.writerows(lines)

    print("Formated TXT to CSV\n ")


adresses_list = []




test_formating_files_to_csv()
base_file = csv.DictReader(open(csv_file))
for row in base_file:
    dict = row
    UID = dict.get('UID', '')
    Sequencer = dict.get('Sequencer', '')
    MID = dict.get('MID', '')
    Application_Type = dict.get('Application Type', '')
    FirstName = dict.get('FirstName', '')
    MiddleInit = dict.get('MiddleInit', '')
    LastName = dict.get('LastName', '')
    SuffixName = dict.get('SuffixName', '')
    PriorityLevel = dict.get('PriorityLevel', '')
    Business_Name = dict.get('Business Name', '')
    RevenueClass = dict.get('RevenueClass', '')
    Service_Phone = dict.get('Service Phone', '')
    Service_Extension = dict.get('Service Extension', '')
    Service_Address1 = dict.get('Service Address1', '')
    Service_Address2 = dict.get('Service Address2', '')
    Service_City = dict.get('Service City', '')
    Service_State = dict.get('Service State', '')
    Service_Zip = dict.get('Service Zip', '')
    Service_Zip4 = dict.get('Service Zip4', '')
    Service_County = dict.get('Service County', '')
    Billing_Phone = dict.get('Billing Phone', '')
    Billing_Extension = dict.get('Billing Extension', '')
    Billing_Address1 = dict.get('Billing Address1', '')
    Billing_Address2 = dict.get('Billing Address2', '')
    Billing_City = dict.get('Billing City', '')
    Billing_State = dict.get('Billing State', '')
    Billing_Zip = dict.get('Billing Zip', '')
    Billing_Zip4 = dict.get('Billing Zip4', '')
    Billing_County = dict.get('Billing County', '')
    Attention_Line = dict.get('Attention Line', '')
    email = dict.get('email', '')
    Service_type = dict.get('Service type', '')
    ISO_region = dict.get('ISO region', '')
    TaxExemption = dict.get('TaxExemption', '')
    BillMethod = dict.get('BillMethod', '')
    EnrollType = dict.get('EnrollType', '')
    RequestStartDate = dict.get('RequestStartDate', '')
    Utility_Code = dict.get('Utility Code', '')
    UtilityAccountNumber = dict.get('UtilityAccountNumber', '')
    Rate_Class = dict.get('Rate Class', '')
    Promo_Code = dict.get('Promo Code', '')
    Rep_ID = dict.get('Rep ID', '')
    Campaign_ID = dict.get('Campaign ID', '')
    Cell_Code = dict.get('Cell Code', '')
    Date_of_Sale = dict.get('Date of Sale', '')
    Partner_Code = dict.get('Partner Code', '')
    Partner_Member_Number = dict.get('Partner Member Number', '')
    Authorization_Accepted = dict.get('Authorization Accepted', '')
    Agreement_Accepted = dict.get('Agreement Accepted', '')
    Confirmation_Number = dict.get('Confirmation Number', '')
    Time_of_Sale = dict.get('Time of Sale', '')
    Green = dict.get('Green', '')
    Referral_ID = dict.get('Referral ID', '')
    IP_Address = dict.get('IP Address', '')
    Budget_Billing = dict.get('Budget Billing', '')
    Entered_By = dict.get('Entered By', '')
    App_Taken_By = dict.get('App Taken By', '')
    Name_Key = dict.get('Name Key', '')
    BAcctNum = dict.get('BAcctNum', '')
    IntroGroup = dict.get('IntroGroup', '')
    MKGroup = dict.get('MKGroup', '')
    PartnerFirstName = dict.get('PartnerFirstName', '')
    PartnerLastName = dict.get('PartnerLastName', '')
    EnrollCustID = dict.get('EnrollCustID', '')
    FICO = dict.get('FICO', '')
    PaymentSource = dict.get('PaymentSource', '')
    PaymentMethod = dict.get('PaymentMethod', '')
    PaymentAmount = dict.get('PaymentAmount', '')
    contractterm = dict.get('contractterm', '')
    SpanishBill = dict.get('SpanishBill', '')
    notificationwaiver = dict.get('notificationwaiver', '')
    BirthDate = dict.get('BirthDate', '')
    MotherMaiden = dict.get('MotherMaiden', '')
    TaxID = dict.get('TaxID', '')
    Credit1 = dict.get('Credit1', '')
    credit2 = dict.get('credit2', '')
    AvgBill = dict.get('AvgBill', '')
    RentOwn = dict.get('RentOwn', '')
    ResidenceLength = dict.get('ResidenceLength', '')
    EmployeeCount = dict.get('EmployeeCount', '')
    BusinessLength = dict.get('BusinessLength', '')
    CurrentSupplier = dict.get('CurrentSupplier', '')
    spfname = dict.get('spfname', '')
    splname = dict.get('splname', '')
    InitialOffer_ChargeID = dict.get('InitialOffer_ChargeID', '')
    FixedIntro = dict.get('FixedIntro', '')
    years_inbiz = dict.get('years_inbiz', '')
    years_bizaddr = dict.get('years_bizaddr', '')
    late_payment6 = dict.get('late_payment6', '')
    busname_change = dict.get('busname_change', '')
    elec_supp_prevyear = dict.get('elec_supp_prevyear', '')
    years_creditbiz = dict.get('years_creditbiz', '')
    RiskQuestion1 = dict.get('RiskQuestion1', '')
    RiskQuestion2 = dict.get('RiskQuestion2', '')
    RiskQuestion3 = dict.get('RiskQuestion3', '')
    campaign_version = dict.get('campaign_version', '')
    brand_slug = dict.get('brand_slug', '')
    sku = dict.get('sku', '')
    export_job_id = dict.get('export_job_id', '')
    tos_version = dict.get('tos_version', '')
    ConsentPhone = dict.get('ConsentPhone', '')
    ConsentEmail = dict.get('ConsentEmail', '')
    ConsentData = dict.get('ConsentData', '')
    ConsentCompanies = dict.get('ConsentCompanies', '')
    AgentId = dict.get('AgentId', '')
    Rep_First_Name = dict.get('Rep First Name', '')
    Rep_Last_Name = dict.get('Rep Last Name', '')
    call_direction = dict.get('call_direction', '')

    for row in test_result_dict:
        dict = row
        ServiceAddress1 = dict.get('ServiceAddress1', '')
        print(dict)

        if Service_Address1==ServiceAddress1:
            if Service_Address1 in adresses_list:
                pass
            else:
                adresses_list.append(Service_Address1)


                if os.path.isfile(final_file):
                    f = open(final_file, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow([UID, Sequencer, MID, Application_Type, FirstName, MiddleInit, LastName, SuffixName,
                                    PriorityLevel, Business_Name, RevenueClass, Service_Phone, Service_Extension,
                                    Service_Address1, Service_Address2, Service_City, Service_State, Service_Zip,
                                    Service_Zip4, Service_County, Billing_Phone, Billing_Extension, Billing_Address1,
                                    Billing_Address2, Billing_City, Billing_State, Billing_Zip, Billing_Zip4,
                                    Billing_County, Attention_Line, email, Service_type, ISO_region, TaxExemption,
                                    BillMethod, EnrollType, RequestStartDate, Utility_Code, UtilityAccountNumber,
                                    Rate_Class, Promo_Code, Rep_ID, Campaign_ID, Cell_Code, Date_of_Sale, Partner_Code,
                                    Partner_Member_Number, Authorization_Accepted, Agreement_Accepted,
                                    Confirmation_Number, Time_of_Sale, Green, Referral_ID, IP_Address, Budget_Billing,
                                    Entered_By, App_Taken_By, Name_Key, BAcctNum, IntroGroup, MKGroup, PartnerFirstName,
                                    PartnerLastName, EnrollCustID, FICO, PaymentSource, PaymentMethod, PaymentAmount,
                                    contractterm, SpanishBill, notificationwaiver, BirthDate, MotherMaiden, TaxID,
                                    Credit1, credit2, AvgBill, RentOwn, ResidenceLength, EmployeeCount, BusinessLength,
                                    CurrentSupplier, spfname, splname, InitialOffer_ChargeID, FixedIntro, years_inbiz,
                                    years_bizaddr, late_payment6, busname_change, elec_supp_prevyear, years_creditbiz,
                                    RiskQuestion1, RiskQuestion2, RiskQuestion3, campaign_version, brand_slug, sku,
                                    export_job_id, tos_version, ConsentPhone, ConsentEmail, ConsentData,
                                    ConsentCompanies, AgentId, Rep_First_Name, Rep_Last_Name, call_direction,
                                    ])
                else:
                    f = open(final_file, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow(
                        ['UID', 'Sequencer', 'MID', 'Application_Type', 'FirstName', 'MiddleInit', 'LastName',
                         'SuffixName', 'PriorityLevel', 'Business_Name', 'RevenueClass', 'Service_Phone',
                         'Service_Extension', 'Service_Address1', 'Service_Address2', 'Service_City', 'Service_State',
                         'Service_Zip', 'Service_Zip4', 'Service_County', 'Billing_Phone', 'Billing_Extension',
                         'Billing_Address1', 'Billing_Address2', 'Billing_City', 'Billing_State', 'Billing_Zip',
                         'Billing_Zip4', 'Billing_County', 'Attention_Line', 'email', 'Service_type', 'ISO_region',
                         'TaxExemption', 'BillMethod', 'EnrollType', 'RequestStartDate', 'Utility_Code',
                         'UtilityAccountNumber', 'Rate_Class', 'Promo_Code', 'Rep_ID', 'Campaign_ID', 'Cell_Code',
                         'Date_of_Sale', 'Partner_Code', 'Partner_Member_Number', 'Authorization_Accepted',
                         'Agreement_Accepted', 'Confirmation_Number', 'Time_of_Sale', 'Green', 'Referral_ID',
                         'IP_Address', 'Budget_Billing', 'Entered_By', 'App_Taken_By', 'Name_Key', 'BAcctNum',
                         'IntroGroup', 'MKGroup', 'PartnerFirstName', 'PartnerLastName', 'EnrollCustID', 'FICO',
                         'PaymentSource', 'PaymentMethod', 'PaymentAmount', 'contractterm', 'SpanishBill',
                         'notificationwaiver', 'BirthDate', 'MotherMaiden', 'TaxID', 'Credit1', 'credit2', 'AvgBill',
                         'RentOwn', 'ResidenceLength', 'EmployeeCount', 'BusinessLength', 'CurrentSupplier', 'spfname',
                         'splname', 'InitialOffer_ChargeID', 'FixedIntro', 'years_inbiz', 'years_bizaddr',
                         'late_payment6', 'busname_change', 'elec_supp_prevyear', 'years_creditbiz', 'RiskQuestion1',
                         'RiskQuestion2', 'RiskQuestion3', 'campaign_version', 'brand_slug', 'sku', 'export_job_id',
                         'tos_version', 'ConsentPhone', 'ConsentEmail', 'ConsentData', 'ConsentCompanies', 'AgentId',
                         'Rep_First_Name', 'Rep_Last_Name', 'call_direction',
                         ])
                    csv_a.writerow([UID, Sequencer, MID, Application_Type, FirstName, MiddleInit, LastName, SuffixName,
                                    PriorityLevel, Business_Name, RevenueClass, Service_Phone, Service_Extension,
                                    Service_Address1, Service_Address2, Service_City, Service_State, Service_Zip,
                                    Service_Zip4, Service_County, Billing_Phone, Billing_Extension, Billing_Address1,
                                    Billing_Address2, Billing_City, Billing_State, Billing_Zip, Billing_Zip4,
                                    Billing_County, Attention_Line, email, Service_type, ISO_region, TaxExemption,
                                    BillMethod, EnrollType, RequestStartDate, Utility_Code, UtilityAccountNumber,
                                    Rate_Class, Promo_Code, Rep_ID, Campaign_ID, Cell_Code, Date_of_Sale, Partner_Code,
                                    Partner_Member_Number, Authorization_Accepted, Agreement_Accepted,
                                    Confirmation_Number, Time_of_Sale, Green, Referral_ID, IP_Address, Budget_Billing,
                                    Entered_By, App_Taken_By, Name_Key, BAcctNum, IntroGroup, MKGroup, PartnerFirstName,
                                    PartnerLastName, EnrollCustID, FICO, PaymentSource, PaymentMethod, PaymentAmount,
                                    contractterm, SpanishBill, notificationwaiver, BirthDate, MotherMaiden, TaxID,
                                    Credit1, credit2, AvgBill, RentOwn, ResidenceLength, EmployeeCount, BusinessLength,
                                    CurrentSupplier, spfname, splname, InitialOffer_ChargeID, FixedIntro, years_inbiz,
                                    years_bizaddr, late_payment6, busname_change, elec_supp_prevyear, years_creditbiz,
                                    RiskQuestion1, RiskQuestion2, RiskQuestion3, campaign_version, brand_slug, sku,
                                    export_job_id, tos_version, ConsentPhone, ConsentEmail, ConsentData,
                                    ConsentCompanies, AgentId, Rep_First_Name, Rep_Last_Name, call_direction,
                                    ])

# print("min idoc#:  "+ str(min(idoc_list)))
# print("max idoc#:  "+ str(max(idoc_list)))
