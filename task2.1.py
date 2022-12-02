import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()


def check_sold_cars():                                                          # Проверка наличия проданных авто
    current_page = int(driver.find_element(By.XPATH, '//span[@class="css-xz6vp0 e10f3cqr0"]').text)
    while True:
        try:
            driver.find_element(By.XPATH, "//div[@class='css-r91w5p e3f4v4l2']")
            print('Проданные есть')
            driver.find_element(By.XPATH, '//a[@class="css-1jjais5 ena3a8q0"]').click()
            return False
        except NoSuchElementException:
            if current_page + 1 < 3:
                driver.find_element(By.XPATH, f'//div[contains(@class ,"e15hqrm30")][{current_page + 1}]').click()
                time.sleep(2)
                current_page += 1
            else:                                                                 # Цикл конечно не лучший но благодаря ему можно
                                                                                  # изменить количество страниц для проверки при помощи изменения условия if
                print('На первых двух страницах поиска нет проданных авто')
                time.sleep(2)
                driver.find_element(By.XPATH, '//a[@class="css-1jjais5 ena3a8q0"]').click()   # Возврат на первую страницу чтобы проверки
                return True                                                                   # можно было запускать как независимо так и вместе


def check_year():
    current_page = int(driver.find_element(By.XPATH, '//span[@class="css-xz6vp0 e10f3cqr0"]').text)
    while True:
        cars_list = driver.find_elements(By.XPATH, '//div[@class="css-17lk78h e3f4v4l2"]//span')
        for element in cars_list:
            if int(element.text[16:20]) >= 2007:
                continue
            else:
                print('На одной из страниц есть объявления с годом выпуска меньше 2007')
                driver.find_element(By.XPATH, '//a[@class="css-1jjais5 ena3a8q0"]').click()
                return False
        if current_page + 1 < 3:
            driver.find_element(By.XPATH, f'//div[contains(@class ,"e15hqrm30")][{current_page + 1}]').click()
            time.sleep(2)
            current_page += 1
        else:
            print('Год всех авто на двух страницах не меньше 2007')
            driver.find_element(By.XPATH, '//a[@class="css-1jjais5 ena3a8q0"]').click()
            return True


def check_mileage():
    current_page = int(driver.find_element(By.XPATH, '//span[@class="css-xz6vp0 e10f3cqr0"]').text)
    while True:
        ads_list = driver.find_elements(By.XPATH, '//a[@class ="css-xb5nz8 ewrty961"]')
        mileage_elements_list = driver.find_elements(By.XPATH, '//span[contains(text(), "тыс. км")]')
        if len(ads_list) == len(mileage_elements_list):                                         #Сравнение количества объявлений на странице
            if current_page + 1 < 3:                                                            #c количеством элементов содержащих пробег на странице
                driver.find_element(By.XPATH, f'//div[contains(@class ,"e15hqrm30")][{current_page + 1}]').click()
                time.sleep(2)
                current_page += 1
            else:
                print('У всех авто на двух страницах есть пробег')
                driver.find_element(By.XPATH, '//a[@class="css-1jjais5 ena3a8q0"]').click()
                return True
        else:
            print('Не у всех авто на двух страницах есть пробег')
            driver.find_element(By.XPATH, '//a[@class="css-1jjais5 ena3a8q0"]').click()
            return False


def search_filter():
    driver.get('https://auto.drom.ru/')
    driver.find_element(By.XPATH, '//input[@placeholder="Марка"]').click()  # Выбор марки авто
    driver.find_element(By.XPATH, '//div[@class="css-1r0zrug e1uu17r80"][3]').click()

    car_model_list = driver.find_element(By.XPATH, '//input[@placeholder="Модель"]')  # Выбор модели авто
    time.sleep(2)
    car_model_list.click()
    time.sleep(2)
    car_model_list.send_keys('Harrier')
    time.sleep(2)
    driver.find_element(By.XPATH, '//div[@class="css-109956f e1x0dvi10"]').click()

    driver.find_element(By.XPATH, '//button[text()="Топливо"]').click()  # Выбор типа топлива
    driver.find_element(By.XPATH, '//div[@class="css-u25ii9 e154wmfa0"]//div[6]').click()

    driver.find_element(By.XPATH, '//label[@for="sales__filter_unsold"]').click()  # Выбор непроданных авто

    driver.find_element(By.XPATH, '//button[text()="Год от"]').click()  # Выбор года выпуска
    driver.find_element(By.XPATH, '//div[@class="css-u25ii9 e154wmfa0"]//div[18]').click()
    time.sleep(2)

    driver.find_element(By.XPATH, '//button[@class="ezmft1z0 css-1q5ta30 e104a11t0"]').click()  # Выбор пробега
    time.sleep(2)
    mileage = driver.find_element(By.XPATH, '//input[@placeholder="от, км"]')
    time.sleep(2)
    mileage.send_keys('1')
    time.sleep(2)

    driver.find_element(By.XPATH, '//button[@class="css-2842jw e3cb8x01"]').click()  # Нажатие кнопки показать
    time.sleep(2)
    check_sold_cars()
    check_year()
    check_mileage()


search_filter()
