#
# Company - > Garrett
# Link -> https://ehth.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_2001/requisitions?location=Romania&locationId=300000000275207&locationLevel=country&mode=location
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests


def make_request(url):

    ses = requests.session()
    response = ses.get(url, headers=DEFAULT_HEADERS).json()['items']
    return response


def get_num_jobs():

    res = make_request(url='https://ehth.fa.em2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_2001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,locationId=300000000275207,sortBy=POSTING_DATES_DESC,offset=')
    num_jobs = int(res[0]['TotalJobsCount'])
    return num_jobs


def get_jobs():

    list_jobs = []

    for page in range(0, get_num_jobs(), 25):

        r = make_request(f'https://ehth.fa.em2.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_2001,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,locationId=300000000275207,sortBy=POSTING_DATES_DESC,offset={page}')[0]['requisitionList']

        for job in r:
            id = job['Id']
            title = job['Title']
            link = f'https://ehth.fa.em2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_2001/job/{id}/?location=Romania&locationId=300000000275207&locationLevel=country&mode=location'
            city = job['PrimaryLocation'].split(',')[0]

            if city == 'Romania' or city == 'BUCUREŞTI':
                city = 'Bucuresti'
            else:
                pass

            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "Garrett",
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


company_name = 'Garrett'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Garrett',
                  'https://upload.wikimedia.org/wikipedia/commons/5/51/Garrett_-_Advancing_Motion_Logo.png'
                  ))

