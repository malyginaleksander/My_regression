from datetime import datetime
import uuid

# now = datetime.now()
# current_time = now.strftime("_%m_%d_%Y_%I_%M_%S_%p_")
# textfiles = "../GME/GME_regression/TextFileConfirmations/GME_{}_{}".format("test", uuid.uuid4())
#
# file = open(textfiles + str(current_time) + ".txt", 'a')
# file.write("hello")



now = datetime.now()
current_time = now.strftime("_%m_%d_%Y_%I_%M_%S_%p_")
textfiles = "./TextFileConfirmations/gme".format("test", uuid.uuid4())
            # 'C:\Users\AMALYGIN\Downloads\Regression-master (5)\Regression-master\Regression\States\for_me.py'
file = open(textfiles + str(current_time) + ".txt", 'a')
file.write("hello")



