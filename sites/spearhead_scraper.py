#
#  Company - > spearhead
# Link -> https://spearhead.systems/jobs
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import uuid
import requests
from bs4 import BeautifulSoup

def get_jobs():

    list_jobs = []

    response = requests.get('https://spearhead.systems/jobs',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')
    jobs = soup.find_all('a',class_='text-decoration-none')

    for job in jobs:

        link = 'https://spearhead.systems' + job.get('href')
        title = job.find('h3').text.strip()
        city = job.find('span',class_='w-100 o_force_ltr d-block').text.split()[-4]

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "Spearhead",
            "country": "Romania",
            "city": city
        })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Spearhead'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Spearhead',
                  'https://www.romanianstartups.com/wp-content/uploads/2013/09/spearhead-systems-logo-177x100.jpg'
                  ))