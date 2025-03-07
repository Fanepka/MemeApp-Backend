import requests


r= requests.post('http://192.168.88.97:8000/auth/login', data={"username": "me@fanepka.ru", "password": "1234"})
print(r.json())