import requests

user_inp = input("Enter user key: ")

def validate(key):
    url = "http://127.0.0.1:8000/validate/"
    client = requests.session()
    client.get(url)
    csrftoken = client.cookies['csrftoken']
    login_data = dict(key=key, csrfmiddlewaretoken=csrftoken)
    r = client.post(url, data=login_data, headers=dict(Referer=url))
    if r.status_code == 200:
        return True
    else:
        return False

def mai(inp):
    check = validate(inp)
    if check == True:
        print("key is working")
    else:
        print("key is not working")

mai(user_inp)