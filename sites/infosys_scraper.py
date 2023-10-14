#
#  Company - > Infosys
# Link -> https://digitalcareers.infosys.com/infosys/global-careers?page=2&per_page=25&job_type=experienced&location=Romania
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_soup(url: str):

    ses = requests.Session()
    response = ses.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')

    return soup

def get_pages():

    soup_pages = get_soup('https://digitalcareers.infosys.com/infosys/global-careers?page=0&per_page=25&job_type=experienced&location=Romania')
    num_jobs = int(soup_pages.find('div',class_='sumarry').text.split('of')[-1].split()[0])
    pages = int(num_jobs/25)

    if num_jobs%25>0:
        pages += 1
    else:
        pass

    return pages


def get_jobs():

    list_jobs = []

    for page in range(1,get_pages()+1,1):
        soup_jobs = get_soup(url=f'https://digitalcareers.infosys.com/infosys/global-careers?page={page}&per_page=25&job_type=experienced&location=Romania')
        jobs = soup_jobs.find_all('a',class_='job editable-cursor')

        for job in jobs:
            link = job.get('href')
            title = job.find('div', class_='job-title').text.strip()
            city = job.find('div', class_='job-location js-job-city').text.split('-')[0].split()[0].strip(',')

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Infosys",
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

company_name = 'Infosys'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Infosys',
                  'https://w7.pngwing.com/pngs/563/912/png-transparent-infosys-technologies-hd-logo-thumbnail.png'
                  ))


