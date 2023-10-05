#
# Company - > TalentKompass
# Link ->https://jobs.lever.co/talentkompass-deutschland/?
#
from A_OO_get_post_soup_update_dec import update_peviitor_api,DEFAULT_HEADERS
from L_00_logo import update_logo
from bs4 import BeautifulSoup
import requests
import uuid

def get_jobs():

    req = requests.get('https://jobs.lever.co/talentkompass-deutschland/?',headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(req.text,'lxml')
    jobs = soup.find_all('div',class_='posting')

    list_jobs=[]

    for job in jobs:
        link = job.find('a',class_='posting-title')['href']
        title = job.find('a',class_='posting-title').find('h5').text
        city = job.find('span',class_='sort-by-location posting-category small-category-label location').text.split(', ')[0]
        location = job.find('span',class_='sort-by-location posting-category small-category-label location').text.split(', ')[1]
        remote = job.find('span',class_='display-inline-block small-category-label workplaceTypes').text

        if location == 'Romania':

            list_jobs.append({
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "TalentKompass",
                "country": "Romania",
                "city": city,
                "remote": remote
            })
    return list_jobs

@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'TalentKompass'  # add test comment
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('TalentKompass',
                  'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiDUm17RBdaE_fX5AKUhprKteU5iVpOfWutd4lYBosA7KMtQhgT7bQ3YPlOuWt9iO9DlpeNeAWRwj--YaDycElUXCvWiaQRNBlnj6GugU3GLsgmrFM24n4vBo-evNUIImgDJeVbdAv-uWxi4GZnRiVZY4EHZ1mTiEduGq_HdYKSaMcQjvFFSWowqaYzWQ/w640-h402/download%20(2).jpg=.jpg'
                  ))

