#
# Company - > Cmed
# Link -> https://aixialgroup.hire.trakstar.com/#content
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid

def get_jobs():

    req = requests.get('https://aixialgroup.hire.trakstar.com/#content',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text,'lxml')
    jobs = soup.find_all('div',class_='js-card list-item list-item-clickable js-careers-page-job-list-item')

    list_jobs=[]

    for job in jobs:
        ty = job.find('div',class_='rb-text-4 js-job-list-opening-meta').text.split('|')[-1].strip()

        if ty == 'Partially remote':
            type = 'hybrid'
        elif ty == 'Fully remote':
            type = 'remote'
        else:
            type = 'on-site'

        link = 'https://aixialgroup.hire.trakstar.com' + job.find('a')['href']
        title = job.find('h3').text.strip()
        country = job.find('div',class_='rb-text-6 js-job-list-opening-loc cut-text').text.split(',')[-1].strip()
        city = job.find('div',class_='rb-text-6 js-job-list-opening-loc cut-text').text.split(',')[0].strip()

        if 'Romania' in country:

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Cmed",
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


company_name = 'Cmed'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Cmed',
                  'https://tukuz.com/wp-content/uploads/2019/11/cmed-logo-vector.png'
                  ))