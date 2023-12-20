#
# Company - > AMS
# Link -> https://www.careers-page.com/ams-hr#openings
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests


def get_jobs():

    list_jobs = []

    response = requests.get(
        "https://www.careers-page.com/api/v1.0/c/ams-hr/jobs/?page_size=50&page=1&city_new__in=172,1254,2097,44432,5105,2312&organization__in=&ordering=-is_pinned_in_career_page,-last_published_at",
        headers=DEFAULT_HEADERS).json()['results']

    for job in response:

        title = job['position_name']
        city = job['city']
        country = job['country']
        link = 'https://www.careers-page.com/ams-hr/job/' + job['hash']

        if 'Romania' in country:
            list_jobs.append({
                "job_title": title,
                "job_link": link,
                "company": "AMS",
                "country": "Romania",
                "city": city
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



