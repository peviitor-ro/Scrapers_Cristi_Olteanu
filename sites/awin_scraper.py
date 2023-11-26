#
# Company - > Awin
# Link -> https://boards.greenhouse.io/awin
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests


def get_jobs():
    list_jobs = []

    req = requests.get("https://boards.greenhouse.io/awin", headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text, "lxml")

    jobs = soup.find_all('div', class_='opening')

    for job in jobs:
        city = job.find('span', class_='location').text.split(',')[0]
        link = 'https://boards.greenhouse.io' + job.find('a')['href']
        title = job.find('a').text
        location = job.find('span', class_='location').text

        if 'Romania' in location:
           list_jobs.append({
               "job_title": title,
               "job_link": link,
               "company": "Awin",
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


company_name = 'Awin'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Awin',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Logo-awin-black.svg/177px-Logo-awin-black.svg.png'
                  ))