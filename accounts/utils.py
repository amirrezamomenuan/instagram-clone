import json
from unittest import result
import requests
import random

apikey = ""
address = f"https://api.kavenegar.com/v1/{apikey}/sms/send.json"


def phone_number_validator(number):
    # confirmation_code = random.randint(10000,99999)
    # data = {"receptor": str(number), "message": f"your confirmation code is : {confirmation_code}"}

    # result = requests.post(url=address, data=data)
    # if result.status_code == 200:
    #     status = True
    # else:
    #     status = False

    # return confirmation_code, number, status
    return 123456, number, True
