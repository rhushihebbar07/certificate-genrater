import smtplib
from email.message import EmailMessage

def send_certificate_email(name, email, cert_url):
    msg = EmailMessage()
    msg.set_content(f"Hi {name},\n\nYour certificate is ready at: {cert_url}")
    msg["Subject"] = "Your Project Completion Certificate"
    msg["From"] = "your_email@example.com"
    msg["To"] = email

    # Use your real credentials here
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("donotreplay93@gmail.com", "pnai waam mzpp stjd")
        smtp.send_message(msg)
