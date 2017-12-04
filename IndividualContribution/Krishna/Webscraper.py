import bs4 as bs
import urllib.request
import time
import pandas as pd
import csv

outfile = open('/home/kkanagalananthapadm1/weather_dataB.csv','w')
except_file = open('/home/kkanagalananthapadm1/weather_data_exceptionsB.txt','a')
writer = csv.writer(outfile,lineterminator = '\n')
airport_data = ['KAVP','KAZO','KBDL','KBET','KBFL','KBGM','KBGR','KBHM','KBIL','KBIS',
'KBJI','KBLI','KBMI','KBNA','KBOI','KBOS','KBPT','KBQK','KBQN','KBRD',
'KBRO','KBRW','KBTM','KBTR','KBTV','KBUF','KBUR','KBWI','KBZN']

def get_daily_data(url,month):
    source = urllib.request.urlopen(url)
    daily_data = []
    soup = bs.BeautifulSoup(source,'html.parser')
    table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="obsTable")
    if table is None:
        daily_data.append('WrongLink')
        print (daily_data)
        return daily_data
    rows = table.findAll('td')
    counts = len(rows)    
    recordings = counts/13
    if counts%13 != 0:
        except_record = url + '\n'
        except_file.write(str(except_record))
    daily_list = []
    for i in range (1,int(recordings)+1):
        for j in range(1,14):
            disposition = (i-1)*13 + (j-1)
            if rows[disposition].find('span'):
                for wrapper in rows[disposition].findAll('span',{'class' : 'wx-value' }):
                    daily_list.append(wrapper.text)
            else:
                daily_list.append(rows[disposition].contents[0])
        daily_data.append(daily_list)
        daily_list = []
    return daily_data

base_url = "https://www.wunderground.com/history/airport/"
Year = "2015"
daily_weather = []
for airport_code in airport_data:
    for month in range (1,13):
        for day in range (1,32):
            if (month in [4,6,9,11] and day==31):
                continue
            elif (month==2 and day > 28):
                continue
            else:
                url = base_url+ airport_code + '/' + Year + '/' + str(month) + '/'+ str(day) + '/' + "/DailyHistory.html"
                weather = get_daily_data(url,month)
                if weather[0] == 'WrongLink':
                    print ('Here')
                    break
                key = airport_code + '-' + Year + '-' + str(month) + '-' +str(day)
                for hourly in weather:
                    daily_weather.extend((airport_code,Year,month,day))
                    daily_weather.extend(hourly)
                    writer.writerow(daily_weather)
                    daily_weather = []
        if weather[0] == 'WrongLink':
            break
    print (airport_code,'done')
    time.sleep(2)

outfile.close()
except_file.close()
time.sleep(1)

