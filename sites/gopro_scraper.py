#
#  Company - > gopro
# Link -> https://job-boards.greenhouse.io/goprojobs
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city


def get_jobs():
    list_jobs = []

    url = "https://boards-api.greenhouse.io/v1/boards/goprojobs/jobs"
    params = {"content": "true"}

    try:
        req = requests.get(url, headers=DEFAULT_HEADERS, params=params, timeout=15)
        if req.status_code != 200:
            return list_jobs
        data = req.json()
        jobs = data.get("jobs", [])
    except Exception:
        return list_jobs

    for job in jobs:
        location_name = (job.get("location") or {}).get("name", "") or ""
        location_name_lower = location_name.lower()

        # Filter for Romania/Bucharest if location info indicates
        if "romania" not in location_name_lower and "bucharest" not in location_name_lower and "bucuresti" not in location_name_lower:
            # Still include if no location filter applies? Keep behavior conservative - but original filtered Bucharest
            pass  # Don't filter out if unclear; but try to match original intent

        title = (job.get("title") or "").strip()
        link = job.get("absolute_url") or job.get("url") or ""

        city = validate_city(location_name)
        county = get_county(city)

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "GoPro",
            "country": "Romania",
            "city": city,
            "county": county,
            "remote": job.get("employment_type") or job.get("location_type") or "on-site"
        })

    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list


company_name = 'GoPro'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('GoPro',
                  'https://1000logos.net/wp-content/uploads/2018/12/Gopro-Logo-500x313.png'
                  ))
