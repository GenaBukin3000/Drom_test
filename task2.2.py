import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()


def login():
    driver.get('https://auto.drom.ru/')
    driver.find_element(By.XPATH, '//a[@data-ga-stats-name="auth_block_login"]').click()
    driver.find_element(By.XPATH, '//input[@name="sign"]').send_keys('login')
    driver.find_element(By.XPATH, '//input[@name="password"]').send_keys('password')
    driver.find_element(By.XPATH, '//button[@id="signbutton"]').click()
    time.sleep(5)
    add_to_favorites()


def add_to_favorites():
    # В задании не сказано какое объявление добавлять в избранное поэтому добавлю первое видимое на странице
    car = driver.find_element(By.XPATH, '//a[@data-ftid="component_premium-carousel_item"][2]')
    href = car.get_attribute('href')
    car.click()
    driver.find_element(By.XPATH, '//div[@data-ga-stats-track-click="favorite"]').click()
    time.sleep(2)
    # Если окно о добавлении в избранное всплыло переходим в избранное через него
    try:
        driver.find_element(By.XPATH, '//div[@data-ftid="component_notification_type_success"]')
        driver.find_element(By.XPATH, '//a[@title="Перейти в раздел «Мое избранное»"]').click()
    # Иначе идем в обход через профиль
    except NoSuchElementException:
        user_info_list = driver.find_element(By.XPATH, '//div[@data-ftid="component_header_user-info-expand-controller"]')
        action = ActionChains(driver)
        action.move_to_element(user_info_list)
        action.perform()
        driver.find_element(By.XPATH, '//a[@data-ga-stats-name="topmenu_accountMy"]').click()
        time.sleep(5)
    # Проверка того, что объявление действительно добавлено в избранное
    try:
        driver.find_element(By.XPATH, f'//a[@href="{href}"]')
        print('Объявление добавлено в избранное')
        # Если объявление добавлено удаляем его, чтобы тест можно было запускать много раз
        driver.find_element(By.XPATH, '//a[@class="removeBookmark"]').click()
        time.sleep(2)
        return True
    except NoSuchElementException:
        print('Объявление не добавлено в избранное')
        return False


login()
