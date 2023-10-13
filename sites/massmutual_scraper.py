#
#  Company - > MassMutual
# Link -> https://careers.massmutualromania.com/search-jobs
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
import uuid

def get_jobs():

    list_jobs= []

    response = requests.get('https://careers.massmutualromania.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=46&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=0&SortDirection=0&SearchType=5&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf=',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text,'lxml')

    jobs = soup.find_all('li')

    for job in jobs:
        text = job.find('h2',attrs={})
        if text != None:
            title = text.text
            link = 'https://careers.massmutualromania.com/' + job.findNext('a')['href'].split('\"/')[1].strip('\\"')
            city = job.findNext('span').text.split(',')[0]

            list_jobs.append({
                "id": str(uuid.uuid4()),
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
                  'https://banner2.cleanpng.com/20180426/ekw/kisspng-massachusetts-mutual-life-insurance-company-massmu-5ae196127600b5.6295915315247334584834.jpg'
                  ))

