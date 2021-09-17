import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Data.data import dfs_20_21
from datetime import datetime

dates = dfs_20_21.Date.unique()

DRIVER_PATH = 'chromedriver.exe'
options = Options()
options.headless = True
options.binary_location = ("C:\Program Files\Google\Chrome\Application\chrome.exe")

cash_avg = []
d = []
for date in dates:
    try:
        date_adj = datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
        cash_xpath = '//*[@id="root"]/main/div[3]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/div/div[4]/div/div/div[2]'
        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        driver.get(f'https://rotogrinders.com/resultsdb/site/draftkings/date/{date_adj}/sport/nba/slate/')
        test = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, cash_xpath)))
        cash_line_avg = driver.find_element_by_xpath(cash_xpath).text
        driver.quit()

        d.append(date)
        cash_avg.append(cash_line_avg)
        print(f'Running {date_adj} date', cash_line_avg)
    except Exception as error:
        print(error, date)

print(cash_avg)

df = pd.DataFrame(cash_avg, columns=['Cash Lines'])
df['Date'] = d
df.to_csv('resultsDB.csv', index=False)
