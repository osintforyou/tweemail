import smtplib, ssl, email
from twitter import tweets_df #twitter.py is the second file, handling the scrapping part of the program
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

tweets_df.head()

sender_email ="sender_email_address" #Add the email address which will send the email.
receiver_email = "John.Doe@JaneDoe.com" #Add the email address which will receive the email.
password = "sender_email_password" #Add the password for the sender email.

#Create MIMEMultipart object
msg = MIMEMultipart("alternative")
msg["Subject"] = "Latest News from Twitter"
msg["From"] = sender_email
msg["To"] = receiver_email
filename = "raw_data.html"

#HTML Message Part
html = """\
<html>
  <body>
    <p><b>Latest News from Twitter</b>
    <br><br>
       Please see the latest update in the attached HTML file.<br><br>
       Kind regards,<br><br>
    </p>
  </body>
</html>
"""

part = MIMEText(html, "html")
msg.attach(part)

# Add Attachment
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
   
encoders.encode_base64(part)

# Set mail headers
part.add_header(
    "Content-Disposition",
    "attachment", filename= filename
)
msg.attach(part)

# Create secure SMTP connection and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, msg.as_string()
    )
