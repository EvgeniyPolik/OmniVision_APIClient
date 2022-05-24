import requests
catalog_boller = []


def get_catalog():
    global catalog_boller
    ids = 0
    while True:
        reg = requests.get('https://localhost:5001/GetCatolog/' + str(ids), verify=False)
        if reg.text != 'endoffile':
            answer = reg.json()
            catalog_boller.append(answer)
            ids += 1
            print(ids)
        else:
            break
