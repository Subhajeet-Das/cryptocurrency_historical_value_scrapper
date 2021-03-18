# this version uses pyautogui to generate the table with desired date range.
# use web scrapping at your own risk.
# make sure you have chrome web driver installed on your workstation.
# csv data will be saved as strings, you need to clean up the datatypes afterwards.

from datetime import date
from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import pyautogui as pag


# list of coins to check; make sure name is correct.
currency_name_list = [
    "ethereum",
    "bitcoin",
    "cardano",
    "nem",
    # "binance-coin",
    # "polkadot-new",
    # "stellar",
    # "xrp",
    ]

end_date = str(date.today())

page_counter = 1 # track number of currencies to download

for currency_name in currency_name_list:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome("C:\\Users\\localtt\\webdrivers\\chromedriver.exe", chrome_options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)
    driver.get(f"https://coincheckup.com/coins/{currency_name}/charts")


    maximize_btn = (1845, 21)
    browser_scrollbar = (1736, 898)
    loc_datepicker = (1706, 236)
    loc_forever = (1706, 434)
    loc_applybtn = (1706, 515)

    sleep(6)
    pag.click(maximize_btn)
    sleep(1)
    pag.moveTo(500,500)
    sleep(1)

    pag.scroll(-1800) # scroll down 3 clicks

    pag.click(browser_scrollbar)
    sleep(1)
    pag.click(loc_datepicker)
    sleep(1)
    pag.click(loc_forever)
    sleep(1)
    pag.click(loc_datepicker)
    sleep(1)
    pag.click(loc_applybtn)
    sleep(3)


    page_source = driver.page_source
    sleep(5)
    soup = BeautifulSoup(page_source, 'html.parser')
    price_table = soup.find("table",{"class":"table dataTable"})


    # saves table data to csv file
    with open(f"./{currency_name}_price.csv", "w") as ofile:
        print(f'save CSV data for {currency_name} from FOREVER to {end_date}... coin:{page_counter}/{len(currency_name_list)}')
        writer = csv.writer(ofile)
        rows = price_table.find_all("tr")
        for row in rows:
            csv_row = []
            for cell in row.findAll(["td", "th"]):
                csv_row.append(cell.get_text())
            writer.writerow(csv_row)

    driver.close()

    # pause after each page request to prevent bann, except on last page
    if page_counter < len(currency_name_list):
        n = random.randint(7, 15)
        for i in range(n):
            print(f'pausing {n} seconds before accessing next page')
            sleep(1)
            n -= 1
    else:
        print('finished attempting to download CSV data for all coins')

    page_counter += 1 # increment page_counter by 1