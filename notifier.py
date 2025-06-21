
import smtplib
import ssl
EMAIL_SENDER = 'lmdockweiler@gmail.com'
EMAIL_RECEIVER = 'dockweiler.lennert@gmail.com'
EMAIL_PASSWORD = 'knbrjfjmrihywwbo'  # your App Password (without spaces)


def send_email(subject, body):
    message = f"Subject: {subject}\n\n{body}"
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_email(subject, body):
    msg = f"Subject: {subject}\n\n{body}"
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg)
        server.quit()
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")