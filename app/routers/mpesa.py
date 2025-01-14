import base64
import requests
from fastapi import HTTPException
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth

consumer_key='7tWrv1GzADCWG7gdFeXlGGfWKJdu9iplFEXA3AL2L0c6KDoT'
consumer_secret ='VIzhHEdmCN8519EsnkKH4DpZ0nOoMBcFNDCXlpQktZnKn4YktpL8fB0A1YenRanE'
pass_key ='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
saf_url = "https://sandbox.safaricom.co.ke/"
short_code = '174379'
callback_url = 'https://oneshop.co.ke/stk_callback'



def stk_push_sender(mobile, amount):
    try:
        encoded_credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {encoded_credentials}","Content-Type": "application/json"}
        url = saf_url+"/oauth/v1/generate?grant_type=client_credentials"
        #Send the request and parse the response
        response = requests.get(url, headers=headers).json()

        # Check for errors and return the access token
        if "access_token" in response:
            token = response["access_token"]
        else:
            raise Exception("Failed to get access token: " + response["error_description"])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e)) 

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    stk_password = base64.b64encode((short_code + pass_key + timestamp).encode('utf-8')).decode()

    url = saf_url + "mpesa/stkpush/v1/processrequest"
    headers = {'Authorization': 'Bearer ' + token,'Content-Type': 'application/json'}

    request = {"BusinessShortCode": short_code,"Password": stk_password , "Timestamp": timestamp,
               "TransactionType": "CustomerPayBillOnline","Amount": str(amount), "PartyA": str(mobile),
               "PartyB": short_code, "PhoneNumber": str(mobile), "CallBackURL": callback_url,
               "AccountReference" : "myduka1", "TransactionDesc" : "Testing STK Push"}
    response = requests.post(url, json = request, headers = headers)
    return response.text

stk_push_sender("254714056473", 1)











