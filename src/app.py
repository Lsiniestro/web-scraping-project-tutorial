
import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import re
import pandas as pd


resource_url = "https://ycharts.com/companies/TSLA/revenues"


response = requests.get(resource_url,headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"})

if response:
    # Transformamos el HTML plano en un HTML real (estructurado y anidado, con forma de árbol)
    soup = BeautifulSoup(response.text, 'html')
    soup

tables = soup.find_all("table")
tables

for index, table in enumerate(tables):
    table_index = index
    break

# Create a DataFrame
tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("B", "").replace(".", "").strip()
        tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({
            "Date": Date,
            "Revenue": Revenue
        }, index = [0])], ignore_index = True)


tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]


import sqlite3

connection = sqlite3.connect("Tesla.db")
connection

cursor = connection.cursor()
cursor.execute("""CREATE TABLE revenue (Date, Revenue)""")

tesla_tuples = list(tesla_revenue.to_records(index = False))


cursor.executemany("INSERT INTO revenue VALUES (?,?)", tesla_tuples)
connection.commit()


#Grafico lineplot con todos los registros

fig, axis = plt.subplots(figsize = (10, 5))

tesla_revenue["Date"] = pd.to_datetime(tesla_revenue["Date"])
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].astype('int')

sns.lineplot(data = tesla_revenue, x = "Date", y = "Revenue")

plt.tight_layout()
plt.savefig('grafico1') 

#Barras por año

fig, axis = plt.subplots(figsize = (10, 5))
tesla_revenue["Date"] = pd.to_datetime(tesla_revenue["Date"])
por_año = tesla_revenue.groupby(tesla_revenue["Date"].dt.year).sum().reset_index()

sns.barplot(data = por_año[por_año["Date"] <= 2024], x = "Date", y = "Revenue")

plt.tight_layout()
plt.savefig('grafico2') 

#Pie Chart por año

por_año = tesla_revenue.groupby(tesla_revenue["Date"].dt.year).sum().reset_index()
labels = por_año['Date']
fig, ax = plt.subplots()
ax.pie(por_año['Revenue'], labels=labels)
plt.savefig('grafico3') 
