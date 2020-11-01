from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re

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
username = driver.find_element_by_class_name('input__input')
sleep(3)
username.send_keys('juanjo.hdicomo@gmail.com')
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

sleep(3)
# driver.execute_script("document.getElementsByClassName('jobs-search__left-rail')[0].scrollBy();")
# driver.execute_script("const i = 0;const item = document.querySelectorAll('.jobs-search-results__list-item')[i];item.forEach(item => {item.scrollIntoView({ behavior: 'smooth', block: 'start' });});")
driver.execute_script("const item = document.querySelectorAll('.jobs-search-results__list-item')[0];item.scrollIntoView({ behavior: 'smooth', block: 'start' });")
sleep(1)
driver.execute_script("const item = document.querySelectorAll('.jobs-search-results__list-item')[5];item.scrollIntoView({ behavior: 'smooth', block: 'start' });")
sleep(1)
driver.execute_script("const item = document.querySelectorAll('.jobs-search-results__list-item')[10];item.scrollIntoView({ behavior: 'smooth', block: 'start' });")
sleep(1)
driver.execute_script("const item = document.querySelectorAll('.jobs-search-results__list-item')[15];item.scrollIntoView({ behavior: 'smooth', block: 'start' });")
sleep(1)
driver.execute_script("const item = document.querySelectorAll('.jobs-search-results__list-item')[20];item.scrollIntoView({ behavior: 'smooth', block: 'start' });")
sleep(1)
driver.execute_script("const item = document.querySelectorAll('.jobs-search-results__list-item')[24];item.scrollIntoView({ behavior: 'smooth', block: 'start' });")
sleep(1)


# sleep(20)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
container = soup.find('ul', class_ = 'jobs-search-results__list')
print(soup)
print('Obtenidos {} puestos de trabajo'.format(len(container)))

# setting up list for job information
job_id = []
post_title = []
company_name = []
post_date = []
job_location = []
job_desc = []
level = []
emp_type = []
functions = []
industries = []

# jobs = soup.findAll(class_ = 'jobs-search-results__list-item')

# for loop for job title, company, id, location and date posted
for job in soup.find_all(class_ = 'jobs-search-results__list-item'):
    
    # job title job-card-list__title
    job_titles = job.find("a", class_="job-card-list__title")
    if job_titles is not None:
        post_title.append(job_titles.text)
    else:
        post_title.append("None")
    print(job_titles)
    
    # linkedin job id
    job_ids = job.find('a', href=True)
    if job_ids is not None:
        job_ids = job_ids['href']
        job_ids = re.findall(r'(?!-)([0-9]*)(?=\?)',job_ids)[0]
        job_id.append(job_ids)
    else:
        job_id.append("None")
    print(job_ids)
    
    # company name
    company_names = job.find("a", class_="job-card-container__company-name")
    if company_names is not None:
        company_name.append(company_names.text)
    else:
        company_name.append("None")
    print(company_names)
    
    # job location job-card-container__metadata-item
    job_locations = job.find("li", class_="job-card-container__metadata-item")
    if job_locations is not None:
        job_location.append(job_locations.text)
    else:
        job_location.append("None")
    print(job_location)
    
    # posting date soup.find("a",{"class":"Label"})
    post_dates = job.find("time")
    if post_dates is not None:
        post_date.append(post_dates.text)
    else:
        post_date.append("None")
    print(post_date)

print(len(job_id))
print(len(post_date))
print(len(company_name))
print(len(post_title))
print(len(job_location))
print(len(job_desc))
print(len(level))
print(len(emp_type))
print(len(functions))
print(len(industries))

job_data = pd.DataFrame({'Job ID': job_id,
'Date': post_date,
'Company Name': company_name,
'Post': post_title,
'Location': job_location
})

job_data.head()

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
