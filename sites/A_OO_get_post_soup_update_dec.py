#
#
#
# This Decorator will avoid duplicate for me!
# Respect DRY
# This decorator have: default headers and soup and update data on peviitor.ro!
#
import requests
#
import os  # I do not have API KEY
#
import json
import time


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Refer': 'https://google.com',
    'DNT': '1'
}


########### UPDATE API DECORATOR ############
def update_peviitor_api(original_function):
    """
    Decorator for update data on Peviitor.ro API
    """

    def new_function(*args, **kwargs):
        company_name, data_list = args
        #
        API_KEY = os.environ.get('API_KEY')
        CLEAN_URL = 'https://api.peviitor.ro/v4/clean/'

        clean_header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'apikey': API_KEY
            }

        #clean_request = requests.post(CLEAN_URL, headers=clean_header, data={'company': company_name})

        time.sleep(0.2)
        token = get_token()
        post_header = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
            }
        validator_endpoint = 'https://api.laurentiumarian.ro/jobs/add/'

        res = requests.post(validator_endpoint, json=data_list, headers=post_header)
        #post_request_to_server = requests.post('https://api.peviitor.ro/v4/update/', headers=post_header, data=json.dumps(data_list))
        print(json.dumps(data_list, indent=4))

        return original_function(*args, **kwargs)

    return new_function


def get_token():
    #token_endpoint = 'https://api.peviitor.ro/v5/get_token/'
    token_endpoint = 'https://api.laurentiumarian.ro/get_token'

    token = requests.post(token_endpoint, json={
        "email": "cristiolteanu1892@gmail.com"
    }, headers = {
    "Content-Type": "application/json",
})

    return token.json()['access']
