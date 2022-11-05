import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.closed()

if __name__ == '__main__':
    create_connection("ecomm.db")

# # import requests module
# import requests
# import json
# import urllib.parse
# import sys

# # Making a get request
# # response = requests.get('https://api.github.com')

# meme = sys.argv[1]
# top = sys.argv[2]
# bottom = sys.argv[3]

# url = f"https://apimeme.com/meme?meme={urllib.parse.quote_plus(meme)}&top={urllib.parse.quote_plus(top)}&bottom={urllib.parse.quote_plus(bottom)}"


# response = requests.get(url)

# with open("/home/projects/final_project/meme2.png",'wb') as f:
#     f.write(response.content)

# print(response)
# # response = requests.get(url)
# # # print response
# # print(response)

# # header = response.headers 

# # json_data = response.headers
# # json_object = json.loads(json_data)
# # print headers of response
# # for i in header:
# #     print(f"{i}: {header[i]}")






# # from datetime import datetime

# # x = datetime.now()
# # format_data = "%Y-%m-%d"
# # # date = datetime.strptime(x, "%Y-%m-%d")
# # print("Hello from ubuntu server running on windows")
# # # print(f"today is {date.date} of month: {date.month} in the year: {date.year}")
# # print(x)
# # print(format_data)