# import requests module
import requests
import json

# Making a get request
response = requests.get('https://api.github.com')
  
# print response
print(response)

header = response.headers 

# json_data = response.headers
# json_object = json.loads(json_data)
# print headers of response
for i in header:
    print(f"{i}: {header[i]}")






# from datetime import datetime

# x = datetime.now()
# format_data = "%Y-%m-%d"
# # date = datetime.strptime(x, "%Y-%m-%d")
# print("Hello from ubuntu server running on windows")
# # print(f"today is {date.date} of month: {date.month} in the year: {date.year}")
# print(x)
# print(format_data)