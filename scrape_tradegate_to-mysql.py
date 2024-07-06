import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
from sqlalchemy import create_engine


def run():
	headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
	i=0
# list of tradegate urls
	urls =[
		"https://www.tradegate.de/orderbuch.php?isin=XXXXX",
		"https://www.tradegate.de/orderbuch.php?isin=XXXXX"
		]
	for url in urls:
		page = requests.get(url,headers=headers) 

		datatomysql =[]
		soup = BeautifulSoup(page.text, 'html.parser')
		timestamp = datetime.now()
		if timestamp.now().hour > 22 or timestamp.now().hour < 8 or timestamp.weekday() >=5: # should only collect data if market is open
			showweekday = timestamp.weekday()
			showhour = timestamp.now().hour
			#print("Weekend or not between 8am and 22pm ", showweekday, showhour)
			break
		else:
			stockname = soup.find('div', {'class': 'block'}).find_all('span')[0].text.strip()
			table = soup.find_all('table', attrs={'class':'full fixed right lines marketdata'})
			lastprice = soup.find(id="last").text.strip()

			dataframe =[stockname,timestamp,lastprice]
			datatomysql = pd.DataFrame(dataframe).T
			datatomysql.columns = ['stockname', 'timestamp', 'lastprice']
			print(datatomysql)
			mysqlengine = create_engine("mysql+mysqlconnector://user:password@host/database") #your mysql connection "user:password@host/database"
			datatomysql.to_sql('stockdata', con=mysqlengine, if_exists='append', index=False) #your table to add data
			time.sleep(5)

while True:
	run()
	time.sleep(60)
