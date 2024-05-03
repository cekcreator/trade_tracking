from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime


def find_recent_trade_write_to_csv():
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    driver.get('https://www.quiverquant.com/congresstrading/politician/Nancy%20Pelosi-P000197?')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'tradeTable')))

    element_to_click = driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[1]")
    element_to_click.click()
    main_content = driver.find_element(By.ID, 'main-content')
    lines = main_content.text.split('\n')
    driver.quit()

    indices = [lines.index('Amount'), lines.index('Traded'), lines.index('Disclosed'), lines.index('Description')]
    stock = lines.index('Stock')
    politician = lines.index('Politician')
    stock = lines[stock + 1: politician]
    stock = ' '.join(stock)
    trade_info = [lines[i + 1] for i in indices]

    today = datetime.now()
    today = today.strftime('%Y-%m-%d')
    trade_df = {'Stock': [stock], 'Amount': [trade_info[0]],
                'Traded': [trade_info[1]], 'Disclosed': [trade_info[2]],
                'Description': [trade_info[3]], "Date_Retrieved": today}

    trade_df = pd.DataFrame(trade_df, columns=['Stock','Amount','Traded','Disclosed','Description','Date_Retrieved'])
    writer = pd.ExcelWriter('./csvs/trades.xlsx',)
    trade_df.to_excel(excel_writer=writer)
    writer.close()


if __name__ == '__main__':
    find_recent_trade_write_to_csv()
    print('Added to csv file')
