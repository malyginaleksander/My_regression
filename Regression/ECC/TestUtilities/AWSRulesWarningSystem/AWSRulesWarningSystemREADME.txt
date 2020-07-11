The program AWSRulesWarningSystem.pyw monitors Cloudwatch rules on a ten minute interval(which can be changed by opening the script and changing time.sleep(600) to however many seconds you want.
If it detects a rule has changed, the program will create a popup with information about the changed rules.  Perhaps let other employees know
in chat, and then reset or change the program's configuration as described below in "Is this a rule change you're okay with?"

Include (full address here).....\TestUtilities\UtilitySupportModules in your PythonPath variable or Python won't be able to find modules this program needs.  You can also look there to find the helper modules like GenericSettings.py
and "peek under the hood" and change internal program logic.

It is highly recommended that users set this program as a scheduled event in their operating system, as with Windows Scheduler(which you can search in the Windows search bar).  That way it can just run on a set schedule
every day and you don't need to worry about forgetting to turn it on.  It can't warn you about problems if you don't turn it on or schedule it.

Updates: 1/25/2019: Now handles rule descriptions (.json's) with a variable number of fields named unpredictable things.
Gracefully informs the user with a messagebox when there's a rule in AWSRulesFile.txt but no rule description (.json) file for it.  Tells the user how to fix that and then exits smoothly on clicking OK.
Added a warning to the readme about trying to schedule this program for running when no one's logged in(GUI programs can't do that on Windows, though they can run-even create new windows- while the screen's locked).
Verified that the program runs, even creates windows while the screen's locked.

Setup:
First, to use this most effectively remember to include new rules you start to care about for XYZ project in the rules file.  This program can't warn you about rule changes if you don't add the rules!  And then make sure
to run the AWSRuleDescriptionGenerator.py before running the program or the program won't know what to expect from the new rule, and will exit with an informative warning message about this situation.
Also, this a reactive program, not a preventative one- your first line of defense is always letting people know "Hey, I'm working on XY project that uses rule Z, if you're going to mess with rule Z ask me first."
and then update people when you're done with it.  And when you're done with that rule, consider removing the rule from your AWSRulesFile.txt rules file.  The old RuleDescription .json won't hurt anything if there's not a rule
in the AWSRulesFile.txt file pointing to it, but you can delete if you feel like it.

When updating the AWSRulesFile.txt rules file, make sure you enter the relevant aws environment with the rule, like --profile=prod for PT(or prod, but those rules haven't been tested with this program) and --profile=qa for QA.
0.  Include (full address here).....\TestUtilities\UtilitySupportModules in your PythonPath variable or Python won't be able to find modules this program needs.
1. Set the rules in AWSRulesFile.txt.  To do so, get the name of the rule from aws and add on the -- options you'll want.  Usually you'll want --profile=YourParticularEnvironment and --region=us-east-1 or the name of your AWS region.
Make sure each rule in the text file gets its own line.  If you're curious, the command this program runs to get information on rules is: "aws events describe-rule --name " + the rule's name, including the options in AWSRulesFile.txt.
2. Manually examine the rules you care about in AWS and make sure they have the settings you want- especially "State" and "ScheduleExpression".
3. If for some reason there is a rule that is currently not in the state you'd like, you can create an expected response file for the settings you'd like.  Follow step 4 and then open the .json file containing your rule's name.
Manually edit the variable values to what you want them to be.  You can get an idea of the kinds of valid values from trying aws describe-rule on different rules, but in general the only variable that has a tricky response is
ScheduleExpression... if you see a rate of 2 hours, that will come back from the aws describe-rule command as "rate(2 hours)"   without the quotes.
4. Then run Python AWSRuleDescriptionGenerator.py  Then make sure you go on to step 5 as normal(again).

To Run:
5. Open a terminal in the file's directory and enter "python AWSRulesWarningSystem.pyw".

Continued Operation:
If the program detects a rule has changed, the program will create a popup with information about the changed rules.  When it does this, decide:

Optimal Operation Method:
Set up a Windows scheduled task with TaskScheduler(enter it in your Windows search bar).  Set the options to:
Under tab General, heading Security Options, select "Run only when user is logged on."  Tasks with GUI elements can not run when a user is not logged in BUT once a user has logged in, screen locks don't affect it.
Under tab General, set Configure for: to your operating system- I selected Windows 10.
Under tab Triggers, select new and set "Begin the Task" to At log on".  This is the only setting this is verified to work with.  Use others at your own risk.  Click OK.
Under tab Actions, select New then set Action to "Start a program", set Program/script to C:\\Users\\mhissong\\AppData\\Local\\Programs\\Python\\Python37\\python.exe or whatever your path is to the python executable.
Set "Add arguments(optional)" to: C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\AWSRulesWarningSystem\\AWSRulesWarningSystem.pyw or your path to the AWSRulesWarningSystem.pyw file.
Set "Start in(optional)" to: C:\Users\mhissong\Desktop\Regression\Regression\ECC\TestUtilities\AWSRulesWarningSystem\ or the path to AWSRulesWarningSystem.pyw 's native/containing folder
(should be your computer's specific path and then \Regression\Regression\ECC\TestUtilities\AWSRulesWarningSystem\).  Hit OK.
Look at the Conditions tab and make sure you're comfortable with them... I turned off the "Start task only if the computer is on AC Power" and "Stop if the computer switches to battery power."
Under tab Settings, select "Allow task to be run on demand", Run task ASAP... If the task fails... (5 minutes)... Attempt to restart up to 3 times(though you could set it higher, should only matter if there's an issue at Amazon),
Stop the task... (3 days), If the running task does not end... and then RE: the "If the task is already running" drop down, select "Do not start a new instance."
Click OK.
The AWSRulesWarningSystem.pyw should now run at logon, remain through screen locks, and be there to tell you when someone changes a rule!

Is this a rule change that you're okay with?

A) Yes.  Execute step 4 above, for recreating the expected response files.

B) No.  Either:

    1) Confer with other employees and, if the change was inappropriate, ask the changer to change it back.

    2) Open AWSRulesWarningSystem.pyw and look for time.sleep().  The value inside is in seconds.  Right now it's 600, which is ten minutes.  Change it to whatever interval you want the program to check the rules at, but
remember, this applies to ALL the rules.  So if you want a timely warning about other rules, consider:

    3) Take the rule out of your AWSRulesFile.txt file temporarily.  Set a reminder for yourself in Outlook and put it back in when you feel like it or the rule change you don't like is reverted.  This way you still get information
