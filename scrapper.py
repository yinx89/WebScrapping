#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct-Nov 2020

@author: Íñigo Álvarez y Ginés Molina

Usage: scrapper.py

The docstrings for Python script should document the script's functions and command-line
syntax as a usable message.

It should serve as a quick reference to all the functions and arguments.
"""

import re
import functools
import sys
from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
# from stem import Signal
# from stem.control import Controller
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.common.exceptions import TimeoutException


MAX_DELAY = 10
BASE_URL = "https://www.linkedin.com"
USER_MAIL = "juanjo.hdicomo@gmail.com"
USER_PASS = "3240hdicomo_98800"
PATH = "/usr/local/bin/geckodriver"

def retry_if_fail(fun):
    '''
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        delay = 0
        while True:
            sleep(delay)
            try:
                return fun(*args, **kwargs)
            except requests.exceptions.RequestException:
                print("Error on request, applying delay", file=sys.stderr)
                delay = min(delay + 1, MAX_DELAY)
                continue
    return wrapper

class Information():
    """
    Clase para las columnas.

    ...

    Attributes
    ----------
    name : str
        first name of the person
    surname : str
        family name of the person
    age : int
        age of the person

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """
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

    def __init__(self):
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        ----------
            name : str
                first name of the person
            surname : str
                family name of the person
            age : int
                age of the person
        """
    @retry_if_fail
    def print_length(self):
        """
        Muestra el tamaño de cada columna.

        If the argument 'additional' is passed, then it is appended after the main info.

        Parameters
        ----------
        additional : str, optional
            More info to be displayed (default is None)

        Returns
        -------
        None
        """
        print(len(self.job_id))
        print(len(self.post_date))
        print(len(self.company_name))
        print(len(self.post_title))
        print(len(self.job_location))
        print(len(self.job_desc))
        print(len(self.level))
        print(len(self.emp_type))
        print(len(self.functions))
        print(len(self.industries))
        print(len(self.solicitudes))
        print(len(self.empleados))
        print(len(self.quick_application))
        print(len(self.emails))
        print(len(self.visualizaciones))
        print(len(self.recommendedFlavor))

    @retry_if_fail
    def save_file(self):
        """
        Guarda los datos en un archivo csv..

        If the argument 'additional' is passed, then it is appended after the main info.

        Parameters
        ----------
        additional : str, optional
            More info to be displayed (default is None)

        Returns
        -------
        None
        """
        job_data = pd.DataFrame(
            {
                'Job ID': self.job_id,
                'Date': self.post_date,
                'Company Name': self.company_name,
                'Title': self.post_title,
                'Location': self.job_location,
                'Description': self.job_desc,
                'Level': self.level,
                'Type': self.emp_type,
                'Functions': self.functions,
                'Industries': self.industries,
                'Solicitudes': self.solicitudes,
                'Empleados': self.empleados,
                'Quick Application': self.quick_application,
                'Emails': self.emails,
                'Visualizaciones': self.visualizaciones,
                'Recommended Flavor': self.recommendedFlavor
                })

        job_data['Description'] = job_data['Description'].str.replace('\n', ' ')
        job_data.to_csv("clean.csv", encoding='utf-8-sig')
        print("Done!")

@retry_if_fail
def login():
    '''
    Inicia sesión en la página web.

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    driver = webdriver.Firefox(executable_path=PATH)
    t0 = time.time()
    driver.get(BASE_URL)
    global response_delay
    response_delay = time.time() - t0
    sleep(2 + response_delay)
    # try:
    #     captcha_string = "//h1[text()[0][contains(., 'Vamos a hacer una comprobación rápida de seguridad')]]"
    #     captcha = driver.find_element_by_xpath(captcha_string)
    # except:
    #     print("WAIT")
    # finally:
    #     print("No hay captcha!")
    sleep(2 + response_delay)
    username = driver.find_element_by_class_name('input__input')
    sleep(2 + response_delay)
    username.send_keys(USER_MAIL)
    password = driver.find_element_by_name('session_password')
    sleep(2 + response_delay)
    password.send_keys(USER_PASS)
    log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
    sleep(2 + response_delay)
    log_in_button.click()
    sleep(3)
    return driver

@retry_if_fail
def search(driver):
    '''
    Busca los empleos.

            Parameter:
                    driver

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    
    empleos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ember26"))) # Explicit wait
    empleos.click()
    buscar_empleo = driver.find_element_by_class_name('jobs-search-box__text-input')
    sleep(2 + response_delay)
    buscar_empleo.send_keys('data scientist')
    sleep(2 + response_delay)
    lugar = driver.find_element_by_xpath(
        "//input[@class='jobs-search-box__text-input']//following::input[2]")
    lugar.clear()
    time.sleep(2 + response_delay)
    lugar.clear()
    time.sleep(2 + response_delay)
    lugar.send_keys('Remote')
    time.sleep(2 + response_delay)
    boton_buscar_empleo = driver.find_element_by_class_name('jobs-search-box__submit-button')
    boton_buscar_empleo.click()
    time.sleep(3 + response_delay)

