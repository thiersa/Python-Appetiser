#!/usr/bin/env python3

import bs4
import sqlite3
import requests

def main():
    db = sqlite3.connect('fuelprices.db')

    for fuel, price in scrape():
        print(fuel, price)
        store(db, fuel, price)
    
    db.close()

def scrape():
    fuels = ('Euro95', 'Diesel', 'LPG')
    response = requests.get("https://www.nu.nl/brandstof")
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    targetcells = soup.find_all('td', string='GLA*')

    for i, td in enumerate(targetcells):
        pricecell = td.parent.contents[3]
        yield fuels[i], pricecell.text.replace(',', '.')

        if i == 2: # only get Euro95, Diesel, and LPG
            break

def store(db, fuel, price):
    curs = db.cursor()
    curs.execute('INSERT INTO prices (fuel, price) VALUES (?, ?)', (fuel, price))
    db.commit()
    curs.close()

main()
