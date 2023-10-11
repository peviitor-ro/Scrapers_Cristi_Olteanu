#
# Company - > TokenMetrics
# Link -> https://jobs.lever.co/tokenmetrics?location=Bucharest
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid

def get_jobs():

    req = requests.get('https://jobs.lever.co/tokenmetrics?location=Bucharest',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text,'lxml')
    jobs = soup.find_all('div',class_='posting')

    list_jobs=[]

    for job in jobs:

        link = job.find('a',class_='posting-title')['href']
        title = job.find('h5').text
        city = job.find('span',class_='sort-by-location posting-category small-category-label location').text
        type = job.find('span',class_='display-inline-block small-category-label workplaceTypes').text

        list_jobs.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "TokenMetrics",
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


company_name = 'TokenMetrics'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('TokenMetrics',
                  'https://global-uploads.webflow.com/634054bf0f60201ce9b30604/634503713190a76b2bdd040b_TM%20Logo.svg'
                  ))
