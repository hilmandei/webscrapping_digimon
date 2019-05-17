from bs4 import BeautifulSoup
import requests
import mysql.connector
import csv

mydb = mysql.connector.connect(
        host='localhost',
        user='hilmandei',
        passwd='rongjelek19',
        database='purwadhika')


# from website
url = 'https://wikimon.net/Visual_List_of_Digimon'
x = requests.get(url)
y = BeautifulSoup(x.content, 'html.parser')
img = y.find_all('td', style="border: 1px solid #AAAAAA; background-color: #FFFFFF;height: 124px;")

listcsv=[['id', 'nama', 'link']]
id = 1
for x in img:
    img2 = x.find_all('img')
    for i in img2:
        name = str(i.get('alt'))
        link = str('https://wikimon.net' + i.get('src'))

        listcsv.append([id, name, link])
        id = id + 1

        x = mydb.cursor()
        x.execute('insert into digimon (name, link) values (%s, %s)', (name, link))
        mydb.commit()


print(listcsv)
with open('listdigimon.csv', 'w', encoding='utf-8', newline='') as csvFile:
    datacsv = csv.writer(csvFile, delimiter=';')
    datacsv.writerows(listcsv)


x = mydb.cursor()
x.execute('select * from digimon')
data = x.fetchall()
print(data)
print(type(data))