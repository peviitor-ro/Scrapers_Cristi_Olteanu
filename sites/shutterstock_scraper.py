#
# Company - > shutterstock
# Link -> https://shutterstock.wd1.myworkdayjobs.com/ShutterstockCareers
#
from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
import requests

session = requests.Session()


def get_jobs():

    list_jobs = []

    session.get(
        'https://shutterstock.wd1.myworkdayjobs.com/en-US/ShutterstockCareers',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        },
        timeout=15
    )

    csrf_token = session.cookies.get('CALYPSO_CSRF_TOKEN', '')

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://shutterstock.wd1.myworkdayjobs.com',
        'Referer': 'https://shutterstock.wd1.myworkdayjobs.com/en-US/ShutterstockCareers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-CALYPSO-CSRF-TOKEN': csrf_token,
    }

    response = session.post(
        url='https://shutterstock.wd1.myworkdayjobs.com/wday/cxs/shutterstock/ShutterstockCareers/jobs',
        headers=headers,
        json={},
        timeout=15
    ).json()

    for job in response.get('jobPostings', []):
        title = job['title']
        locations_text = job['locationsText']
        external_path = job['externalPath']

        if 'Romania' in locations_text or 'RO' in locations_text.upper():
            city = locations_text.split(',')[0].strip()

            list_jobs.append({
                "job_title": title,
                "job_link": 'https://shutterstock.wd1.myworkdayjobs.com/en-US/ShutterstockCareers' + external_path,
                "company": "Shutterstock",
                "country": "Romania",
                "city": city,
                "remote": 'on-site'
            })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list


company_name = 'Shutterstock'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Shutterstock',
                  'https://logos-world.net/wp-content/uploads/2021/10/Shutterstock-Logo.png'
                  ))
