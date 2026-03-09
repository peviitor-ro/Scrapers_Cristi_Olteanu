#
# Company - > Lenovo
# Link -> https://jobs.lenovo.com/en_US/careers
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county


def get_jobs():
    list_jobs = []

    try:
        req = requests.get(
            'https://jobs.lenovo.com/en_US/careers/SearchJobs/?13036=%5B12016749%5D&13036_format=6621&listFilterMode=1&jobSort=relevancy&jobRecordsPerPage=10&jobOffset=0&sort=relevancy',
            headers=DEFAULT_HEADERS, 
            timeout=15)
        
        if req.status_code != 200 or len(req.text) == 0:
            return list_jobs
            
        soup = BeautifulSoup(req.text, 'lxml')
        jobs = soup.find_all('div', class_='article__header')

        if not jobs:
            return list_jobs

        for job in jobs:
            text_info = job.find('h3', class_="article__header__text__title article__header__text__title--4")
            if text_info is not None and text_info.text.strip() and 'No jobs found' not in text_info.text.strip():
                link = job.find('a')
                if link and link.get('href'):
                    link = link['href']
                    title = text_info.text.strip()

                    list_jobs.append({
                        "job_title": title,
                        "job_link": link,
                        "company": "Lenovo",
                        "country": "Romania",
                        "city": 'București',
                        "county": 'București',
                        "remote": 'on-site'
                    })
    except Exception as e:
        print(f"Error fetching Lenovo jobs: {e}")

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Lenovo'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Lenovo',
                  'https://static.lenovo.com/fea/images/lenovo-logo-red.png'
                  ))

