#
# Company - > Picsart
# Link -> https://picsart.com/jobs/vacancies/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import uuid

def get_jobs():

    list_jobs = []

    response = requests.get('https://api.picsart.com/careers/jobs',headers=DEFAULT_HEADERS).json()

    for job in response:
        country = job['location'].split(',')[-1]

        if 'Romania' in country:

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": job['title'],
                "job_link": 'https://picsart.com/jobs/vacancies/' + job['id'],
                "company": "Picsart",
                "country": "Romania",
                "city": job['city']
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