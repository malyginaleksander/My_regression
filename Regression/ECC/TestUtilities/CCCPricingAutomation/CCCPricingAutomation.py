import cx_Oracle

#Far from finished- this is the kind of stuff you'd need to interact with the oracle database, plus some information on CEN warning intervals.

#Use this https://www.timeanddate.com/date/durationresult.html?d1=26&m1=6&y1=2019&d2=25&m2=8&y2=2019&ti=on& for calculating the time between dates.
#Use this for determining how far out the cen should be sent out(can be more, I think): https://ccc.pt.nrgpl.us/admin/pricing/correspondencefulfillmentterms/

#Notice there's a description for both kinds of PA CEN's.
#STATE CORRESPONDENCE TYPE EFFECTIVE DATE COMMENT REQUIRED DAYS BUFFER DAYS
#CT      cen1	            Jan. 1, 2017	 	    45	           10
#DC      cen1	            Jan. 1, 2017	 	    45	           10
#DE      cen1	            Jan. 1, 2017	 	    45	           10
#MD      cen1	            Jan. 1, 2017	 	    45	           10
#NY      cen1	            Jan. 1, 2017	 	    45	           10
#OH      cen1	            Jan. 1, 2017	 	    45	           10
#PA      cen1	            Jan. 1, 2017	 	    45	           10
#PA      cen2	            Jan. 1, 2017	 	    32	           10
#Notice there's a description for both kinds of PA CEN's.

#conn_str = u'user/password@host:port/service'
conn_str = u'NE_PRICING_ENGINE_USR/Ne_pricing_usr#0@rtldwt01.reinternal.com:1531/TCST1N'
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()
forbiddenAccountListString = "()"
#utilityString = "and utility_name = 'COMMONWEALTH EDISON'"
brandRepOwnrIdString = "and REP_OWNR_ID in ('0393')"
utilityString = ""
#Should be able to automate getting the current date and then looking up the day that will be 60 days from now... maybe I can just use 60 days as a substitute for now?
#This would be a good reason to - normally- only search one state at a time.  Or at least stay within the same CEN send-out window.
myQuery = """
select * from TCS.nrp_pricing_customer_v where state = 'PA' and CNTR_END_DT >= '26-AUG-19' and CNTR_END_DT < '26-AUG-22'
and NY_LIDA_FLAG is null and Future_swap_flag is null and not in %s %s %s order by cntr_end_dt asc
""" % (forbiddenAccountListString, brandRepOwnrIdString, utilityString)
#Verify contract_start_date and contract_end_date id more than 3 months apart ( not a 3 month product)

myScheduleQuery = """
select * from TCS.TE418_V where TERMSCHL = 'MRU_from_pricing_customer_v' ORDER BY TERMTDAT
"""
c.execute(myQuery)
for row in c:
    print(row)
conn.close()
#Run a postman (request) query to make a pricing call.
