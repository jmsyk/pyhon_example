from bs4 import BeautifulSoup
from datetime import date
import re, requests, openpyxl

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Weather Data'
sheet.append(['Time','Temperature','Chance of Rain'])

#Create today's URL
base = 'https://www.metoffice.gov.uk/weather/forecast/gcqds9uch#?nearestTo=B2%20(United%20Kingdom)&date=' 
today = str(date.today())
url_today = base + today

url = requests.get(url_today)
soup = BeautifulSoup(url.text,'html.parser')


times = soup.find('tr', class_='step-time')
ppt_chances = soup.find('tr', class_='step-pop')
temperatures = soup.find('tr', class_='step-temp')
#conditions = soup.find('tr', class_='step-symbol')

day = 'd0'

times_list = []
temps_list = []
ppts_list = []

for time in times.find_all('th', id = re.compile(day)):
    times_list.append(time.get_text(strip=True))

for temp in temperatures.find_all('td', headers = re.compile(day)):
    temps_list.append(temp.get_text(strip=True))

for chance in ppt_chances.find_all('td', headers = re.compile(day)):
    ppts_list.append(chance.get_text(strip=True))

for i in range(len(times_list)):
    sheet.append([times_list[i],temps_list[i],ppts_list[i]])

'''
for n in soup.find_all('tr', class_='step-time'):
   for x in n.find_all('th',id=True):
       l2.append(x.get_text(strip=True))

'''

print(times_list, temps_list, ppts_list)
excel.save('Weather data.xlsx')