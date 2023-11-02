#
# Company - > temps
# Link -> https://www.careers-page.com/temps-hr-2
#
from A_OO_get_post_soup_update_dec import update_peviitor_api, DEFAULT_HEADERS
from L_00_logo import update_logo
import uuid
import requests
from bs4 import BeautifulSoup


def get_jobs():

    list_jobs = []

    response = requests.get('https://www.careers-page.com/temps-hr-2', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('li', class_='media')

    for job in jobs:
        link_text = job.find('a', class_='text-secondary').get('href')

        if link_text is not None:
            link = 'https://www.careers-page.com' + link_text
            title = str(job.find('h5')).split('\n')[1].strip()
            city = str(job.find('span', attrs={'style': 'margin-right: 10px;'})).split('i>')[1].split(',')[0].strip()

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "temps",
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


company_name = 'temps'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('temps',
                  'https://manatal-backend-public-assets.s3.amazonaws.com/media/career_portal_logo_direct_upload/e74c9c7b-01ee-4899-a1b9-684ba18c7a0e_Temps%20-%20logo%20-%20final.png'
                  ))

