from twilio.rest import Client
import smtplib

TWILIO_SID = "AC6917d102cfc2375f7575a3eac98d7e7b"
TWILIO_AUTH_TOKEN = "f9975ce48ed2f877cfcf8bf1cb861607"
TWILIO_VIRTUAL_NUMBER = "+12184526685"
TWILIO_VERIFIED_NUMBER = "+917569562436"


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        self.my_email = "adarsheluri123@gmail.com"
        self.password = "zertwpjaqmfrgvsk"

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        '''print(message.sid)'''

    def send_emails(self, user_mails, message):
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            connection.sendmail(from_addr=self.my_email, to_addrs=user_mails,
                                msg=f"Subject: Cheap FLight Ticketsmessage\n\n{message}")


