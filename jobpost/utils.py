from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def email_template(name, status):
    html = """
            <!DOCTYPE html>
            <html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <meta name="x-apple-disable-message-reformatting">
            <title></title>
            <!--[if mso]>
            <noscript>
                <xml>
                <o:OfficeDocumentSettings>
                    <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
                </xml>
            </noscript>
            <![endif]-->
            <style>
                table, td, div, h1;
            </style>
            </head>
            <body style="margin:0;padding:0;">
            <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
                <tr>
                <td align="center" style="padding:0;">
                    <table role="presentation" style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
                    <tr>
                        <td align="center" style="padding:40px 0 30px 0;background:#eff7fd;">
                        <img src="https://peso.davaocity.gov.ph/wp-content/uploads/2020/06/logo_peso.png" alt="" width="200" style="height:auto;display:block;" />
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:36px 30px 42px 30px;">
                        <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                            <tr>
                            <td style="padding:0 0 36px 0;color:#153643;">
                                <h1 style="font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">Hi {name}</h1>
                                <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">
                                Thank You for sending your application. We would like to inform you that your application is {status}. <br>
                                Please log in to your PESO Online account for the next step.
                                </p>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:30px;background:#ee4c50;">
                        <table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                            <tr>
                            <td style="padding:0;width:50%;" align="left">
                                <p style="margin:0;font-size:14px;line-height:16px;font-family:Arial,sans-serif;color:#ffffff;">
                                PESO-Malvar
                                </p>
                            </td>
                            <td style="padding:0;width:50%;" align="right">
                                <table role="presentation" style="border-collapse:collapse;border:0;border-spacing:0;">
                                <tr>
                                    <td style="padding:0 0 0 10px;width:38px;">
                                    <a href="https://www.facebook.com/search/top?q=peso%20malvar" style="color:#ffffff;"><img src="https://assets.codepen.io/210284/fb_1.png" alt="Facebook" width="38" style="height:auto;display:block;border:0;" /></a>
                                    </td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </body>
            </html>
        """.format(name=name, status=status)

    return html

def send_email(email, name, status):
    message = Mail(
    from_email='pesomalvar@gmail.com',
    to_emails=email,
    subject='PESO Malvar',
    html_content=email_template(name, status))
    try:
        sg = SendGridAPIClient(
            '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')
        sg.send(message)
    except Exception as e:
        print(e.message)


def encrypt_email(email):
    message_bytes = email.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decrypt_email(encrypted_email):
    base64_bytes = encrypted_email.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message