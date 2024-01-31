#
# Company - > siena
# Link -> https://jobs.ashbyhq.com/siena
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests

session = requests.Session()


def prepare_post():

    url = "https://jobs.ashbyhq.com/api/non-user-graphql"

    querystring = {"op": "ApiJobBoardWithTeams"}

    payload = {
        "operationName": "ApiJobBoardWithTeams",
        "variables": {"organizationHostedJobsPageName": "siena"},
        "query": "query ApiJobBoardWithTeams($organizationHostedJobsPageName: String!) "
                 "{\n  jobBoard: jobBoardWithTeams"
                 "(\n    organizationHostedJobsPageName: $organizationHostedJobsPageName\n  )"
                 " {\n    teams {\n      id\n      name\n      parentTeamId\n      __typename\n    }"
                 "\n    jobPostings "
                 "{\n      id\n      title\n      teamId\n      "
                 "locationId\n      locationName\n      employmentType\n      secondaryLocations "
                 "{\n        ...JobPostingSecondaryLocationParts\n        __typename\n      }"
                 "\n      compensationTierSummary\n      __typename\n    }"
                 "\n    __typename\n  }\n}\n\nfragment JobPostingSecondaryLocationParts on JobPostingSecondaryLocation "
                 "{\n  locationId\n  locationName\n  __typename\n}"}

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
        "Origin": "https://jobs.ashbyhq.com",
        "Referer": "https://jobs.ashbyhq.com/siena?utm_source=zLmkeq71qy"
    }

    return url, payload, headers, querystring


def get_jobs():

    list_jobs = []
    data = prepare_post()
    response = session.request("POST", data[0], json=data[1], headers=data[2], params=data[3]
                               ).json()['data']['jobBoard']['jobPostings']

    for job in response:

        locations = job['secondaryLocations']
        cities = []
        title = job['title']
        link = f"https://jobs.ashbyhq.com/siena/{job['id']}?utm_source=zLmkeq71qy"
        first_city = job['locationName']

        if 'remote' in title.lower():
            job_type = 'remote'
        elif 'hybrid' in title.lower():
            job_type = 'hibrid'
        else:
            job_type = 'on-site'

        for location in locations:
            secondary_location = location['locationName']

            if 'Cluj' in secondary_location:
                cities.append('Cluj-Napoca')
            if 'Bucharest' in secondary_location:
                cities.append('Bucharest')
            if 'Iasi' in secondary_location:
                cities.append('Iasi')

        if first_city in ['Bucharest', 'Cluj', 'Iasi']:
            cities.append(first_city)

        if cities:
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "siena",
                "country": "Romania",
                "city": cities,
                "remote": job_type
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'siena'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('siena',
                  'https://app.ashbyhq.com/api/images/org-theme-wordmark/2dbfc236-5c7c-4a85-95e0-942e757542ee/0e3c3c2a-e957-422a-96eb-661e8d2d50ba.png'
                  ))








