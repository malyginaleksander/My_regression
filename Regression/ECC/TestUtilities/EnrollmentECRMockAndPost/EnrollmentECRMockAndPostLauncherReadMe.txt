Program Purpose: Mock(copy, with slight alterations to make it unique) an enrollment_candidate_received json file and post it to the s3 bucket in the appropriate environment(qa or pt).
Special Note: This program uses a launcher called EnrollmentECRMockAndPostLauncher.py.  This readme will refer to that, although behind the scenes EnrollmentECRMockAndPost.py is doing the work(but EnrollmentECRMockAndPost's
functions aren't callable directly, it has no main() function, so that program can't be called).  EnrollmentECRMockAndPost.py should be in the TestUtilities\UtilitySupportModules folder, if you're looking for it.
Same with GenericSettings.py, a helper utility EnrollmentECRMockAndPost.py uses.

Include (full address here).....\TestUtilities\UtilitySupportModules in your PythonPath variable or Python won't be able to find modules that the launcher / its service program need.  You can also look there to find the
helper modules like EnrollmentECRMockAndPost.py and GenericSettings.py and "peek under the hood" to view / change internal program logic.

Authors: Matt Hissong, with some code from Chris Wolf.  To see Chris' main code, ask him about getting a copy of eccutil.py.

Update: 1/25/2019- Now has a separate launcher program named EnrollmentECRMockAndPostLauncher.py.  The program EnrollmentECRMockAndPost.py has been moved to TestUtilities\UtilitySupportModules.
The modularization from the launcher program allows other programs to include EnrollmentECRMockAndPost as a module and use its functions directly.

User instructions:
Have the standard Python 3.5 environment.

Open EnrollmentECRMockAndPostLauncher.py in a text editor and change:
this path to the path of the enrollment_candidate_received json you want to mock(mocking means "copy with slight alterations to make it unique") and the environment you want the ecr posted to in s3- "QA" or "PT"
ECRMockingHelper("C:\\Users\\mhissong\\Desktop\\Regression\\Regression\\ECC\\TestUtilities\\EnrollmentECRMockAndPost\\3e411696-2e43-4cb1-9299-29ec6e28b78b.json", "PT")

To execute:  First, set up your AWS (Amazon Web Services) credentials for whether you want to post to QA or PT on AWS-s3.  Important note: Prod currently uses the same aws credentials profile as PT.
The program uses the names "qa" and "prod" for the profile names in its sessions, so name your profiles like that.  

Once you have your AWS credentials set up, just enter python EnrollmentECRMockAndPostLauncher.py at the command prompt where EnrollmentECRMockAndPostLauncher.py is.

Output: The program will write the mocked file to the same folder with an incremented string name(digits get one added, letters go up one).  If you already have a file with that name in the folder, the program will overwrite it.

Any possible issues? -

To use this, you'll need to be connected to an NRG-privileged network, like with a Philadelphia or Princeton office ethernet cable, or over the VPN at home.

If you see an error about not posting to s3, you probably misread / mistook the aws credentials directions above.  Reread them and try to rerun.  If you still have problems,
you can take the output file in your directory- which will have a slightly incremented filename- like XYZ1.json would be XYZ2.json- and put it in QA's or PT's s3 folder yourself.  Which is at:
 
https://s3.console.aws.amazon.com/s3/buckets/nrg-portal-qa/business_events/enrollment_candidate_received/ insert today's date here   /nerf/  insert confirmation code aka UID here   /   insert filename here   .json
or, for PT:
https://s3.console.aws.amazon.com/s3/buckets/nrg-portal-pt/business_events/enrollment_candidate_received/ insert today's date here   /nerf/  insert confirmation code aka UID here   /   insert filename here   .json

If Python tells you you don't have a module, type pip install ThatModuleName.  If you don't have pip, download and install it.
