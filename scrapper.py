from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.keys import Keys

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

# LOGIN - Web scrapping usgin normal IP
driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
driver.get("https://www.linkedin.com")
sleep(3)
username = driver.find_element_by_id("session_key")
sleep(3)
username.send_keys('david.herrera@fw025.com')
password = driver.find_element_by_name('session_password')
sleep(3)
password.send_keys('3240hdicomo_98800')
log_in_button= driver.find_element_by_class_name('sign-in-form__submit-button')
sleep(3)
log_in_button.click()
sleep(3)
# saltar_num = driver.find_element_by_class_name('secondary-action')
# sleep(3)
# saltar_num.click()
# sleep(3)
# confirm_button = driver.find_element_by_class_name('primary-action-new')
# sleep(3)
# confirm_button.click()
# FIN LOGIN
# START SEARCHING
buscar = driver.find_element_by_class_name('search-global-typeahead__input')
sleep(3)
buscar.send_keys('data scientist')
sleep(3)
buscar.send_keys(Keys.RETURN)
html = driver.page_source
print(html)
sleep(5)
admi = driver.find_element_by_xpath("//button[@aria-label='Ver solo resultados de Empleos.']")
admi.click()
sleep(5)
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
