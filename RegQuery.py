import requests
import UserDialog

catalog_bollers = []
health_bollers = {}

def get_catalog():
    global catalog_bollers
    try:
        ids = 0
        while True:
            reg = requests.get('https://localhost:5001/GetCatolog/' + str(ids), verify=False)
            if reg.text != 'endoffile':
                answer = reg.json()
                catalog_bollers.append(answer)
                ids += 1
            else:
                break
        catalog_bollers = sorted(catalog_bollers, key=lambda x: x["Id"])
    except requests.exceptions.ConnectionError:
        UserDialog.popup('Ошибка связи с сервером')

def update_status():
    global health_bollers
    for item in catalog_bollers:
        reg = requests.get('https://localhost:5001/GetStatus/' + str(item["Id"]), verify=False)
        if reg.text != 'Not_found':
            answer = reg.json()
            health_bollers[item["Id"]] = answer
