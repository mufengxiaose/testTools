import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

url = "https://mp-platfrom.intra.xiaojukeji.com/#/tool/%E6%94%AF%E4%BB%98%E5%B7%A5%E5%85%B7"

username = "cliuxiao_v"
passport = "Supanpan521/"

driver = webdriver.Chrome()
driver.get(url=url)
try:
    # 等待加载
    wait = WebDriverWait(driver, 10)

    #输入
    username_el = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
    username_el.send_keys(username)

    passport_el = driver.find_element(By.XPATH, '//*[@id="password"]')
    passport_el.send_keys(passport)

    login_bt = driver.find_element(By.XPATH, '//*[@id="submit"]/span')
    login_bt.click()

    time.sleep(3)

    trigger_el = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/div/ul/li[1]/div'))
    )
    ActionChains(driver).move_to_element(trigger_el).perform()
    tuikuan_el = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/ul/li[5]'))
    ).click()

    time.sleep(1)
    env_el = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div/div[1]/div/div/span[2]/div/div/span/i')
    env_el.click()
    kf_env_el = driver.find_element(By.XPATH, '//*[@id="dropdown-menu-4358"]/li[8]')
    kf_env_el.click()

    time.sleep(10)
finally:
    driver.quit()