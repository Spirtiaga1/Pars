from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from pprint import pprint
main_link2='https://www.superjob.ru/vacancy/search/?keywords='
main_link='https://hh.ru/search/vacancy?area=1&st=searchVacancy&text='
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
job=input('Введите наименование должности: ')
p=job.split()
sep='%20'
job=sep.join(p)
jobhh='+'.join(p)
pages=input('Введите количество страниц для парсинга: ')
job=job.lower()
Main_data=[]

for i in range( int(pages)):
    html=requests.get(main_link2+job+'&page='+str(i+1),headers=headers).text
    parsed_html=bs(html,'lxml')
    vac_block=parsed_html.find('div',{'style':'display:block'},)
    vac_list=vac_block.findChildren('div',{'class':'_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})
    for vac in vac_list:
        main={}
        if vac.find('span',{'class':'_1rS-s'}).nextSibling==None:
            name=vac.find('span',{'class':'_1rS-s'}).string
        else:
            name = vac.find('span', {'class': '_1rS-s'}).string + vac.find('span', {'class': '_1rS-s'}).nextSibling
        link='https://www.superjob.ru'+vac.find('a')['href']
        salar_block=vac.find('span',({'class':'_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})).getText().split()
        if salar_block[0]=="от":
            low_sal=int(salar_block[1]+salar_block[2])
            max_sal=''
            currency=salar_block[-1]
        elif salar_block[0]=='до':
            max_sal = int(salar_block[1]+salar_block[2])
            low_sal = ''
            currency = salar_block[-1]
        elif salar_block[0]=="По":
            max_sal=''
            low_sal=''
            currency=''
        elif salar_block[2]=='₽':
            max_sal = int(salar_block[0] + salar_block[1])
            low_sal = int(salar_block[0] + salar_block[1])
            currency = salar_block[-1]
        else:
            currency = salar_block[-1]
            low_sal = int(salar_block[0]+salar_block[1])
            max_sal = int(salar_block[3]+salar_block[4])
        main['vacancy'] = name
        main['lowsal'] = low_sal
        main['maxsal'] = max_sal
        main['currency'] = currency
        main['link'] = link
        main['source'] = 'https://superjob.ru/'
        Main_data.append(main)
for i in range(int(pages)):
    # 1 HH

    html = requests.get(main_link + jobhh + '&page' + str(i), headers=headers).text
    parsed_html = bs(html, 'lxml')
    vac_block = parsed_html.find('div', {'class': 'vacancy-serp'})
    vac_list = vac_block.findChildren('div', {
        'data-qa': ['vacancy-serp__vacancy vacancy-serp__vacancy_premium', 'vacancy-serp__vacancy']})
    for vac in vac_list:
        main = {}
        name = vac.find('a', {'class': 'bloko-link HH-LinkModifier'}).string
        salar_block = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salar_block == None:
            lowsal = ''
            maxsal = ''
            currency = ''
        else:
            salary = salar_block.string
            if salary.find('от') != -1:
                lowsal = salary.replace(u'\xa0', '').replace(' ', '')[2:-4]
                maxsal = ''
                currency = salary[-4:-1]
            elif salary.find('до') != -1:
                lowsal = ''
                maxsal = salary.replace(u'\xa0', '').replace(' ', '')[2:-4]
                currency = salary[-4:-1]
            else:
                lowsal = salary.replace(u'\xa0', '').replace(' ', '')[:salary.find('-') - 1]
                maxsal = salary.replace(u'\xa0', '').replace(' ', '')[salary.find('-'):-4]
                currency = salary[-4:-1]
        link = vac.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        main['vacancy'] = name
        main['lowsal'] = lowsal
        main['maxsal'] = maxsal
        main['currency'] = currency
        main['link'] = link
        main['source'] = 'https://hh.ru/'
        Main_data.append(main)
Main_Panda=pd.DataFrame(Main_data)
pprint(Main_Panda)