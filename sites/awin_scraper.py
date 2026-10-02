#
# Company - > Awin
# Link -> https://job-boards.greenhouse.io/awin
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city


def get_jobs():
    list_jobs = []

    req = requests.get("https://boards-api.greenhouse.io/v1/boards/awin/jobs",
                       headers=DEFAULT_HEADERS, params={"content": "true"})
    jobs = req.json()['jobs']

    for job in jobs:
        text = (job.get('location') or {}).get('name', '').strip()

        if 'Romania' not in text:
            continue

        link = job.get('absolute_url')
        title = job.get('title', '').strip()

        if 'Iasi' in text or 'Iași' in text:
            city = 'Iasi'
        elif 'Bucharest' in text:
            city = 'Bucuresti'
        else:
            city = ''
        
        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "Awin",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": 'on-site',
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Awin'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Awin',
                  'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Logo-awin-black.svg/177px-Logo-awin-black.svg.png'
                  ))