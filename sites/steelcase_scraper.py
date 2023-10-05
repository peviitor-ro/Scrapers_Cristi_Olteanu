#
# Company - > Steelcase
# Link ->https://careers.steelcase.com/external/SearchJobs/?3_142_3=38706&folderOffset=0
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid


def get_soup(url: str):

    res = requests.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(res.text,'lxml')
    return soup

def get_nr_jobs():

    soup_iter = get_soup(url='https://careers.steelcase.com/external/SearchJobs/?3_142_3=38706&folderOffset=0')
    nr_jobs= int(soup_iter.find('span',class_='pagination__legend').text.split()[2])
    return nr_jobs

def get_jobs():
    list_jobs = []

    for page in range(0,get_nr_jobs(),5):

        soup_jobs = get_soup(url='https://careers.steelcase.com/external/SearchJobs/?3_142_3=38706&folderOffset=0'+str(page))
        jobs = soup_jobs.find_all('div',class_='list__item__text')

        for job in jobs:
            title = job.find('a').text
            link = job.find('a')['href']
            city = job.find('div',class_='list__item__text__subtitle').text.split('City:')[-1].split('.')[0]

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Steelcase",
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


company_name = 'Steelcase'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Steelcase',
                  'https://dumy1g3ng547g.cloudfront.net/content/themes/steelcase/img/logo.svg'
                  ))