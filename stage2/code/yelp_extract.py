#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
import json
import pprint
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

API_KEY = ""


# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Search term
TERM = 'restaurants'
SORT_BY = 'review_count'
SEARCH_LIMIT = 50
ZIPS = [90005, 90006, 90007, 90008, 90009, 90010, 90011, 90012, 90013, 90014, 90015, 90016, 90017, 90018, 90019,
            90020, 90021, 90022, 90023, 90024, 90025, 90026, 90027, 90028, 90029, 90030,
            90034, 90035, 90036, 90037, 90038, 90039, 90040, 90041, 90042, 90043, 90044, 90045, 90046, 90047, 90048, 90049,
            90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90064, 90065, 90066, 90067, 90068, 90069,
            90210, 90211, 90222, 90223, 90224, 90225, 90226, 90227, 90228, 90229, 90230, 90231, 90232,
            90240, 90241, 90242, 90290, 90291, 90292, 90400, 90401, 90402, 90403, 90404, 90405, 90406,
            91103, 91104, 91105, 91204, 91205, 91206, 91210, 91505, 91604, 91605, 91606, 91607, 91800, 91801, 91802, 91803]


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def get_result():
    
    data = []
    total_count = 0;
    for z in ZIPS:
    #for z in range(90070, 90210):
        url_params = {'term' : TERM,
                      'location' : z,
                      'limit': SEARCH_LIMIT,
                      'sort_by': SORT_BY }
    
       
        response = request(API_HOST, SEARCH_PATH, API_KEY, url_params)
        businesses = response.get('businesses')

        if not businesses:
            print(u'No businesses for {0} in zip ({1}) found.'.format(url_params.get('term'), z))
            continue

        #business_id = businesses[0]['id']
        print('{0} businesses found, querying business info for the top result in zip ({1}) ...'.format(len(businesses), z))
        
        total_count += len(businesses)
        for b in range(0, len(businesses)):
            response = get_business(API_KEY, businesses[b]['id'])
            data.append(response)
            
    file = open('yelp_2.json','w')
    json.dump(data,file,indent=4, sort_keys=True)
    file.close()
    print ('Work done. Total get %d restaurants info' % total_count)
            

def main():
    
    try:
        get_result()
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
