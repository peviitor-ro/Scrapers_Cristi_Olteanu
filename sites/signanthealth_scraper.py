#
#  Company - > SignantHealth
# Link -> https://globalus232.dayforcehcm.com/CandidatePortal/en-US/signanthealth?l=3
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup

def get_soup(link):

    response = requests.get(link,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_jobs():

    list_jobs = []

    page = 1
    flag = True

    while flag:

        jobs = get_soup(f'https://globalus232.dayforcehcm.com/CandidatePortal/en-US/signanthealth?page={page}'
                        ).find_all('li', class_='search-result')

        if len(jobs) > 0:

            for job in jobs:
                link = 'https://globalus232.dayforcehcm.com' + job.find('a')['href']
                title = job.find('a').text
                location = job.find('div', class_='posting-subtitle').text

                job_type_text = get_soup(link).find('div', class_="job-posting-section").text

                if "remote" in job_type_text.lower() or  "#remote" in job_type_text.lower():
                    job_type = 'remote'
                elif 'hybrid' in job_type_text.lower():
                    job_type = 'hybrid'
                else:
                    job_type = "on-site"

                if 'Romania' in location:
                    list_jobs.append({
                        "job_title": title,
                        "job_link": link,
                        "company": "SignantHealth",
                        "country": "Romania",
                        "city": 'Iasi',
                        "remote": job_type
                    })

        else:
            flag = False
        page += 1

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'SignantHealth'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('SignantHealth',
                  'https://tukuz.com/wp-content/uploads/2019/09/signant-health-logo-vector.png'
                  ))
