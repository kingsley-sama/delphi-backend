from core import settings
import resend
from schema import EmailSchema

resend.api_key = settings.RESEND_API_KEY

def send_mail(email_body: EmailSchema) -> resend.Emails.SendResponse:
    params: resend.Emails.SendParams = {
        "from": email_body.from_email,
        "to": email_body.to,
        "subject": email_body.subject,
        "html": email_body.html,
    }
    email: resend.Emails.SendResponse = resend.Emails.send(params)
    return email
