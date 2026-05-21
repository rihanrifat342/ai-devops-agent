import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration

sender_email = "rihanrifat342@gmail.com"

receiver_email = "mohammed.rihan342@gmail.com"

app_password = "oyws lrct uzib plsx"

# Email content

subject = "🚨 CRITICAL ALERT - AI DevOps Agent"

body = """
Critical issue detected by AI DevOps Agent.

Possible anomaly detected:
- High CPU usage
- Container failure
- Infrastructure instability

Immediate attention required.
"""

# Create email

message = MIMEMultipart()

message["From"] = sender_email

message["To"] = receiver_email

message["Subject"] = subject

message.attach(MIMEText(body, "plain"))

try:

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        app_password
    )

    server.send_message(message)

    server.quit()

    print("Email alert sent successfully!")

except Exception as e:

    print("Failed to send email.")

    print(e)