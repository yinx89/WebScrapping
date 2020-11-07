from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
from tqdm import tqdm

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
sleep(5)
admi = driver.find_element_by_xpath("//button[@aria-label='Ver solo resultados de Empleos.']")
admi.click()
sleep(3)
location = driver.find_element_by_xpath("//input[@class='jobs-search-box__text-input']//following::input[2]")
location.clear()
sleep(1)
location.send_keys('Scotland')
sleep(1)
search_job_button = driver.find_element_by_class_name('jobs-search-box__submit-button')
search_job_button.click()
sleep(3)

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
solicitudes = []
empleados = []
quick_application = []
emails = []
visualizaciones = []
recommendedFlavor = []

html = driver.page_source
soup = BeautifulSoup(html, 'lxml', from_encoding="utf-8")

paginas_ul = soup.find("ul", class_='artdeco-pagination__pages--number')
paginas_li = paginas_ul.find_all("li", class_="artdeco-pagination__indicator--number")
total_paginas = paginas_li[-1].button.span.text

for pagina in tqdm(range(2,int(total_paginas)), desc="Paginas"):
# for pagina in tqdm(range(2,20), desc="Paginas"):
    
    jobs_per_page = len(soup.find_all('li',class_="jobs-search-results__list-item"))
    
    for i in tqdm(range(0, jobs_per_page-1, 4), desc="Scroll down"):
        js_string = ("const item = document.querySelectorAll('.jobs-search-results__list-item')[{0}];try{{item.scrollIntoView({{ behavior: 'smooth', block: 'start' }});}}catch(e){{}}").format(i)
        while True:
            try:
                driver.execute_script(js_string) 
            except TypeError:
                continue
            break
        sleep(2)
    last_element = "const item = document.querySelectorAll('.artdeco-pagination__indicator--number')[0];try{item.scrollIntoView({ behavior: 'smooth', block: 'start' });}catch(e){}"
    while True:
        try:
            driver.execute_script(last_element) 
        except TypeError:
            continue
        break
    sleep(1)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml', from_encoding="utf-8")
    puestos = soup.find('ul', class_ = 'jobs-search-results__list')
    print('Obtenidos {} puestos de trabajo'.format(len(puestos.find_all('li',class_="jobs-search-results__list-item"))))
    
    # jobs = soup.findAll(class_ = 'jobs-search-results__list-item')
    
    # for loop for job title, company, id, location and date posted
    for job in tqdm(soup.find_all(class_ = 'jobs-search-results__list-item'), desc="First loop"):
        
        # job title job-card-list__title
        job_titles = job.find("a", class_="job-card-list__title")
        if job_titles is not None:
            post_title.append(job_titles.text.strip())
        else:
            post_title.append("None")
        
        # linkedin job id
        if job_titles is not None:
            job_ids = job_titles['href']
            job_ids = re.findall(r'/jobs/view/(\d+)/',job_ids)[0]
            job_id.append(job_ids)
        else:
            job_id.append("None")
        
        # company name
        company_names = job.find("a", class_="job-card-container__company-name")
        if company_names is not None:
            company_name.append(company_names.text.strip())
        else:
            company_name.append("None")
        
        # job location job-card-container__metadata-item
        job_locations = job.find("li", class_="job-card-container__metadata-item")
        if job_locations is not None:
            job_location.append(job_locations.text.strip())
        else:
            job_location.append("None")
        
        # posting date soup.find("a",{"class":"Label"})
        post_dates = job.find("time")
        if post_dates is not None and post_dates.has_attr('datetime'):
            post_date.append(post_dates['datetime'])
        else:
            post_date.append("None")
            
        quick_application_element = job.find(lambda tag:tag.name=="li" and "Solicitud sencilla" in tag.text)
        if quick_application_element is not None:
            quick_application.append(True if quick_application_element.text.strip() == "Solicitud sencilla" else False)
        else:
            quick_application.append(False)
        
        if job_titles is not None:
            recommendedFlavor_element = job_titles['href']
            recommendedFlavor_element = re.findall('[?&]recommendedFlavor=([^&#]+)', recommendedFlavor_element)
            if len(recommendedFlavor_element) > 0:
                recommendedFlavor.append(recommendedFlavor_element[0])
            else:
                recommendedFlavor.append("None")
        else:
            recommendedFlavor.append("None")

    # for loop for job description and criterias
    for x in tqdm(range(0,len(soup.find_all(class_ = 'jobs-search-results__list-item'))), desc="Second loop"):
        
        lista = driver.find_elements_by_class_name("job-card-list__title")
        # clicking on different job containers to view information about the job
        while (len(soup.find_all(class_ = 'jobs-search-results__list-item')) > len(lista)):
            for i in tqdm(range(0, jobs_per_page-1, 4), desc="Scroll down"):
                js_string = ("const item = document.querySelectorAll('.jobs-search-results__list-item')[{0}];try{{item.scrollIntoView({{ behavior: 'smooth', block: 'start' }});}}catch(e){{}}").format(i)
                while True:
                    try:
                        driver.execute_script(js_string) 
                    except TypeError:
                        continue
                    break
                sleep(2)
            last_element = "const item = document.querySelectorAll('.artdeco-pagination__indicator--number')[0];try{item.scrollIntoView({ behavior: 'smooth', block: 'start' });}catch(e){}"
            while True:
                try:
                    driver.execute_script(last_element) 
                except TypeError:
                    continue
                break
            sleep(1)
            lista = driver.find_elements_by_class_name("job-card-list__title")
            
        title = lista[x]
        title.click()
        sleep(3)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml', from_encoding="utf-8")
        container = soup.find("div", class_='jobs-description-content__text')
        
        # job description
        description = container.find('span')
        if description is not None:
            job_desc.append(description.text.strip().replace(';', ':').replace('"', "'"))
        else:
            job_desc.append("None")
        
        details = container.find('div',class_='jobs-description-details')
        details_div = details.find_all('div')
        
        # Seniority level
        level_element = soup.find(lambda tag:tag.name=="h3" and "Nivel de experiencia" in tag.text)
        if level_element is not None:
            p_level = level_element.find_next('p').contents[0]
            level.append(str(p_level.string).strip())
        else:
            level.append("None")
        
        # Employment type
        emp_type_element = soup.find(lambda tag:tag.name=="h3" and "Tipo de empleo" in tag.text)
        if emp_type_element is not None:
            p_emp_type = emp_type_element.find_next('p').contents[0]
            emp_type.append(str(p_emp_type.string).strip())
        else:
            emp_type.append("None")    
        
        # Job function
        functions_list_element = soup.find(lambda tag:tag.name=="h3" and ("Funciones laborales" in tag.text or "Función laboral" in tag.text))
        if functions_list_element is not None:
            functions_list = functions_list_element.find_next('ul').get_text(', ', strip=True)
            functions.append(functions_list)
        else:
            functions.append("None")  
        
        # Industries
        industries_list_element = soup.find(lambda tag:tag.name=="h3" and ("Sector" in tag.text or "Sectores" in tag.text))
        if industries_list_element is not None:
            industries_list = industries_list_element.find_next('ul').get_text(', ', strip=True)
            industries.append(industries_list)
        else:
            industries.append("None")  
        
        #ul = soup.find("ul", class_="artdeco-list artdeco-list--border artdeco-list--grid t-12 t-black--light jobs-details-job-summary")
        solicitudes_element = soup.find(lambda tag:tag.name=="span" and "solicitudes" in tag.text)
        if solicitudes_element is not None:
            solicitudes_search = re.search('[0-9]+',solicitudes_element.text.strip())
            if solicitudes_search is not None:
                solicitudes.append(int(solicitudes_search.group(0)))
            else:
                if soup.find(lambda tag:tag.name=="span" and "Ya no se aceptan solicitudes para este empleo" in tag.text) is not None:
                    solicitudes.append("Ya no se aceptan solicitudes para este empleo.")
                else:
                    solicitudes.append("None")
        else:
            solicitudes.append("None")
        
        empleados_element = soup.find(lambda tag:tag.name=="span" and "empleados" in tag.text)
        if empleados_element is not None:
            empleados.append(empleados_element.text.strip().replace(" empleados",""))
        else:
            empleados.append("None")
            
        emails_list = re.findall(r'[\w\.-]+@[\w\.-]+', description.text.strip())
        if emails_list is not None:
            emails_elements = ", ".join(emails_list)
            emails.append(emails_elements)
        else:
            emails.append("None")
        
        visualizaciones_element = soup.find(lambda tag:tag.name=="span" and "visualizaciones" in tag.text)
        if visualizaciones_element is not None:
            visualizaciones.append(int(re.search('[0-9]+',visualizaciones_element.text.strip()).group(0)))
        else:
            visualizaciones.append("None")

        x = x + 1
    
    next_page_string = ("//button[@aria-label='Página {0}']").format(pagina)
    next_page = driver.find_element_by_xpath(next_page_string)
    next_page.click()
    sleep(3)
    
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
print(len(solicitudes))
print(len(empleados))
print(len(quick_application))
print(len(emails))
print(len(visualizaciones))
print(len(recommendedFlavor))

job_data = pd.DataFrame({'Job ID': job_id,
'Date': post_date,
'Company Name': company_name,
'Title': post_title,
'Location': job_location,
'Description': job_desc,
'Level': level,
'Type': emp_type,
'Functions': functions,
'Industries': industries,
'Solicitudes': solicitudes,
'Empleados': empleados,
'Quick Application': quick_application,
'Emails': emails,
'Visualizaciones': visualizaciones,
'Recommended Flavor': recommendedFlavor
})

job_data['Description'] = job_data['Description'].str.replace('\n',' ')

job_data.to_csv("clean.csv",encoding='utf-8')

print("Done!")

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
