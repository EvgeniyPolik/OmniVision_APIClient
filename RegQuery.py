import requests
import json

def get_catalog():
    request = requests.get('https://localhost:5001/GetCatolog/0', verify=False)
    catallog_boller = json.load(request.text)
    print(catallog_boller["Ip"])