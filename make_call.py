from twilio.rest import Client
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

try:
    # Twilio credentials
    account_sid = 'ACd51d37ccb4d1a8ea53ccc5352c4aaacf'
    auth_token = '90111e379990122e515726d1c69c4c6d'

    logging.info("Creating Twilio client...")
    client = Client(account_sid, auth_token)

    # Numbers
    twilio_number = '+12602352948'     # Your Twilio number (US)
    your_number = '+918401781811'      # Your Indian number

    logging.info("Placing call...")
    call = client.calls.create(
        twiml='<Response><Say>Hello Sapan! This is a test call from your AI assistant using Twilio. Have a great day!</Say></Response>',
        to=your_number,
        from_=twilio_number
    )

    print(f"✅ Call initiated. Call SID: {call.sid}")

except Exception as e:
    print(f"❌ Error occurred: {e}")
