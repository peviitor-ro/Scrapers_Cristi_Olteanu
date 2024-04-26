#
# Company - > Akwel
# Link -> https://careers.lectra.com/search/?q=&q2=&alertId=&title=&location=RO&date=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get('https://akwel-automotive.com/en/careers/job-opportunities/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('div', class_='job-offer-list-item')

    for job in jobs:

        link = job.find('a', class_='btn btn-block btn-sm btn-outline-secondary-reverse')['href']
        title = job.find('div', class_='job-offer-list-item__title').text
        city = job.find('div', class_='value').text.split(',')[0]
        country = job.find('div', class_='value').text.split(',')[-1].strip()
        if country == 'Roumania' or country == 'Romania':
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Akwel",
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


company_name = 'Akwel'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Akwel',
                  'https://upload.wikimedia.org/wikipedia/fr/thumb/4/44/Logo_Akwel.svg/600px-Logo_Akwel.svg.png?20180723184252'
                  ))