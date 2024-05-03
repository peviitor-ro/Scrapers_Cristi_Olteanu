#
# Company - > AstorMueller
# Link -> https://astormueller-ag.jobs.personio.com/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests


def get_jobs():

    jobs_list = []
    response = requests.get('https://astormueller-ag.jobs.personio.com/search.json',
                            headers=DEFAULT_HEADERS).json()
    for job in response:

        link = f"https://astormueller-ag.jobs.personio.com/job/{job['id']}?language=en&display=en"
        office_location = job['office']
        title = job['name']

        if 'remote' in office_location.lower():
            job_type = 'remote'
        else:
            job_type = 'on-site'

        if 'Romania' in office_location or "Oradea" in office_location:
            jobs_list.append({
                "job_title": title,
                "job_link": link,
                "company": "AstorMueller",
                "country": "Romania",
                "city": 'Oradea',
                "county": 'Bihor',
                "remote": job_type
            })

    return jobs_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'AstorMueller'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('AstorMueller',
                  'https://www.indiaretailing.com/wp-content/uploads/2017/07/astormueller-2.jpg'
                  ))


