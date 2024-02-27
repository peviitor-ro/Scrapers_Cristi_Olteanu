#
# Company - > FlTechincs
# Link -> https://fltechnics.com/careers/?c-ctry=29#career-list
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup



def get_soup(url: str):
    session = requests.Session()
    response = session.get(url,headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_pages():
    soup_pages = get_soup(url='https://fltechnics.com/careers/?c-ctry=29&c-search=#career-list')
    nr_jobs = int(soup_pages.find('div', class_='vc_col-md-12 vc_col-sm-12 vc_col-xs-12 wpb_column column_container vc_column_container col child_column no-extra-padding inherit_tablet inherit_phone'
                                  ).text.split()[0])
    nr_pages = int(nr_jobs / 10)
    if int(int(nr_jobs % 10) > 0):
        nr_pages += 1
    return nr_pages


def get_jobs():

    list_jobs = []

    for page in range(1, get_pages() + 1, 1):

        soup = get_soup(url=f'https://fltechnics.com/careers/?p-page={page}&c-ctry=29&c-search#career-list')
        jobs = soup.find_all('div', class_='row_col_wrap_12 col span_12 dark left career')

        for job in jobs:

            link = job.find('a')['href']
            title = job.find('a')['title']
            location = job.find('div', class_='asgc-list-col col-location').text.strip().split(', ')[1]
            city = job.find('div', class_='asgc-list-col col-location').text.strip().split(', ')[0]

            if location == 'Romania':
                list_jobs.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "FlTechnics",
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


company_name = 'FlTechnics'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('FlTechnics',
                  'https://fltechnics.com/wp-content/uploads/2021/07/flt-logo-org.svg'
                  ))


