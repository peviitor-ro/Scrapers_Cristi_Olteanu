#
# Company - > Stericycle
# Link -> https://careers.stericycle.com/search/?q=&locationsearch=Romania&searchby=location&d=10&startrow=10
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid


def get_soup(url: str):

    res = requests.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(res.text,'lxml')
    return soup

def get_nr_pages():

    soup_pages = get_soup('https://careers.stericycle.com/search/?q=&locationsearch=Romania&searchby=location&d=10&startrow=')
    nr_pages = int(soup_pages.find('span',class_='paginationLabel').text.split()[-1])
    return nr_pages


def get_jobs():
    list_jobs = []

    for page in range(0,get_nr_pages(),10):

        soup_jobs = get_soup('https://careers.stericycle.com/search/?q=&locationsearch=Romania&searchby=location&d=10&startrow='+str(page))
        jobs = soup_jobs.find_all('tr', class_='data-row')

        for job in jobs:

            title = job.find('a',class_='jobTitle-link').text
            link = 'https://careers.stericycle.com/' + job.find('a',class_='jobTitle-link')['href']
            city = job.find('span',class_='jobLocation').text.split(',')[0].strip()

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Stericycle",
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


company_name = 'Stericycle'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Stericycle',
                  'https://ww2.freelogovectors.net/wp-content/uploads/2022/08/stericycle-logo-freelogovectors.net_-400x76.png?lossy=1&ssl=1&fit=400%2C76'
                  ))