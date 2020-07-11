from datetime import datetime

import xlwt

# Create object of wirkbook

now = datetime.now()
time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
wk = xlwt.Workbook()
ws = wk.add_sheet(time)
# ws.write(0, 0, "testing world")
# ws.write(0, 1, "www.testingworld.com")
#Save workbook
wk.save("./Excel_write.xls")

    #
    # time = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    #
    # f = open("results.txt", 'a')
    # f.write(time)
    # f.write(time + "\n")
    # f.write("Test name: GAS_prices_verify" + "\n")
    # f.write("Tester: Aleksandr" + "\n")
    #
    # gas_pgw_bch_pr_web = self.driver.find_element(By.CSS_SELECTOR,
    #                                               ".plan:nth-child(1) .price:nth-child(1) .price").text
    # gas_pgw_cb_pr_web = self.driver.find_element(By.CSS_SELECTOR, ".plan:nth-child(2) .price .price").text
    # ggas_pgw_bbbs_pr_web = self.driver.find_element(By.CSS_SELECTOR, ".plan:nth-child(3) .price .price").text
    #
    #
    # f.write("Results:" + "\n")
    #
    # ##ACTUAL RESULTS
    # actual_gas_gas_pgw_bch_pr = str(
    #     self.driver.find_element(By.CSS_SELECTOR, ".plan:nth-child(1) .price .price").text)
    # actual_gas_pgw_cb_pr = str(self.driver.find_element(By.CSS_SELECTOR, ".plan:nth-child(2) .price .price").text)
    # actual_ggas_pgw_bbbs = str(self.driver.find_element(By.CSS_SELECTOR, ".plan:nth-child(2) .price .price").text)
    #
    # if gas_pgw_bch_pr_web == gas_pgw_bch_pr:
    #     f.write("gas_pgw_bch_pr price is correct" + "\n")
    # else:
    #     f.write("gas_pgw_cb_pr is wrong: expected result is - " + " " + str(gas_pgw_bch_pr) +
    #             ", " + "actual result is - " + actual_gas_gas_pgw_bch_pr + "\n")
    #
    # if gas_pgw_cb_pr_web == gas_pgw_cb_pr:
    #     f.write("gas_pgw_cb_pr price is correct" + "\n")
    # else:
    #     f.write("gas_pgw_cb_pr is wrong: expected result is - " + " " + str(gas_pgw_cb_pr) +
    #             ", " + "actual result is - " + actual_gas_pgw_cb_pr + "\n")
    #
    # if ggas_pgw_bbbs_pr_web == ggas_pgw_bbbs_pr:
    #     f.write("gas_pgw_cb_pr price is correct" + "\n")
    # else:
    #     f.write("gas_pgw_cb_pr is wrong: expected result is - " + " " + str(ggas_pgw_bbbs_pr) +
    #             ", " + "actual result is - " + actual_ggas_pgw_bbbs + "\n")
    # f.close()