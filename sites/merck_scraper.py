#
#  Company - > Merck
# Link -> https://www.merckgroup.com/en/careers/job.html?s=10&f=0&fjc=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import uuid

def get_jobs():

    response = requests.get('https://search.merckgroup.com/v1/search?s=10&f=0&fjc=Romania&d=global_english&l=en&fc=jobs',
                            headers=DEFAULT_HEADERS).json()['items']
    list_jobs = []

    for job in response:

        id = job['jobid']
        link = f'https://www.merckgroup.com/en/careers/jobs/{id}.html?location=Romania&state=Bucuresti&city=Bucharest&functionalarea=Commercial'

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": job['title'],
            "job_link": link,
            "company": "Merck",
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

company_name = 'Merck'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Merck',
                  'https://www.in.gr/wp-content/uploads/2021/03/merck-kgaa-vector-logo-150x83.png'
                  ))