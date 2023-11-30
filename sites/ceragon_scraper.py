#
# Company - > Ceragon
# Link -> https://www.ceragon.com/about-ceragon/careers
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():

    req = requests.get('https://www.ceragon.com/about-ceragon/careers',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text,'lxml')
    jobs = soup.find_all('div',class_='row')

    list_jobs=[]

    for job in jobs:

        link = 'https://www.ceragon.com' + job.find('a')['href']
        title = job.find('h5').text
        city = job.find('li',class_='hs-data-location').text.split()[-1]
        country = job.find('li',class_='hs-data-location').text.split()[0]

        if country == 'Romania':
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Ceragon",
                "country": "Romania",
                "city": city,
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list


company_name = 'Ceragon'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Ceragon',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Ceragon_logo.svg/180px-Ceragon_logo.svg.png'
                  ))