@retry_if_fail
def get_soup_from_page(driver):
    '''
    Devuelve el HTML parseado.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml', from_encoding="utf-8")
    return soup

@retry_if_fail
def scroll_down(driver, jobs_per_page):
    '''
    Baja en los resultados de la búsqueda.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    for i in tqdm(range(0, jobs_per_page-1, 4), desc="Scroll down"):
        js_string = ("const item = document.querySelectorAll('.jobs-search-results__list-item')[{0}];try{{item.scrollIntoView({{ behavior: 'smooth', block: 'start' }});}}catch(e){{}}").format(i)
        driver.execute_script(js_string)
        sleep(2)
    last_element = "const item = document.querySelectorAll('.artdeco-pagination__indicator--number')[0];try{item.scrollIntoView({ behavior: 'smooth', block: 'start' });}catch(e){}"
    driver.execute_script(last_element)
    sleep(1)

@retry_if_fail
def search_list_title(query, data):
    '''
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        data.post_title.append(query.text.strip())

        job_ids = query['href']
        job_ids = re.findall(r'/jobs/view/(\d+)/', job_ids)[0]
        data.job_id.append(job_ids)

        recommendedflavor_element = query['href']
        recommendedflavor_element = re.findall(
            '[?&]recommendedFlavor=([^&#]+)',
            recommendedflavor_element
            )
        if len(recommendedflavor_element) > 0:
            data.recommendedFlavor.append(recommendedflavor_element[0])
        else:
            data.recommendedFlavor.append("None")
    else:
        data.post_title.append("None")
        data.job_id.append("None")
        data.recommendedFlavor.append("None")
    return data

@retry_if_fail
def search_company_names(query, data):
    '''
    Busca y añade el nombre de cada empresa.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        data.company_name.append(query.text.strip())
    else:
        data.company_name.append("None")
    return data

@retry_if_fail
def search_job_locations(query, data):
    '''
    Busca y añade la ubicación del trabajo.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        data.job_location.append(query.text.strip())
    else:
        data.job_location.append("None")
    return data

@retry_if_fail
def search_post_dates(query, data):
    '''
    Busca y añade la fecha de la oferta de empleo.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None and query.has_attr('datetime'):
        data.post_date.append(query['datetime'])
    else:
        data.post_date.append("None")
    return data

@retry_if_fail
def search_quick_application(query, data):
    '''
    Busca si la oferta tiene solicitud sencilla.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        data.quick_application.append(
            bool(query.text.strip() == "Solicitud sencilla")
            )
    else:
        data.quick_application.append(False)
    return data

@retry_if_fail
def search_description(query, data):
    '''
    Busca y añade la descripción de la oferta de empleo.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        data.job_desc.append(query.text.strip().replace(';', ':').replace('"', "'"))
    else:
        data.job_desc.append("None")
    return data

@retry_if_fail
def search_level(query, data):
    '''
    Busca y añade el nivel del puesto ofertado.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        p_level = query.find_next('p').contents[0]
        data.level.append(str(p_level.string).strip())
    else:
        data.level.append("None")
    return data

@retry_if_fail
def search_emp_type(query, data):
    '''
    Busca y añade el tipo de empresa.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        p_emp_type = query.find_next('p').contents[0]
        data.emp_type.append(str(p_emp_type.string).strip())
    else:
        data.emp_type.append("None")
    return data

@retry_if_fail
def search_functions(query, data):
    '''
    Busca y añade las funciones del puesto ofertado.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        functions_list = query.find_next('ul').get_text(', ', strip=True)
        data.functions.append(functions_list)
    else:
        data.functions.append("None")
    return data

@retry_if_fail
def search_industries(query, data):
    '''
    Busca y añade el sector.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        industries_list = query.find_next('ul').get_text(', ', strip=True)
        data.industries.append(industries_list)
    else:
        data.industries.append("None")
    return data

