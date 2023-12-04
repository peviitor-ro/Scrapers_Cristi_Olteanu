#
#  Company - > MassMutual
# Link -> https://careers.massmutualromania.com/search-jobs
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get(
        'https://careers.massmutualromania.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=41&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=',
        headers=DEFAULT_HEADERS).json()['results']

    soup = BeautifulSoup(response, 'lxml')
    jobs = soup.find_all('li')

    for job in jobs:
        link = 'https://careers.massmutualromania.com' + job.find('a')['href']
        title = job.find('a').text
        city = job.find('span', class_='job-location').text.split(',')[0].strip()

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "MassMutual",
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

company_name = 'MassMutual'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('MassMutual',
'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/MassMutual_logo.svg/512px-MassMutual_logo.svg.png'
                  ))

