# Sending emails without attachments using Python.
# importing the required library.
import smtplib

# creates SMTP session
email = smtplib.SMTP('smtp.gmail.com', 587)

# TLS for security
email.starttls()

# authentication
# compiler gives an error for wrong credential.
email.login("testernrgqa@gmail.com", "Tester123")

# message to be sent
message = "message_to_be_send"

# sending the mail
email.sendmail("malyginaleksander@gmail.com", "malyginaleksander@icloud.com", message)

# terminating the session
email.quit()