#
# Company - > AMS
# Link -> https://www.careers-page.com/ams-hr#openings
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from _county import get_county
from _validate_city import validate_city


def get_jobs():

    list_jobs = []

    response = requests.get(
        "https://www.careers-page.com/api/v1.0/c/ams-hr/jobs/?page_size=100&page=1&city_new__in=172,382,349912,5182,2312,350638&organization__in=&ordering=-is_pinned_in_career_page,-last_published_at",
        headers=DEFAULT_HEADERS).json()['results']

    for job in response:

        title = job['position_name']
        city = validate_city(job['city'])
        link = 'https://www.careers-page.com/ams-hr/job/' + job['hash']

        if "remote" in title.lower():
            job_type = "remote"
        elif "hybrid" in title.lower():
            job_type = "hybrid"
        else:
            job_type = "on-site"

        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "AMS",
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

company_name = 'AMS'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('AMS',
                  'https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/554f1615-4c29-44ac-aa3e-63d1891bf70a_logo.png'
                  ))



