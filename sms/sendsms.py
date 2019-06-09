import requests
import json

def sending_sms(message, phone_numbers):
    url = "https://www.fast2sms.com/dev/bulk"
    headers = {
                'authorization': "ucmdDpw3FEaBMo1XAlqGL8nrbJ6jeK07HzUgtP5SsIvRWQ42kZwkDjS5eXPJb9R1CVmMW0KzoYapQZv7",
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache",
            }
    # payload
    payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="+phone_numbers
    # send
    response = requests.request("POST", url, data=payload, headers=headers)
    dict_response = json.loads(response.text)
    message = dict_response['message']
    returns = dict_response['return']

    return message, returns
