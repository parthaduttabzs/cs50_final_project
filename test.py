import json


cart_list = '[{"product_id":3,"qty":2,"price":100}]'
cart_list = json.loads(cart_list)

# cart = json.loads( cart )

# new = {}
# new['product_id'] = 4
# new['qty'] = 1
# new['price'] = 20 

# cart.append(new)

print((cart_list))

# text = '204629_16-aashirvaad-select-atta.webp'
# index_start = 0
# index_end = 0
# for i in range(0,len(text)-1,1):
#     if text[i].isalpha():
#         index_start = text.find(text[i])
#         continue
#     if text[i] == ".":
#         index_end = text.find(text[i])
#         break
# text1 = text[index_start:index_end]
# text2 = text1.replace("-"," ")
# text3 = text2.title()
# print(text3)




# # Create a DB
# import sqlite3
# from sqlite3 import Error

# def create_connection(db_file):
#     conn = None

#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.closed()

# if __name__ == '__main__':
#     create_connection("ecomm.db")

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