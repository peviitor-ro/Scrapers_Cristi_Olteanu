#
# Company - > Picsart
# Link -> https://picsart.com/jobs/vacancies/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county
from _validate_city import validate_city


def get_job_types(job_id):

    res = requests.get('https://api.picsart.com/careers/jobs/' + job_id).json()['description']
    soup = BeautifulSoup(res, 'lxml').find_all('li', attrs={'style': 'line-height: 1.1;'})[1].text

    if 'hybrid' in soup.lower():
        job_type_ = 'hybrid'
    elif 'remote' in soup.lower():
        job_type_ = 'remote'
    else:
        job_type_ = 'on-site'
    return job_type_


def get_jobs():

    list_jobs = []
    response = requests.get('https://api.picsart.com/careers/jobs', headers=DEFAULT_HEADERS).json()

    for job in response:
        country = job['location'].split(',')[-1]

        if 'Romania' in country:
            job_type = get_job_types(job['id'])
            city = validate_city(job['city'])

            list_jobs.append({
                "job_title": job['title'],
                "job_link": 'https://picsart.com/jobs/vacancies/' + job['id'],
                "company": "Picsart",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": job_type
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Picsart'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Picsart',
                  'https://1000logos.net/wp-content/uploads/2022/11/Picsart-Logo-1536x864.png'
                  ))