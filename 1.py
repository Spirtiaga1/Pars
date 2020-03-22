import requests
import json
from pprint import pprint
#Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

main_link='https://api.github.com/users'
user_name=input('Ввелите имя пользователя GitHub: ')
response=requests.get(f'{main_link}/{user_name}/repos')
if response.ok:
    l=1
    user_data={'User_Name': user_name}
    data_list=json.loads(response.text)
    for data in data_list:
        user_data.update({f'Repos{l}':data['full_name']})
        l+=1
    with open(f'{user_name} Repositories.json','w') as f:
        f.write(json.dumps(user_data))
    pprint(user_data)
else:
    print('Такого пользователя не существует')