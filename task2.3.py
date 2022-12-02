import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from prettytable import PrettyTable

driver = webdriver.Chrome()
driver.get('https://auto.drom.ru/')
driver.find_element(By.XPATH, '//a[@data-ga-stats-name="geoOverCity"]').click()
time.sleep(2)
driver.find_element(By.XPATH, '//div[@class="css-1r2f04i e93r9u20"][42]').click()
driver.find_element(By.XPATH, '//div[@class="css-1s8kstr edw82zo1"]').click()
driver.find_element(By.XPATH, '//input[@placeholder="Марка"]').click()
action = ActionChains(driver)
brand_list = list()
# Скроллинг списка
for i in range(6):
    action.send_keys(Keys.ARROW_DOWN)
    action.perform()

for i in range(1, 156):
    action.send_keys(Keys.ARROW_DOWN)
    action.perform()
    try:
        brand = driver.find_element(By.XPATH, '//div[@class="css-109956f e1x0dvi10"]')
        brand_cleaned = brand.text.translate({ord(')'): None}).split(' (')
        brand_list.append([brand_cleaned[0], int(brand_cleaned[1])])
    except NoSuchElementException:
        continue

sorted_brand_list = (sorted(brand_list, key=lambda x: x[1], reverse=True))
print('| Фирма | Количество объявлений |')
for i in range(20):
    print(f'| {sorted_brand_list[i][0]} | {sorted_brand_list[i][1]} |')

#x = PrettyTable()           #Если захочется, то можно сделать красиво

#x.field_names = ["Фирма", "Количество объявлений"]
#for i in range(20):
    #x.add_row([sorted_brand_list[i][0], sorted_brand_list[i][1]])

#print(x)
