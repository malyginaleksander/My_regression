import smtplib, ssl
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "testernrgqa@gmail.com"
receiver_email = "testernrgqa@gmail.com"
password = "Tester123"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)