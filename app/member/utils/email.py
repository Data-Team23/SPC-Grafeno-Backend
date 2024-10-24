import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.template.loader import render_to_string


def send_email(to_email, otp_code):
    from_email = settings.EMAIL_HOST_USER
    from_password = settings.EMAIL_HOST_PASSWORD

    html_content = render_to_string('email/opt_verification.html', {'otp_code': otp_code})

    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = "Código de Autenticação 2FA"

    part = MIMEText(html_content, "html")    
    msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.close()
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
