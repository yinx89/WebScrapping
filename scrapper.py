from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def cambia_IP():
    with Controller.from_port(port = 9051) as controlador:
        controlador.authenticate()
        controlador.signal(Signal.NEWNYM)

# network.proxy.type -> Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
def my_Proxy(PROXY_HOST,PROXY_PORT):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks",PROXY_HOST)
    profile.set_preference("network.proxy.socks_port",int(PROXY_PORT))
    profile.update_preferences()
    options = Options()
    options.headless = True
    return webdriver.Firefox(options=options, firefox_profile=profile,
                             executable_path = '/usr/local/bin/geckodriver')

t0 = time.time()
# LOGIN - Web scrapping usgin normal IP
driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
driver.get("https://www.linkedin.com")
response_delay = time.time() - t0
time.sleep(1 + response_delay)
username = driver.find_element_by_id("session_key")
time.sleep(1 + response_delay)
username.send_keys('wallacedaniel.89@outlook.com')
password = driver.find_element_by_name('session_password')
time.sleep(3 + response_delay)
password.send_keys('jT7.W56TbVr28')
log_in_button= driver.find_element_by_class_name('sign-in-form__submit-button')
time.sleep(3 + response_delay)
log_in_button.click()
time.sleep(3 + response_delay)
jobs = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ember26"))) # Explicit wait
jobs.click()
time.sleep(3 + response_delay)
search_job = driver.find_element_by_class_name('jobs-search-box__text-input')
time.sleep(3 + response_delay)
search_job.send_keys('data scientist')
time.sleep(3 + response_delay)
location = driver.find_element_by_xpath(
    "//input[@class='jobs-search-box__text-input']//following::input[2]")
location.clear()
time.sleep(3 + response_delay)
location.send_keys('Worldwide')
time.sleep(3 + response_delay)
search_job_button = driver.find_element_by_class_name('jobs-search-box__submit-button')
search_job_button.click()
time.sleep(3 + response_delay)
html = driver.page_source
print(html)
time.sleep(3 + response_delay)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
container = soup.find('ul', class_ = 'jobs-search-results__list')
print(soup)
print('Obtenidos {} puestos de trabajo'.format(len(container)))

# LOGIN - Using Tor and changing proxies
# proxy = my_Proxy("127.0.0.1", 9050)
# proxy.get("https://www.linkedin.com/")
# print(proxy.page_source)
# buscar = proxy.find_element_by_class_name('search-global-typeahead__input')
# sleep(3)
# buscar.send_keys('data scientist')
# buscar.send_keys(Keys.RETURN)
# html = proxy.page_source
# print(html)
# soup = BeautifulSoup(html, 'lxml')
# container = soup.find('ul', class_ = 'jobs-search-results__list')
# print(soup)
# print('Obtained {} jobs.'.format(len(container)))
# cambia_IP()
