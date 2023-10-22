#
#  Company - > justrocket
# Link -> https://join.com/companies/justrocket
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo
import requests
import uuid
from bs4 import BeautifulSoup

def get_jobs():

    list_jobs = []
    response = requests.get('https://join.com/companies/justrocket'
                            ,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')
    jobs = soup.find_all('a',class_='sc-eUXrtT cA-Dtdb JobTile___StyledJobLink-sc-989ef686-0 kYEttm JobTile___StyledJobLink-sc-989ef686-0 kYEttm')

    for job in jobs:

        location = job.find('div',class_='sc-hLseeU JobTile-elements___StyledText-sc-e7e7aa1d-4 fyJRsY kPLurW').text

        if 'hybrid' in location:
            type = 'hybrid'
        elif 'remote' in location:
            type = 'remote'
        else:
            type = 'on-site'

        link = job.get('href')
        city = job.find('div',class_='sc-hLseeU JobTile-elements___StyledText-sc-e7e7aa1d-4 fyJRsY kPLurW').text.split(',')[0]
        title = job.find('h3').text

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": title,
            "job_link": link,
            "company": "JUSTROCKET",
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


company_name = 'JUSTROCKET'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('JUSTROCKET',
                  'https://cdn.join.com/5f5f31e58d5d6100012b61c6/justrocket-logo-l.jpg'
                  ))