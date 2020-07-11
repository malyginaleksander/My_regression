import GenericSettings as g
import CTG
import atexit

def main():
    g.initializeConn()
    g.setMyEnvironment("QA")
    tempString = 'WNTEPNSQLTQ1\\' + g.getMyEnvironment()
    g.safelySetMSSQLConnection(tempString)
    g.safelySetPGSQLConnectionFromEnv(g.getMyEnvironment())
    atexit.register(g.exit_handler)
    
    g.sql_run_job_synchronously("Fileprocessing.InboundFileProcessing", None, "wait_Til_Completion_To_Run_Again")
    g.sql_run_job_synchronously("New Enrollment Processing", None, "wait_Til_Completion_To_Run_Again")
    g.sql_run_job_synchronously("ESG Enrollment Export", None, "wait_Til_Completion_To_Run_Again")
    CTG.CTGProcess(None)
   
if __name__ == '__main__':
    # sys.settrace(trace_calls)
    main()