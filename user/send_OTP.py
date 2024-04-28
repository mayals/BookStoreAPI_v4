from django.conf import settings
# https://www.twilio.com/docs/libraries/python
from twilio.rest import Client

# user_phone_number: The phone number of the user you want to send the SMS code to.

# this function send OTPcode to user_phone_number to check phone number verification
def send_sms_code(user_phone_number, user_OTP_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create( 
                                    body =f"Your verification code is {user_OTP_code}",
                                    from_=settings.TWILIO_FROM_NUMBER,
                                    to   =f'{user_phone_number}'
    )
    print(message.sid)
