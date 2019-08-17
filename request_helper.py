import requests


def get_request(url):
    """ Makes the request to SWAPI with given URL.
    Returns JSON from the results.
    """
    result_json = requests.get(url).json()
    return result_json

def detect_if_url(values):
    """
    Takes a list of values, determines if they other SWAPI endpoints
    """
    for val in values:
        if 'https://swapi.co/' not in val:
            return False
    return True