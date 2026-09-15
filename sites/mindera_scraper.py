#
#  Company - > mindera
# Link -> https://apply.workable.com/minderacraft/
#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
import re
from _county import get_county

session = requests.Session()

REMOTE_MAP = {
    "remote": "remote",
    "hybrid": "hybrid",
    "on_site": "on-site",
    "on-site": "on-site",
}


def get_remote_from_location(location):
    match = re.search(r"\((.+?)\)", location)
    if not match:
        return "on-site"
    workplace = match.group(1).strip().lower().replace(" ", "-")
    return REMOTE_MAP.get(workplace, workplace)


def get_jobs():

    list_jobs = []
    url = "https://apply.workable.com/minderacraft/jobs.md"

    params = {
        "location[0][country]": "Romania",
        "location[0][region]": "Cluj County",
        "location[0][city]": "Cluj-Napoca",
    }

    response = session.get(url, params=params, headers=DEFAULT_HEADERS)
    response.raise_for_status()

    for row in response.text.splitlines():
        if not row.startswith("|"):
            continue
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) < 7 or cells[0] in ("", "Title"):
            continue
        shortcode = re.search(r"/jobs/view/([A-Za-z0-9]+)\.md", cells[6])
        if not shortcode:
            continue

        title = cells[0]
        location = cells[2]
        city = location.split(",")[0].strip()
        link = f"https://apply.workable.com/minderacraft/j/{shortcode.group(1)}/"

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "mindera",
            "country": "Romania",
            "city": city,
            "county": get_county(city),
            "remote": get_remote_from_location(location)
        })
    return list_jobs


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list

company_name = 'mindera'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('mindera',
                  'https://www.cbpecapital.com/wp-content/uploads/mindera-logo-1@3x-480x295.png'
                  ))