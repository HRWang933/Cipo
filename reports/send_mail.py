#############################################################################
# Send mail handler
#############################################################################
import smtplib
import ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.base import MIMEBase
from email import encoders

def send_mail(params):

    assert isinstance(params.get('send_to'), list)

    msg = MIMEMultipart()
    msg['From'] = params.get('send_from')
    msg['To'] = COMMASPACE.join(params.get('send_to'))
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = params.get('subject')

    msg.attach(MIMEText(params.get('text')))

    if params.get('attach_file') !='':
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(params.get('attach_file') , "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(params.get('attach_file')))
        msg.attach(part)

    for f in params.get('files') or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    if params.get('as_table'):
        part2 = MIMEText(params.get('table_html'), 'html')
        msg.attach(part2)

    context=ssl.create_default_context()
    smtp = smtplib.SMTP(params.get('server'),25)
#    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#    smtp.ehlo()
#    smtp.login(params.get('username'),params.get('password'))
    smtp.sendmail(params.get('send_from'), params.get('send_to'), msg.as_string())
    smtp.close()
