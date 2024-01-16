#
# Company - > humanrise
# Link -> https://humanrise.ro/joburi/
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup


def get_jobs():

    job_list = []

    response = requests.get('https://humanrise.ro/joburi/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('div', class_="grid-item-cont")

    for job in jobs:
        title = job.find('h3', class_="entry-title de_title_module dmach-post-title").text
        link = job.find('a', class_="et_pb_button")['href']
        city = job.find_all('p', class_="dmach-acf-value")
        for c in city:
            if "Locations:" in c.text:
                cities = c.text.split("Locations:")[1].strip().split(', ')
        if "Remote" in cities:
            job_type = "remote"
            cities.remove("Remote")
        else:
            job_type = "on-site"

        job_list.append({
            "job_title": title,
            "job_link": link,
            "company": "expressvpn",
            "country": "Romania",
            "city": city,
            "remote": job_type})
    return job_list


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Humanrise'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Humanrise',
                  'https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/4a183d6c-e742-4b7a-9b2e-3575c6c7ee28_Human%20Rise%20logo%20compact_enclosed.png'
                  ))
