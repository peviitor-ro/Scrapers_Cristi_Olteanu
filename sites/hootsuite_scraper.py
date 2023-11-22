#
# Company - > hootsuite
# Link -> https://careers.hootsuite.com/jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests


def get_jobs():

    jobs_list = []

    response = requests.get('https://boards-api.greenhouse.io/v1/boards/hootsuite/jobs?content=true',
                            headers=DEFAULT_HEADERS).json()['jobs']
    for job in response:
        cities = []
        for office in job['offices']:
            city = office['name']

            if 'Romania' in office['location']:
                cities.append(city)
                jobs_list.append({
                    "job_title": job['title'],
                    "job_link": job['absolute_url'].replace('jobs', 'job'),
                    "company": "hootsuite",
                    "country": "Romania",
                    "city": cities,
                })

    return jobs_list

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list


company_name = 'hootsuite'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('hootsuite',
                  'https://www.juniors.ro/storage/company_logo_static/hootsuite-logo.png'
                  ))

