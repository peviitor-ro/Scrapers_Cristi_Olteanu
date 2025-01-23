#
#  Company - > Antal
# Link -> https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page=
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
from _county import get_county
from _validate_city import validate_city


def get_soup(url):

    session = requests.Session()
    response = session.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_nr_pages():

    soup_pages = get_soup('https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page=')
    nr_pages = int(soup_pages.find('a', class_='next text page-numbers')['href'].split('=')[-1])
    print(nr_pages)
    return nr_pages


def get_jobs():

    list_jobs = []

    for page in range(12, get_nr_pages()+1, 1):

        soup_jobs = get_soup(f'https://www.antal.com/jobs?keywords=&sector=&location=1721&type=&page={page}')
        jobs = soup_jobs.find_all('a')
        for job in jobs:
            print(job.get('href'))


    #     for job in jobs:
    #         text = job.find('a', class_='job-card__link more-link')
    #         if text is not None:
    #             link = text['href']
    #             title = job.find('a').text
    #             try:
    #                 city = job.find('ul', class_='job-card__details').text.split(',')[-2].split()[-1]
    #             except:
    #                 city = job.find('ul', class_='job-card__details').text.split(',')[-1].split()[-1]
    #
    #             city = validate_city(city)
    #
    #             if 'on site' in title.lower() or 'on-site' in title.lower():
    #                 job_type = 'on-site'
    #             elif 'hybrid' in title.lower() or 'hibrid' in title.lower():
    #                 job_type = 'hybrid'
    #             elif 'remote' in title.lower() or 'Remote' in title.lower() or 'ful-remote' in title.lower():
    #                 job_type = 'remote'
    #             else:
    #                 job_type = 'on-site'
    #
    #             list_jobs.append({
    #                 "job_title": title,
    #                 "job_link": link,
    #                 "company": "Antal",
    #                 "country": "Romania",
    #                 "city": city,
    #                 "county": get_county(city),
    #                 "remote": job_type
    #             })
    # print(len(list_jobs))
    # return list_jobs
get_jobs()

# @update_peviitor_api
# def scrape_and_update_peviitor(company_name, data_list):
#     """
#     Update data on peviitor API!
#     """
#
#     return data_list
#
#
# company_name = 'Antal'
# data_list = get_jobs()
# scrape_and_update_peviitor(company_name, data_list)
#
# print(update_logo('Antal',
#                   'https://www.antal.com/app/public/images/logo.png'
#                   ))

