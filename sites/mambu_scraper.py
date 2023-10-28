#
# Company - > mambu
# Link -> https://careers-mambu.icims.com/jobs/search?ss=1&searchLocation=13526--
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import uuid
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    querystring = {"ss": "1", "searchLocation": "13526--", "in_iframe": "1"}

    response = requests.get('https://careers-mambu.icims.com/jobs/search#iCIMS_Header',
                            headers=DEFAULT_HEADERS,
                            params=querystring)

    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='row')

    for job in jobs:
        text = job.find('a', class_='iCIMS_Anchor')

        if text is not None:
            title = text['title'].split('-')[-1].strip()
            link = text['href']
            city = job.find('div', class_='col-xs-6 header left').text.split()[-1].split('-')[-1]

            if city == 'Remote':
                city = 'Iasi'
                job_type = 'remote'
            else:
                job_type = 'on-site'

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "mambu",
                "country": "Romania",
                "city": city,
                "remote": job_type
            })

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'mambu'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('mambu',
                  'https://c-12720-20230802-mambu-com.i.icims.com/images/logo/mambu-logo-2023.svg'
                  ))