# use web scrapping at your own risk.
# make sure you have chrome web driver installed on your workstation.
# csv data will be saved as strings, you need to clean up the datatypes afterwards.

from datetime import date
from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv


# list of coins to check; make sure name is correct.
currency_name_list = [
    "ethereum",
    "bitcoin",
    "cardano",
    "nem",
    "binance-coin",
    "polkadot-new",
    "stellar",
    "xrp",
    ]

start_date = '2017-03-01'
end_date = str(date.today())

page_counter = 1 # track number of currencies to download

for currency_name in currency_name_list:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless") 
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome("C:\\Users\\localtt\\webdrivers\\chromedriver.exe", chrome_options=options)

    driver.get(f"https://coincheckup.com/coins/{currency_name}/charts")
    sleep(10) # let's wait until the page loads

    # input date range here to generate table
    date_picker = driver.find_element(By.XPATH, '//input[@ng-model="dateHistory"]')
    date_picker.click()
    sleep(1)
    date_picker.send_keys(Keys.CONTROL, 'a')
    sleep(0.5)
    date_picker.send_keys(Keys.DELETE)
    sleep(0.5)
    date_picker.send_keys(start_date)
    sleep(0.5)
    date_picker.send_keys(' - ')
    sleep(0.5)
    date_picker.send_keys(end_date)
    sleep(2)
    date_picker.send_keys(Keys.ENTER)

    sleep(10) # let's wait for the data table the fully generate

    page_source = driver.page_source # prepare page for beautiful soup to scrape

    soup = BeautifulSoup(page_source, 'html.parser')
    price_table = soup.find("table",{"class":"table dataTable"})


    # saves table data to csv file
    with open(f"./{currency_name}_price.csv", "w") as ofile:
        print(f'save CSV data for {currency_name} from {start_date} to {end_date}... coin:{page_counter}/{len(currency_name_list)}')
        writer = csv.writer(ofile)
        rows = price_table.find_all("tr")
        for row in rows:
            csv_row = []
            for cell in row.findAll(["td", "th"]):
                csv_row.append(cell.get_text())
            writer.writerow(csv_row)

    driver.quit()

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