import requests

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('01.jpg', 'rb')},
    data={'size': 'auto', 'bg_color': '#438edb'},
    headers={'X-Api-Key': 'vABnufCxNtwo7WtaU8ZDqwn3'},
)
if response.status_code == requests.codes.ok:
    with open('001.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)
