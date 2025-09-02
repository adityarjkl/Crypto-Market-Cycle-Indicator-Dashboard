from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

website = 'https://coinmarketcap.com/charts/crypto-market-cycle-indicators/'

driver.get(website)

driver.implicitly_wait(0.5)

h3_title = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/div[1]/div')
print(h3_title.text)

driver.quit()




