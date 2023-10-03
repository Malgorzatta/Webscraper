# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import openpyxl
from openpyxl import workbook
import time

# Create an URL object
pages = np.arange(1,50) #50
headers = []
row_data = []

for page in pages:
    url = "https://playtoearn.net/blockchaingames?sort=socialscore_24h&direction=desc&page="+str(page)+""
    #print(url)
    # Create object page
    page = requests.get(url)
    #print(page)
    # parser-lxml = Change html to Python friendly format
    # Obtain page's information
    soup = BeautifulSoup(page.text, 'lxml')
    #print(soup)
    # Obtain information from tag <table>
    table1 = soup.find("table",{"class":"table table-bordered mainlist"})
    #print(table1)
    # Create a for loop to fill mydata
    for y in table1.find_all('tr')[2:]: #tr rows

        second_td = y.find_all('td')[3].find_all('a')
        second_tdA = [a.text.strip() for a in second_td]
        if 'Move-To-Earn' not in second_tdA:
            continue
        #print(second_tdA)
        #adv = y.find_all('td')[2].find_all('a')
        #if 'https://playtoearn.net/advertise' in adv:
        #    continue

        blockchains = []
        for third_td in y.find_all('td')[4].find_all('a'):
            blockchain = third_td['title']
            blockchains.append(blockchain)
            bl = '\n'.join(blockchains)
        #print(bl)

        devices = []
        for fourth_td in y.find_all('td')[5].find_all('a'):
            device = fourth_td['title']
            devices.append(device)
            dev = '\n'.join(devices)
        #print(dev)

        td_tags = y.find_all('td') #td in tr
        #print(td_tags)
        row = [z.text.strip() for z in td_tags]
        row [4] = bl
        row [5] = dev
        #print(row)
        row_data.append(row)
        #print(row)
# Obtain every title of columns with tag <th>
for x in table1.find_all('th'):
    title = x.text
    title=title.strip()
    headers.append(title)
#print(headers)

# Create a dataframe
mydata = pd.DataFrame(row_data, columns = headers)
#length = len(mydata)
mydata.index = np.arange(1, len(mydata)+1)
#mydata.loc[length] = row
# Drop “xyz” column
mydata.drop('', inplace=True, axis=1)
mydata.drop('Social 7d', inplace=True, axis=1)
mydata.drop('Social 24h', inplace=True, axis=1)

# Drop “xyz” row
#mydata.drop(0, inplace=True, axis=0)
print(mydata)

mydata.to_excel("M2E_games.xlsx")
#mydata.to_csv('P2E.csv')