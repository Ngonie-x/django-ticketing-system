import imaplib
import email

# credentials
username = "ipcconsultants1@gmail.com"

# generated app password
app_password = "9MG8pxqFZ+?vPnhq"

# https://www.systoolsgroup.com/imap/
gmail_host = 'imap.gmail.com'

# set connection
mail = imaplib.IMAP4_SSL(gmail_host)

# login
mail.login(username, app_password)

# select inbox
mail.select("INBOX")

# select specific mails
_, selected_mails = mail.search(None, 'ALL')

for num in selected_mails[0].split()[:10]:
    _, data = mail.fetch(num, '(RFC822)')
    _, bytes_data = data[0]

    # convert the byte data to message
    email_message = email.message_from_bytes(bytes_data)
    print("\n===========================================")

    # access data
    print("Subject: ", email_message["subject"])
    print("To:", email_message["to"])
    print("From: ", email_message["from"])
    print("Date: ", email_message["date"])
    for part in email_message.walk():
        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
            message = part.get_payload(decode=True)
            print("Message: \n", message)
            print("==========================================\n")
            break


class GetEmails:
    def __init__(self):
        gmail_host = 'imap.gmail.com'
        self.mail = imaplib.IMAP4_SSL(gmail_host)

    def login(self, username, password):
        self.mail.login(username, app_password)

    def get_emails(self):
        self.mail.select("INBOX")
        # select specific mails
        _, selected_mails = self.mail.search(None, 'ALL')

        for num in selected_mails[0].split()[:10]:
            _, data = mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]

            # convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)
            print("\n===========================================")

            # access data
            print("Subject: ", email_message["subject"])
            print("To:", email_message["to"])
            print("From: ", email_message["from"])
            print("Date: ", email_message["date"])
            for part in email_message.walk():
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    message = part.get_payload(decode=True)
                    print("Message: \n", message)
                    print("==========================================\n")
                    break
