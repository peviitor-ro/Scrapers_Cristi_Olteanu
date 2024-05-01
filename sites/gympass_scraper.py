
#
#  Company - > Gympass
# Link -> https://boards.greenhouse.io/gympass
#
import requests
from bs4 import BeautifulSoup
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS,update_peviitor_api
from L_00_logo import update_logo


def get_jobs():

    list_jobs = []

    response = requests.get('https://boards.greenhouse.io/gympass', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('div', class_='opening')

    for job in jobs:
        link = 'https://boards.greenhouse.io/' + job.find('a')['href']
        title = job.find('a').text
        location = job.find('span', class_='location').text

        if 'Remote' in location:
            type = 'remote'
        elif 'Hybrid' in location:
            type = 'hybrid'
        else:
            type = 'on-site'

        if 'Romania' in location:
            city = job.find('span', class_='location').text.split()[1].strip('(')
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Gympass",
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


company_name = 'Gympass'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Gympass',
                  'https://s2-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/188/200/resized/Gympass_cover.png?1607553944'
                  ))