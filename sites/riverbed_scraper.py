#
# Company - > Riverbed
# Link -> https://careers.riverbed.com/jobs?stretchUnits=MILES&stretch=10&location=Romania&lat=46&lng=25&woe=12
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
import uuid

def get_jobs():
    """
           ... this func() make a simple requests
           and collect data from Riverbed API.
        """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    response = requests.get('https://careers.riverbed.com/api/jobs?stretchUnits=MILES&stretch=10&location=Romania&lat=46&lng=25&woe=12&page=1&sortBy=relevance&descending=false&internal=false',headers=headers).json()['jobs']

    list_jobs = []

    for job in response:
        country_location = job['data']['country']
        location = job['data']['city']

        if location == 'Home Office':
            city = country_location
            remote = 'remote'
        else:
            city = location
            remote = 'on-site'


        if country_location == 'Romania':
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": job['data']['title'],
                "job_link": job['data']['meta_data']['canonical_url'],
                "company": "Riverbed",
                "country": "Romania",
                "city": city,
                "remote": remote
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Riverbed'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Riverbed',
                  'https://cms.jibecdn.com/prod/riverbed/assets/HEADER-LOGO_IMG-en-us-1649182997894.png'
                  ))

