#
# Company - > humanrise
# Link -> https://www.careers-page.com/humanrise
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_soup(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_pages():

    soup_pages = get_soup(url='https://www.careers-page.com/humanrise?page=')
    nr_jobs = int(soup_pages.find('h4', class_='positions').text.split()[0])
    pages = int(nr_jobs/10)
    if nr_jobs % 10 > 0:
        pages += 1
    return pages


def get_jobs():

    list_jobs = []

    for page in range(1, get_pages()+1, 1):

        soup_jobs = get_soup(f'https://www.careers-page.com/humanrise?page={page}')
        jobs = soup_jobs.find_all('div', class_='media-body')

        for job in jobs:
            text = job.find('a', class_='text-secondary').get('href')

            if text is not None:
                title = str(job.find('h5')).split('>')[1].strip('</h5').strip().replace('&amp;', '&')
                link = 'https://www.careers-page.com' + text
                try:
                    city = str(job.find('span')).split('</span')[0].split('i>')[1].split(',')[0].strip()
                except:
                    city = 'Iasi'

                list_jobs.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "Humanrise",
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


company_name = 'Humanrise'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Humanrise',
                  'https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/4a183d6c-e742-4b7a-9b2e-3575c6c7ee28_Human%20Rise%20logo%20compact_enclosed.png'
                  ))
