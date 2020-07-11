import datetime
from datetime import datetime

# email_addr ="@@12367.890"
# isAtTheRateExist = email_addr.find( '@', 2)
# print( str( isAtTheRateExist ) + " is index of @" )

#
# date = datetime.datetime.now()
# print(date)

now = datetime.now()
current_time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

print(current_time)