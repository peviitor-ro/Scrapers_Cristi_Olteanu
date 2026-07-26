#
#  Company - > kirchhoff
# Link -> https://kirchhoff-automotive.com/careers/jobs/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county

JOBS_URL = 'https://kirchhoff-automotive.com/careers/jobs/'


def get_jobs():
    list_jobs = []

    response = requests.get(JOBS_URL, headers=DEFAULT_HEADERS, timeout=30)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('a', class_='lumesse-job-item')

    for job in jobs:
        country = job.get('data-country', '').lower()
        if country != 'romania':
            continue

        title_el = job.find('div', class_='lumesse-job-title')
        location_el = job.find('div', class_='lumesse-job-location')

        if not title_el:
            continue

        title = title_el.text.strip()
        job_link = job.get('href', '')
        city = location_el.text.strip() if location_el else 'Pitesti'

        list_jobs.append({
            "job_title": title,
            "job_link": job_link,
            "company": "Kirchhoff",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": 'on-site'
        })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Kirchhoff'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Kirchhoff',
                  'https://kirchhoff-automotive.com/wp-content/uploads/2025/03/Kirchhoff_Karriere_Logo_Weiss.svg'
                  ))
