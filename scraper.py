'''
Created on Feb 5, 2017

@author: raghul

Python program to scrape index information from Bloomberg("https://www.bloomberg.com/markets/stocks").
'''
import urllib2
from bs4 import BeautifulSoup
import json

def find_region(section): # Returns region name (eg: Americas).
    header = section.find("div", attrs = {"class" : "chart-and-data__header-section"})
    region = header.find("a").contents[0].strip()
    return region

def find_keys(data_table): # Returns table headers.
    keys = []
    theads = data_table.findAll("th")
    for thead in theads[:-1]: # We don't need the last value ("2 day").
        keys.append(thead.contents[0].strip())
    return keys

def find_values(data_table): # Parsing table rows.
    symbols = [] # Index symbols.
    values = [] # List of lists representing data-tables.
    tbody = data_table.find("tbody")
    rows = tbody.findAll("tr")
    for row in rows:
        values.append([]) # Add a new list for each row.
        columns = row.findAll("td")
        
        divs = columns[0].findAll("div") # First column value contains both symbol and name.
        symbols.append(divs[0].contents[0].strip())
        values[-1].append(divs[1].contents[0].strip()) # Index name will be the first element in each "values[]" list.
        
        for column in columns[1 : -1]: # We have already read the first element of "columns". We don't need the last one ("2 day").
            values[-1].append(column.contents[0].strip())
    
    return symbols, values
   
def build_quotes(id): # Add values for region contained in "id" tag to the "quotes" dictionary.
    section = soup.find("div", attrs = {"data-view-uid" : id})
    region = find_region(section)
    quotes[region] = {} # Dictionary is mutable. Changes are global.

    data_tables = section.find("div", attrs = {"class" : "data-tables"})
    data_table = data_tables.find("table") # The table element that contains all values.
    
    keys = find_keys(data_table) # "keys" contains the table headers.
    symbols, values = find_values(data_table) # Read symbols and values from each line of the table.

    for i in range(len(symbols)): 
        quotes[region][symbols[i]] = {} # Index symbol will be the key.
        for j in range(len(keys)):
            quotes[region][symbols[i]][keys[j]] = values[i][j] # Assign values corresponding to headers. 
         
url = "https://www.bloomberg.com/markets/stocks"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, "html.parser")
quotes = {} # Dictionary that will contain all values.
ids = ["1|0_5_3", "1|0_5_6", "1|0_5_8"] # Indentifiers for containers.
for id in ids:
    build_quotes(id)
with open("sample-output.json", "w") as f:
    json.dump(quotes, f, indent = 4)