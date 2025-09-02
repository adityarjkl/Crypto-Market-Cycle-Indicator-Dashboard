from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()

website = 'https://coinmarketcap.com/charts/crypto-market-cycle-indicators/'

driver.get(website)

driver.implicitly_wait(0.5)

# Extracting the title of the webpage
webpage_title = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[1]/div')
print(webpage_title.text)

# Extracting table data
indicators = driver.find_elements(By.TAG_NAME, 'tr')

indi_index = [] 
indi_name = [] 
indi_current_value = [] 
indi_24hrChange = [] 
indi_reference_value = [] 

# Loop through each row and extract the data
# Skip the header row and empty rows
for indicator in indicators:
    tds = indicator.find_elements(By.TAG_NAME, 'td')
    if tds and len(tds) > 0:
        indi_index.append(tds[0].text)
        indi_name.append(tds[1].text)
        indi_current_value.append(tds[2].text)
        indi_24hrChange.append(tds[3].text)
        indi_reference_value.append(tds[4].text)

driver.quit()

# Creating a DataFrame and saving to CSV
df = pd.DataFrame({'Index': indi_index, 'Name': indi_name, 'Current Value': indi_current_value, '24hr Change': indi_24hrChange, 'Reference Value': indi_reference_value})

df.to_csv('Crypto_Market_Cycle_Indicators_export.csv', index=False)
print(df)