about all the other rules in a timely fashion.
    or
    4) Open task manager with ctrl-alt-delete(or your OS' equivalent), select the program(usually just called "Python") and terminate it.  Open the program again when you feel like checking on the rules.  You won't get any information
about the rules until you open the program again, but it's a very quick solution.

Known Issues: 
If you schedule the program with Windows scheduler, you'll probably see a Python program icon, and can quit out of that to close the program.  If you don't, the program can't be terminated
without an OS' task manager equivalent or without shutting down the computer.
If the program is run from a terminal you can just close the terminal or hit ctrl-C repeatedly, then enter to see if the machine successfully interrupted the program.
It's designed to run without a terminal(ideally scheduled by the os) so that it doesn't clutter up the user's workspace.  Usually it's time.sleep()-ing
except every 10 minutes when it checks the AWS Cloudwatch rules.  It has about a 7.6 MB RAM footprint on my machine.

Possible Issues:
If Python tells you you don't have a module, type pip install ThatModuleName.  If you don't have pip, download and install it.

Tests:
There are three test folders included.  One for a clean, happy path test, one for every "logical" (expected) failure in a single test case, and another with a single logical failure.

Why are these test folders significant?   They contain the modified "expected response files" you'll need for the test cases described in the folder names.  Or you can modify expected response files yourself!  To get an AWS response
manually, run "aws events describe-rule --name " + the rule's name, including the options for your environment(probably qa or pt, like --profile=prod or --profile=qa) and your aws region --region=us-east-1.  In general, the only
tricky response is for ScheduleExpression... if you see a rate of 2 hours in aws, that will come back from the aws describe-rule command as "rate(2 hours)".  So you just have to know the formatting there.

Example: "aws events describe-rule --name pt-ecc-bounce_check_event_trigger --profile=prod --region=us-east-1"
