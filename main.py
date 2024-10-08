"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/68801025-a3e6-4cb8-8849-90d00be35e00' \
  -H 'accept: text/plain'
"""
import pprint

import requests

# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     "accept": '*/*',
#     'Content-Type': 'application/json'
# }
# json = {"login": "PavelTest2",
#         "email": "PavelTest2@mail.com",
#         "password": "123456789"}
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )

url = 'http://5.63.153.31:5051/v1/account/68801025-a3e6-4cb8-8849-90d00be35e00'
headers = {
    "accept": 'text/plain'
}
json = {"login": "PavelTest2",
        "email": "PavelTest2@mail.com",
        "password": "123456789"}

response = requests.put(
    url=url,
    headers=headers
)
print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])

