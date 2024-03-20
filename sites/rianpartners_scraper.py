#
# Company - > rian-partners
# Link -> https://rian-partners.com/en/careers/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():
    list_jobs = []

    response = requests.get('https://rian-partners.com/en/careers/',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('tr')

    for job in jobs:
        title = job.findNext('td').text
        link = job.findNext('a')['href']
        city = job.findNext('td',class_='location').text.split(',')[0].split('/ ')

        for i in city:
            i.strip()
            if 'CLUJ' in i:
                city[city.index(i)] = 'CLuj-Napoca'
            elif 'CAMPULUNG MUSCEL' in i:
                city[city.index(i)] = 'CAMPULUNG'

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "rianpartners",
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


company_name = 'rianpartners'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('rianpartners',
                  'https://rian-partners.com/wp-content/uploads/2019/09/RIAN-partners-1.png'
                  ))

