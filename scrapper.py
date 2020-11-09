#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Oct-Nov 2020

@author: Íñigo Álvarez y Ginés Molina

Usage: scrapper.py

Este script obtiene los resultados de búsqueda según un puesto de trabajo concreto
en un lugar concreto. Los resultados de la búsqueda son limitados a 40 páginas
(ordenados por relevancia). Se deberá utilizar una cuenta de LinkedIn a través
de un usuario y contraseña. El propio script tiene una función que reintenta la
ejecución de las funciones propensas a error y se aplican otras técnicas
como el cambio del UserAgent. Finalmente el archivo generado en la raiz del
proyecto tiene como nombre "results.csv".

"""

import re
import functools
import sys
import time
from time import sleep

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from fake_useragent import UserAgent


MAX_DELAY = 10
BASE_URL = "https://www.linkedin.com"
USER_MAIL = "juanjo.hdicomo@gmail.com"
USER_PASS = "3240hdicomo_98800"
DESIRED_JOB = "data scientist"
LOCATION = "Scotland"
PATH = "/usr/local/bin/geckodriver"


def retry_if_error(fun):
    '''
    Esta función utiliza el decorador @retry_if_error para comprobar si hay
    un error en cada una de las funciones. Lo primero que se realiza es un cambio
    de UserAgent y posteriormente se aplican retardos automáticos y proporcionales.

            Parameters:
                    fun (function): Cualquier función con el decorador

            Returns:
                    wrapper: Ejecución de métodos para reintentarlo
    '''
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        auto_delay = 0
        while True:
            sleep(auto_delay)
            try:
                return fun(*args, **kwargs)
            except requests.exceptions.RequestException:
                print("ERROR - Applying delay", file=sys.stderr)
                auto_delay = min(auto_delay + 1, MAX_DELAY)
                continue
    return wrapper

class Information():
    """
    Clase que representan las variables de las observaciones en listas.

    ...

    Attributes
    ----------
    job_id : list
        id de la oferta
    post_title : list
        titulo de la oferta
    company_name : list
        compañia de la oferta
    post_date : list
        fecha de publicación
    job_location : list
        localización de la oferta
    job_desc : list
        descripción del trabajo
    level : list
        nivel de experiencia
    emp_type : list
        tipo de empleo
    functions : list
        funciones del trabajo
    industries : list
        industrias involucradas
    solicitudes : list
        numero de solicitudes
    empleados : list
        número de empleados de la compañía
    quick_application : list
        aplicación rápida o no
    emails : list
        emails asociados a la oferta
    visualizaciones : list
        visualizaciones totales de la oferta
    recommendedFlavor : list
        tipo de oferta

    Methods
    -------
    print_length():
        Imprime las longitudes de las listas
    save_file():
        Obtiene el pandas Dataframe y lo guarda como .csv
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
        Constructor de la clase
        """

    @retry_if_error
    def print_length(self):
        """
        Imprime las longitudes de las listas
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

    @retry_if_error
    def save_file(self):
        """
        Obtiene el pandas Dataframe y lo guarda como .csv
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
        job_data.to_csv("results.csv", encoding='utf-8-sig')
        print("Done!")

def set_useragent():
    '''
    Establece el UserAgent de Firefox a través del perfil.
    Se podría utilizar tambien para cambiar el UserAgent pero no nos ha causado
    problemas.

            Parameters:
                    useragent (UserAgent()): Fake UserAgent
                    driver (webdriver.Firefox()): Driver

            Returns:
                    driver (webdriver.Firefox()): new Driver
    '''
    # useragent = UserAgent()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override",
                           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:82.0) Gecko/20100101 Firefox/82.0")
    # profile.set_preference("general.useragent.override", useragent.random)
    driver = webdriver.Firefox(firefox_profile=profile, executable_path=PATH)
    # print(driver.execute_script("return navigator.userAgent"))
    return driver

@retry_if_error
def login():
    '''
    Proceso de login de usuario. Se utilizan esperas implícitas.

            Returns:
                    driver (webdriver.Firefox()): Driver
    '''
    driver = set_useragent()
    response_delay = 0
    first_t = time.time()
    driver.get(BASE_URL)
    response_delay = time.time() - first_t
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

@retry_if_error
def search(driver):
    '''
    Proceso de búsqueda de resultados en la web.

            Parameters:
                    driver (webdriver.Firefox()): Driver
    '''
    buscar = driver.find_element_by_class_name('search-global-typeahead__input')
    sleep(3)
    buscar.send_keys(DESIRED_JOB)
    sleep(3)
    buscar.send_keys(Keys.RETURN)
    sleep(5)
    admi = driver.find_element_by_xpath("//button[@aria-label='Ver solo resultados de Empleos.']")
    admi.click()
    sleep(3)
    location = driver.find_element_by_xpath(
        "//input[@class='jobs-search-box__text-input']//following::input[2]"
        )
    location.clear()
    sleep(1)
    location.send_keys(LOCATION)
    sleep(1)
    search_job_button = driver.find_element_by_class_name('jobs-search-box__submit-button')
    search_job_button.click()
    sleep(3)

@retry_if_error
def get_soup_from_page(driver):
    '''
    Obtiene el objeto BeautifulSoup para poder analizarlo posteriormente.

            Parameters:
                    driver (webdriver.Firefox()): Driver

            Returns:
                    soup (BeautifulSoup()): BS object
    '''
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml', from_encoding="utf-8")
    return soup

@retry_if_error
def scroll_down(driver, jobs_per_page):
    '''
    Realiza scroll-down en grupos de resultados de 4 elementos
    hasta llegar a los elementos de Pagination con JavaScript.

            Parameters:
                    driver (webdriver.Firefox()): Driver
    '''
    for i in tqdm(range(0, jobs_per_page-1, 4), desc="Scroll down"):
        js_string = ("const item = document.querySelectorAll('.jobs-search-results__list-item')[{0}];try{{item.scrollIntoView({{ behavior: 'smooth', block: 'start' }});}}catch(e){{}}").format(i)
        driver.execute_script(js_string)
        sleep(2)
    last_element = "const item = document.querySelectorAll('.artdeco-pagination__indicator--number')[0];try{item.scrollIntoView({ behavior: 'smooth', block: 'start' });}catch(e){}"
    driver.execute_script(last_element)
    sleep(1)

@retry_if_error
def search_list_title(query, data):
    '''
    Búsqueda en el elemento title.

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
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

@retry_if_error
def search_company_names(query, data):
    '''
    Búsqueda del nombre de la compañia

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        data.company_name.append(query.text.strip())
    else:
        data.company_name.append("None")
    return data

@retry_if_error
def search_job_locations(query, data):
    '''
    Búsqueda de la localización

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        data.job_location.append(query.text.strip())
    else:
        data.job_location.append("None")
    return data

@retry_if_error
def search_post_dates(query, data):
    '''
    Búsqueda de la fecha de publicación

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None and query.has_attr('datetime'):
        data.post_date.append(query['datetime'])
    else:
        data.post_date.append("None")
    return data

@retry_if_error
def search_quick_application(query, data):
    '''
    Búsqueda si hay botón Quick Application

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        data.quick_application.append(
            bool(query.text.strip() == "Solicitud sencilla")
            )
    else:
        data.quick_application.append(False)
    return data

@retry_if_error
def search_description(query, data):
    '''
    Obtención de la descripción

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        # Dos métodos, haciendo replace() o strip()
        # data.job_desc.append(query.text.replace("\n"," ").replace("\t"," ").replace(';', ':').replace('"', "'"))
        data.job_desc.append(query.text.strip().replace(';', ':').replace('"', "'"))
    else:
        data.job_desc.append("None")
    return data

@retry_if_error
def search_level(query, data):
    '''
    Búsqueda del nivel de la oferta

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        p_level = query.find_next('p').contents[0]
        data.level.append(str(p_level.string).strip())
    else:
        data.level.append("None")
    return data

@retry_if_error
def search_emp_type(query, data):
    '''
    Búsqueda del tipo de empleo

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        p_emp_type = query.find_next('p').contents[0]
        data.emp_type.append(str(p_emp_type.string).strip())
    else:
        data.emp_type.append("None")
    return data

@retry_if_error
def search_functions(query, data):
    '''
    Búsqueda de las funciones de la oferta

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        functions_list = query.find_next('ul').get_text(', ', strip=True)
        data.functions.append(functions_list)
    else:
        data.functions.append("None")
    return data

@retry_if_error
def search_industries(query, data):
    '''
    Búsqueda de las industrias

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        industries_list = query.find_next('ul').get_text(', ', strip=True)
        data.industries.append(industries_list)
    else:
        data.industries.append("None")
    return data

@retry_if_error
def search_solicitudes(query, no_sol_query, data):
    '''
    Búsqueda del número de solicitudes

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    no_sol_query(BS query): Consulta si no se aceptan aplicaciones
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
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

@retry_if_error
def search_empleados(query, data):
    '''
    Obtención del número de empleados de la compañía

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        data.empleados.append(query.text.strip().replace(" empleados", ""))
    else:
        data.empleados.append("None")
    return data

@retry_if_error
def search_emails(query, data):
    '''
    Obtiene si hay direcciones de correo en la descripción

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        emails_elements = ", ".join(query)
        data.emails.append(emails_elements)
    else:
        data.emails.append("None")
    return data

@retry_if_error
def search_visualizaciones(query, data):
    '''
    Obtiene el número de visualizaciones totales de la oferta

            Parameters:
                    query (BS query): Consulta para obtener el elemento
                    data (Information()): resultados

            Returns:
                    data (Information()): resultados
    '''
    if query is not None:
        data.visualizaciones.append(
            int(re.search('[0-9]+', query.text.strip())
                .group(0)))
    else:
        data.visualizaciones.append("None")
    return data


@retry_if_error
def search_information(driver):
    '''
    Se le pasa el driver y se obtienen los resultados de la búsqueda. Es la función
    core del script, en ella se van estableciendo los tiempos, se van iterando
    los bucles y es desde la que parten todas las acciones.

            Parameters:
                    driver (webdriver.Firefox()): Driver

            Returns:
                    data (Information()): resultados de la búsqueda
    '''
    data = Information()

    soup = get_soup_from_page(driver)

    paginas_ul = soup.find("ul", class_='artdeco-pagination__pages--number')
    paginas_li = paginas_ul.find_all("li", class_="artdeco-pagination__indicator--number")
    total_paginas = paginas_li[-1].button.span.text

    for pagina in tqdm(range(2, int(total_paginas)+1), desc="Paginas"):
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

            lista = driver.find_elements_by_class_name("job-card-list__title")
            while len(soup.find_all(class_='jobs-search-results__list-item')) > len(lista):
                scroll_down(driver, jobs_per_page)
                lista = driver.find_elements_by_class_name("job-card-list__title")
            title = lista[result]
            title.click()
            sleep(3)

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
                lambda tag: tag.name == "span" and "empleados" in tag.text and tag.previousSibling.name == "li"), data)
            data = search_emails(re.findall(r'[\w\.-]+@[\w\.-]+', container.find('span').text.strip()), data)
            data = search_visualizaciones(soup.find(
                lambda tag: tag.name == "span" and "visualizaciones" in tag.text), data)

            result = result + 1

        next_page_string = ("//button[@aria-label='Página {0}']").format(pagina)
        next_page = driver.find_element_by_xpath(next_page_string)
        next_page.click()
        sleep(3)

    return data

def main():
    '''
    Función principal. Desde ella comienza el script y establece los pasos.
    '''
    driver = login()
    search(driver)
    diccionario = search_information(driver)
    diccionario.print_length()
    diccionario.save_file()


if __name__ == "__main__":
    main()
