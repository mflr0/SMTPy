import smtplib
from email.mime.text import MIMEText

def send_mail(server: str, port: int, username: str, password: str,
              sender: str, recipients: list[str], subject: str, body: str) -> None:
    """Envoie un mail en SMTP."""
    msg = MIMEText(body, 'html')
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject

    with smtplib.SMTP(server, port) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(sender, recipients, msg.as_string())
