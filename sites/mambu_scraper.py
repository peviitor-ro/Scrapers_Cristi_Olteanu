#
# Company - > mambu
# Link -> https://careers-mambu.icims.com/jobs/search?ss=1&searchLocation=13526--
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from _county import get_county


def get_jobs():

    list_jobs = []

    querystring = {"ss": "1", "in_iframe": "1"}
    response = requests.get('https://careers-mambu.icims.com/jobs/search',
                            headers=DEFAULT_HEADERS,
                            params=querystring)

    soup = BeautifulSoup(response.text, 'lxml')
    jobs = soup.find_all('li', class_='iCIMS_JobCardItem')

    for job in jobs:
        title_elem = job.find(class_='iCIMS_JobTitle')
        if not title_elem:
            continue
        title_link = title_elem.find('a')
        if not title_link:
            continue
        title = title_link.text.strip()
        link = title_link.get('href')

        # Extract location
        city = 'Bucuresti'
        job_type = 'on-site'
        text = job.get_text()
        if 'Job Locations' in text:
            loc_section = text.split('Job Locations')[-1]
            # Get first meaningful location
            import re
            # Look for country/city patterns
            if 'RO-' in loc_section or 'Romania' in loc_section:
                if 'RO-Iasi' in loc_section or 'Iasi' in loc_section:
                    city = 'Iasi'
                elif 'RO-Bucharest' in loc_section or 'Bucharest' in loc_section or 'Bucuresti' in loc_section:
                    city = 'Bucuresti'
                elif 'RO-Remote' in loc_section or 'Remote' in loc_section and 'Romania' in loc_section:
                    job_type = 'remote'
                    # Try to assign a default city if not specified
                    city = 'Bucuresti'
            elif 'Remote' in loc_section:
                job_type = 'remote'
            elif 'JP' in loc_section or 'Japan' in loc_section:
                continue  # Skip non-Romania jobs if any
            else:
                # Try to extract city name
                m = re.findall(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)', loc_section)
                if m:
                    for candidate in m:
                        if candidate not in ['Job', 'Title', 'ID', 'Senior', 'Account']:
                            city = candidate
                            break

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "mambu",
            "country": "Romania",
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


company_name = 'mambu'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('mambu',
                  'https://c-12720-20230802-mambu-com.i.icims.com/images/logo/mambu-logo-2023.svg'
                  ))
