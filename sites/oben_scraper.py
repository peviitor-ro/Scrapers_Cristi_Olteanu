#
# Company - > ObenTechnology
# Link -> https://www.careers-page.com/oben-technology?page=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

session = requests.Session()


def get_soup(url: str):

    response = session.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_pages():

    soup_pages = get_soup('https://www.careers-page.com/oben-technology?page=')
    num_jobs = int(soup_pages.find('h4', class_='positions').text.split()[0])
    num_pages = int(num_jobs/20)

    if num_jobs % 20 > 0:
        num_pages += 1

    return num_pages


def get_jobs():

    list_jobs = []

    for page in range(1, get_pages()+1, 1):

        soup_jobs = get_soup(f'https://www.careers-page.com/oben-technology?page={page}')
        jobs = soup_jobs.find_all('li', class_='media')

        for job in jobs:
            link_text = job.find('a', class_='text-secondary').get('href')

            if link_text is not None:
                title = str(job.find('h5')).split('\n')[1].strip()
                link = 'https://www.careers-page.com' + link_text
                try:
                    city = str(job.find('span')).split('i>')[1].split(',')[0]
                    job_type = 'on-site'
                except:
                    city = ''
                    job_type = 'remote'

                list_jobs.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "ObenTechnology",
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


company_name = 'ObenTechnology'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('ObenTechnology',
                  'https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/b81ef1de-4098-4e0a-af8c-b3c5858e412f_oben-logo-268x268.png'
                  ))











