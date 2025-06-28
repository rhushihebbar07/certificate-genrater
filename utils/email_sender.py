# utils/email_sender.py
import smtplib
from email.message import EmailMessage

def send_certificate_email(name, recipient_email, cert_url):
    msg = EmailMessage()
    msg["Subject"] = "🎓 Your Project Completion Certificate - SMS College"
    msg["From"] = "donotreplay93@gmail.com"  # ✅ Explicit sender required
    msg["To"] = recipient_email

    msg.set_content(f"Hi {name},\n\nYour certificate is ready at: {cert_url}")

    msg.add_alternative(f"""
    <html>
      <body>
        <h3>Hi {name},</h3>
        <p>Your GitHub project has been approved.</p>
        <p><a href="{cert_url}">View Your Certificate</a></p>
        <br><p>Regards,<br>SMS College</p>
      </body>
    </html>
    """, subtype='html')

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("donotreplay93@gmail.com", "pnai waam mzpp stjd")
            smtp.send_message(msg)
    except Exception as e:
        print(f"Email error: {e}")
