python CTGLauncherPlus.py will go from InboundFileProcessing all the way through the last steps of CTG(including the Enrollment and Pricing stored procedures).
If you just want to run the CTG stuff, comment out these lines in CTGLauncherPlus.py with a #:

    g.sql_run_job_synchronously("Fileprocessing.InboundFileProcessing", None, "wait_Til_Completion_To_Run_Again")
    g.sql_run_job_synchronously("New Enrollment Processing", None, "wait_Til_Completion_To_Run_Again")
    g.sql_run_job_synchronously("ESG Enrollment Export", None, "wait_Til_Completion_To_Run_Again")

If you want to change the environment from QA to PT just edit CTGLauncherPlus.py

If you want to change the date in the edi manually, just edit CTG.CTGProcess(None) in CTGLauncherPlus.py to be CTG.CTGProcess("2019-02-03")
or whatever date in that format you want.  Otherwise the program automatically uses (local time, not server time) today's date.  An area for improvement.  Known issue / bug.

Note that this is a rough launcher and does not check for results like falling into staging.  That functionality is in FileEnrollment(a different program not in this folder), which is not yet ready for prime time.

To use this, you'll need to be connected to an NRG-privileged network, like with a Philadelphia or Princeton office ethernet cable, or over the VPN at home.