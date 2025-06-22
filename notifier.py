import smtplib
import ssl

EMAIL_SENDER = 'lmdockweiler@gmail.com'
EMAIL_RECEIVER = 'lennert@lennertdockweiler.com'  # Your alternative email address
EMAIL_PASSWORD = 'knbrjfjmrihywwbo'  # Your Gmail App Password (no spaces)

def send_email(subject, body):
    # Proper encoding for UTF-8 characters like €, ®, etc.
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER

    body_part = MIMEText(body, "plain", "utf-8")
    message.attach(body_part)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message.as_string())
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise