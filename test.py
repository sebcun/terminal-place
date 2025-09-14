import requests

url = "http://localhost:5000/api/place"

data = {"x": 10, "y": 10, "color": "#FF0000"}


response = requests.post(url, json=data)

if response.status_code == 201:
    print("SUCCESS", response.json())
else:
    print(response.status_code, response.json())
