#
# Company - > iiPay
# Link -> https://www.iipay.com/careers/#section-positions
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get('https://www.iipay.com/careers/#section-positions', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('li', class_='c-job-list__item')

    for job in jobs:
        link = job.find('a')['href']
        title = job.find('div', class_='c-job-list__position').text.strip()
        job_type = job.find('div', class_='c-job-list__location').text.split(',')[0].strip()
        country = job.find('div', class_='c-job-list__location').text.split(',')[-1].strip()

        if job_type.lower() == 'remote' and country == 'Romania':
            city = 'Bucuresti'

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "iiPay",
                "country": "Romania",
                "city": city,
                "remote": job_type
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list

company_name = 'iiPay'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('iiPay',
                  'https://www.iipay.com/wp-content/themes/theme_iipay/images/iiPay-Logo-Final-No-Tagline.svg'
                  ))