#
#  Company - > expressvpn
# Link -> https://jobs.deel.com/expresspn
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
import json
import re
from _county import get_county
from _validate_city import validate_city


def get_jobs():

    list_jobs = []

    response = requests.get('https://jobs.deel.com/expresspn',
                            headers=DEFAULT_HEADERS)

    if response.status_code != 200:
        return list_jobs

    chunks = re.findall(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)',
                        response.text)
    payload = ''
    for chunk in chunks:
        try:
            payload += json.loads(chunk)
        except json.JSONDecodeError:
            continue

    key = '"jobPostings":['
    start = payload.find(key)
    if start == -1:
        return list_jobs

    start += len(key) - 1
    depth = 0
    end = None
    for i in range(start, len(payload)):
        if payload[i] == '[':
            depth += 1
        elif payload[i] == ']':
            depth -= 1
            if depth == 0:
                end = i
                break
    if end is None:
        return list_jobs

    try:
        postings = json.loads(payload[start:end + 1])
    except json.JSONDecodeError:
        return list_jobs

    country_by_city = {
        'Tel Aviv': 'Israel',
        'Singapore': 'Singapore',
    }

    for posting in postings:
        job = posting.get('job') or {}
        arrangement = job.get('workArrangementEnum') or ''

        if arrangement == 'REMOTE':
            job_type = 'remote'
        elif arrangement == 'HYBRID':
            job_type = 'hybrid'
        else:
            job_type = 'on-site'

        cities = []
        for item in job.get('jobLocations') or []:
            city = (item.get('location') or {}).get('name')
            if city and city not in cities:
                cities.append(city)

        job_link = ('https://jobs.deel.com/expresspn/job-details/'
                    + str(posting.get('id')) + '/overview')

        if not cities:
            cities = ['']

        for city in cities:
            city = validate_city(city)

            list_jobs.append({
                "job_title": posting.get('title'),
                "job_link": job_link,
                "company": "expressvpn",
                "country": country_by_city.get(city, city),
                "city": city,
                "county": get_county(city),
                "remote": job_type
            })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'expressvpn'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('expressvpn',
                  'https://upload.wikimedia.org/wikipedia/en/thumb/7/79/ExpressVPN-logo.svg/261px-ExpressVPN-logo.svg.png?20210118095637'
                  ))
