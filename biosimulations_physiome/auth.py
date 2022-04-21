import http.client
from lib2to3.pgen2 import token
import os
import dotenv
import json


def main():
    print(get_token())


def get_token():
    dotenv.load_dotenv()
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')

    conn = http.client.HTTPSConnection("auth.biosimulations.org")

    payload = f'{{"client_id":"{client_id}","client_secret":"{client_secret}","audience":"api.biosimulations.org","grant_type":"client_credentials"}}'

    headers = {'content-type': "application/json"}

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    data = data.decode("utf-8")
    data = json.loads(data)
    token = data['access_token']
    token = "Bearer " + token
    return token


if __name__ == "__main__":
    main()
