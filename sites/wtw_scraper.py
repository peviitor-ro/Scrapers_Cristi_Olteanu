#
# Company - > wtw
# Link - https://eedu.fa.em3.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1003/requisitions?lastSelectedFacet=LOCATIONS&location=Romania&locationId=300000000346767&locationLevel=country&mode=location&selectedLocationsFacet=300000000346767
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
import uuid


def get_jobs():

    list_jobs = []

    response = requests.get('https://eedu.fa.em3.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX_1003,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,lastSelectedFacet=LOCATIONS,selectedLocationsFacet=300000000346767,sortBy=POSTING_DATES_DESC',
                            headers=DEFAULT_HEADERS).json()['items'][0]['requisitionList']

    for job in response:

        list_jobs.append({
            "id": str(uuid.uuid4()),
            "job_title": job['Title'],
            "job_link": f"https://eedu.fa.em3.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1003/job/{job['Id']}/?lastSelectedFacet=LOCATIONS&selectedLocationsFacet=300000000346767",
            "company": "wtw",
            "country": "Romania",
            "city": job['PrimaryLocation'].split(',')[0],
        })

    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'wtw'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('wtw',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Logo_WTW.png/800px-Logo_WTW.png?20220722085247'
                  ))

