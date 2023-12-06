#
# Company - > PayU
# Link -> https://corporate.payu.com/job-board/?location%5B%5D=bucharest-romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_soup(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_job_type(url):

    t = get_soup(url).find_all('li')
    job_type_ = 'on-site'
    for ts in t:

        if 'hybrid' in ts.text:
            job_type_ = 'hybrid'
        elif 'remote' in ts.text:
            job_type_ = 'remote'
    return job_type_


def get_jobs():

    jobs_list = []
    jobs = get_soup('https://corporate.payu.com/job-board/?location%5B%5D=bucharest-romania'
                    ).find_all('li', class_='job-entry')

    for job in jobs:

        link = job.find('a', class_='title')['href']
        title = job.find('h3').text
        city = job.find('a').text.split(',')[-2].split()[-1]
        job_type = get_job_type(link)

        jobs_list.append({
            "job_title": title,
            "job_link": link,
            "company": "PayU",
            "country": "Romania",
            "city": city,
            "remote": job_type
        })

    return jobs_list

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'PayU'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('PayU',
                  'https://corporate.payu.com/wp-content/themes/global-website/assets/src/images/payu-logo.svg'
                  ))

