import config
import os
import smtplib
import ssl

def get_directory_contents(dirPath):
    # check if directory exists
    directoryExists = os.path.exists(dirPath)
    if not directoryExists:
        print("Error: The following directory does not exist. Dir = {}".format(dirPath))
        return None

    contents = os.listdir(dirPath)
    return contents


def send_email(cfg, emailToSend):
    from email.mime.text import MIMEText
    from datetime import datetime

    # configure email object
    msg = MIMEText(emailToSend)
    now = datetime.now()
    msg["Subject"] = "{} - [{}]".format(cfg.subjectStem, now.strftime("%a %d/%m/%Y"))
    msg["From"] = cfg.sender
    msg["To"] = cfg.receiver

    status = False  # return status, assume fail unless success
    
    # create SSLContext object with default settings
    context = ssl.create_default_context()

    # send the email
    with smtplib.SMTP_SSL(cfg.host, cfg.port, context=context) as server:
        if not cfg.debugMode:  # do not have to login if using the local email server
            # server.ehlo() # some people say you need this
            # server.starttls()
            # server.ehlo()
            try:
                server.login(cfg.username, config.get_password(cfg.username))
            except smtplib.SMTPHeloError:
                print("The server didn’t reply properly to the HELO greeting.")
                return
            except smtplib.SMTPAuthenticationError:
                print("The server didn’t accept the username/password combination.")
                return
            except smtplib.SMTPNotSupportedError:
                print("    The AUTH command is not supported by the server.")
                return
            except smtplib.SMTPException:
                print("No suitable authentication method was found.")
                return

        try:
            print("Attempting to send the email.")
            server.sendmail(cfg.sender, cfg.receiver, msg.as_string())
        except smtplib.SMTPRecipientsRefused:
            print(
                "All recipients were refused. Nobody got the mail. The recipients"
                " attribute of the exception object is a dictionary with information"
                " about the refused recipients (like the one returned when at least one"
                " recipient was accepted)."
            )
            return
        except smtplib.SMTPHeloError:
            print("The server didn’t reply properly to the HELO greeting.")
            return
        except smtplib.SMTPSenderRefused:
            print("The server didn’t accept the from_addr.")
            return
        except smtplib.SMTPDataError:
            print(
                "The server replied with an unexpected error code (other than a refusal"
                " of a recipient)."
            )
            return
        except smtplib.SMTPNotSupportedError:
            print(
                "SMTPUTF8 was given in the mail_options but is not supported by the"
                " server."
            )
            return
        except:
            print("Unknown exception occurred. Send help.")
            return
        else:
            # handle gracefully
            print("The email should have been sent.")
            status = True
    return status 
