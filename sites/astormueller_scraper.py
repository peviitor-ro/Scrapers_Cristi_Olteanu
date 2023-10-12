#
# Company - > AstorMueller
# Link -> https://astormueller-ag.jobs.personio.com/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import uuid

def get_jobs():

    list_jobs = []
    response = requests.get('https://astormueller-ag.jobs.personio.com/search.json',
                            headers=DEFAULT_HEADERS).json()
    for job in response:
        link_ = job['id']
        link = f'https://astormueller-ag.jobs.personio.com/job/{link_}?language=en&display=en'

        try:
            country = job['office'].split()[1]
        except:
            country = 'none'

        title = job['name']
        city = job['office'].split()[0]

        if city == 'Oradea':
            country = 'Romania'
        else:
            pass

        if city == 'Remote':
            city = ''
            type = 'remote'
        else:
            type = 'on-site'

        if 'Romania' in country:
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "AstorMueller",
                "country": "Romania",
                "city": city,
                "remote": type
            })

    return list_jobs

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


