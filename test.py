from auth import user_authorization
import requests

url = user_authorization()

response = requests.get(url)

print(response.args.get('code'))

