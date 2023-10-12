#
# Company - > Visa
# Link -> https://usa.visa.com/en_us/jobs/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests
import uuid

def get_jobs():

    list_jobs = []
    session = requests.session()
    url = 'https://search.visa.com/CAREERS/careers/jobs?q='

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'Origin': 'https://usa.visa.com',
        'Referer': 'https://usa.visa.com/',
        'Sec-Ch-Ua': 'Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }
    data = {"city":["Bucharest"],"from":0,"size":10}

    response = session.post(url=url, headers=headers, json=data).json()['jobDetails']

    for job in response:

        region = job['region']

        if 'Bucharest' or 'Romania' in region.lower():
            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": job['jobTitle'],
                "job_link": 'https://usa.visa.com/en_us/jobs/' + job['refNumber'],
                "company": "Visa",
                "country": "Romania",
                "city": job['city']
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Visa'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Visa',
                  'https://cdn.visa.com/v2/assets/images/logos/visa/blue/logo.png'
                  ))