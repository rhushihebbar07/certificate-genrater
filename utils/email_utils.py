import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_certificate_email(name, recipient_email, cert_url):
    sender_email = "donotreplay93@gmail.com"
    sender_password = "pnai waam mzpp stjd"

    subject = "🎓 Your Project Completion Certificate - SMS College"
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px;">
        <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
          <h2 style="color: #1e3a8a;">🎓 Congratulations, {name}!</h2>
          <p>You’ve successfully completed your project. Your certificate is ready. 🏆</p>
          <p style="margin: 20px 0;"><a href="{cert_url}" style="background-color: #1e3a8a; color: white; padding: 12px 20px; border-radius: 5px; text-decoration: none;">🔗 View Your Certificate</a></p>
          <p>If the button doesn’t work, here’s the direct link:<br><a href="{cert_url}">{cert_url}</a></p>
          <hr>
          <p style="font-size: 13px; color: gray;">Saint Mary's Syrian College · Department of Computer Applications</p>
        </div>
      </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email
    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Email failed to send: {e}")
        raise
