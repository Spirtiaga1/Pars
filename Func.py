from pymongo import MongoClient
from pprint import pprint
client=MongoClient('localhost',27017)
db=client['work']
vac=db.vacancies
s=input('Введите минимальную зарплату в рублях: ')

for v in vac.find({'lowsal':{'$gt':s}}):
    pprint(v)