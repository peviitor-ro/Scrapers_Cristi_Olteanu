#
# Company - > opentext
# Link    - > https://careers.opentext.com/search/?q=&location=RO&sortColumn=referencedate&sortDirection=desc&startrow=
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county



def get_soup(url):

    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_num_pages():

    soup_pages = get_soup('https://careers.opentext.com/search/?q=&location=RO&sortColumn=referencedate&sortDirection=desc&startrow=')
    try:
        num_pages = soup_pages.find('span', class_='srHelp').text.split('of')[-1].strip()
    except:
        num_pages = 0
    return int(num_pages)


def get_jobs():

    jobs_list = []

    for page in range(0, get_num_pages()*25, 25):
        if page == 0:
            page = ''
        else:
            pass

        soup_jobs = get_soup(f'https://careers.opentext.com/search/?createNewAlert=false&q=&locationsearch=RO&optionsFacetsDD_department=&optionsFacetsDD_location={page}')
        jobs = soup_jobs.find_all('tr', class_='data-row')

        for job in jobs:
            link = 'https://careers.opentext.com'+job.find('a', class_='jobTitle-link')['href']
            title = job.find('a', class_='jobTitle-link').text
            city = job.find('span', class_='jobLocation').text.split(', ')[-2].strip()
            country = job.find('span', class_='jobLocation').text.split(', ')[-1].split()[0]

            if country != 'RO':
                cities = get_soup(link).find_all('span', class_='jobGeoLocation')
                for item in cities:
                    if 'RO' in item.text:
                        city = item.text.split(',')[0].strip('\n')

            if 'Virtual' in city:
                city = 'Bucuresti'
                job_type = 'remote'
            else:
                job_type = 'on-site'

            jobs_list.append({
                "job_title": title,
                "job_link": link,
                "company": "opentext",
                "country": "Romania",
                "city": city,
                "county": get_county(city),
                "remote": job_type
                })

    return jobs_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'opentext'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('opentext',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/OpenText_logo.svg/447px-OpenText_logo.svg.png'
                  ))