@retry_if_fail
def search_solicitudes(query, no_sol_query, data):
    '''
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        solicitudes_search = re.search('[0-9]+', query.text.strip())
        if solicitudes_search is not None:
            data.solicitudes.append(int(solicitudes_search.group(0)))
        else:
            if no_sol_query is not None:
                data.solicitudes.append("Ya no se aceptan solicitudes para este empleo.")
            else:
                data.solicitudes.append("None")
    else:
        data.solicitudes.append("None")
    return data

@retry_if_fail
def search_empleados(query, data):
    '''
    Busca y añade el número de empleados de la empresa.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        data.empleados.append(query.text.strip().replace(" empleados", ""))
    else:
        data.empleados.append("None")
    return data

@retry_if_fail
def search_emails(query, data):
    '''
    Busca y añade el email de contacto.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        emails_elements = ", ".join(query)
        data.emails.append(emails_elements)
    else:
        data.emails.append("None")
    return data

@retry_if_fail
def search_visualizaciones(query, data):
    '''
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    if query is not None:
        data.visualizaciones.append(
            int(re.search('[0-9]+', query.text.strip())
                .group(0)))
    else:
        data.visualizaciones.append("None")
    return data


@retry_if_fail
def search_information(driver):
    '''
    Search and get the information from the results.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    data = Information()

    soup = get_soup_from_page(driver)

    paginas_ul = soup.find("ul", class_='artdeco-pagination__pages--number')
    paginas_li = paginas_ul.find_all("li", class_="artdeco-pagination__indicator--number")
    total_paginas = paginas_li[-1].button.span.text

    for pagina in tqdm(range(2, int(total_paginas)+2), desc="Paginas"):
        jobs_per_page = len(soup.find_all('li', class_="jobs-search-results__list-item"))
        scroll_down(driver, jobs_per_page)
        soup = get_soup_from_page(driver)

        for job in tqdm(soup.find_all(class_='jobs-search-results__list-item'), desc="First loop"):

            data = search_list_title(job.find("a", class_="job-card-list__title"), data)
            data = search_company_names(job.find("a", class_="job-card-container__company-name"), data)
            data = search_job_locations(job.find("li", class_="job-card-container__metadata-item"), data)
            data = search_post_dates(job.find("time"), data)
            data = search_quick_application(
                job.find(lambda tag: tag.name == "li" and "Solicitud sencilla" in tag.text),
                data)

        for result in tqdm(
                range(0, len(soup.find_all(
                    class_='jobs-search-results__list-item'))), desc="Second loop"):

            lista = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-list__title"))) # Explicit wait
            while len(soup.find_all(class_='jobs-search-results__list-item')) > len(lista):
                scroll_down(driver, jobs_per_page)
                lista = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-list__title"))) # Explicit wait
            title = lista[result]
            title.click()
            time.sleep(1 + response_delay)

            soup = get_soup_from_page(driver)
            container = soup.find("div", class_='jobs-description-content__text')

            data = search_description(container.find('span'), data)
            data = search_level(soup.find(
                lambda tag: tag.name == "h3" and "Nivel de experiencia" in tag.text), data)
            data = search_emp_type(soup.find(
                lambda tag: tag.name == "h3" and "Tipo de empleo" in tag.text), data)
            data = search_functions(soup.find(
                lambda tag: tag.name == "h3" and (
                    "Funciones laborales" in tag.text or "Función laboral" in tag.text)), data)
            data = search_industries(soup.find(
                lambda tag: tag.name == "h3" and ("Sector" in tag.text or "Sectores" in tag.text)), data)
            data = search_solicitudes(soup.find(
                lambda tag: tag.name == "span" and "solicitudes" in tag.text
                ), soup.find(
                    lambda tag: tag.name == "span"
                    and "Ya no se aceptan solicitudes para este empleo"
                    in tag.text), data)
            data = search_empleados(soup.find(
                lambda tag: tag.name == "span" and "empleados" in tag.text), data)
            data = search_emails(re.findall(r'[\w\.-]+@[\w\.-]+', container.find('span').text.strip()), data)
            data = search_visualizaciones(soup.find(
                lambda tag: tag.name == "span" and "visualizaciones" in tag.text), data)

            result = result + 1

        next_page_string = ("//button[@aria-label='Página {0}']").format(pagina)
        next_page = driver.find_element_by_xpath(next_page_string)
        next_page.click()
        time.sleep(1 + response_delay)

    return data

def main():
    '''
    Returns the sum of two decimal numbers in binary digits.

            Parameters:
                    a (int): A decimal integer
                    b (int): Another decimal integer

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    driver = login()
    search(driver)
    diccionario = search_information(driver)
    diccionario.print_length()
    diccionario.save_file()


if __name__ == "__main__":
    main()
