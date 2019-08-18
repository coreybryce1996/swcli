import click
import json

from request_helper import get_request, detect_if_url

def print_json(result_json):
    """
    Pretty prints all JSON given. 
    If JSON is empty, leave message for user.
    """

    if (result_json):
        for element in result_json:
            json_str = json.dumps(element, indent=4)
            click.echo(json_str)
    else:
        click.echo("No starships found with given criteria. Try again!")



def clean_value(value, key):
    """
    Specific to Starships.
    Both films and pilots parameters of the Starship responses will be a list of endpoints.
    If the system has not cached those values, this will replace the endpoints with actual values.
    Returns the title of films, and the name of pilots.
    """
    values = []

    if key in ["films", "pilots"] and detect_if_url(value):
        for val in value:
            if key == "films":
                values.append(get_request(val)['title'])
            if key == "pilots":
                values.append(get_request(val)['name'])
        return values
    else:
        return value

def clean_json(json, return_params):
    """
    Creates a new JSON based on the return parameters specified by user.
    If no return parameters specified, still runs through to clean any URL values,
        converts URLs to their respective values with clean_value() function.
    """
    cleaned_json = []
    for element in json:
        new_element = {}
        for key in element:
            if (return_params is None) or (key in return_params):
                value = element[key]
                new_element[key] = clean_value(value, key)

        cleaned_json.append(new_element)

    return cleaned_json

def filter_json(json, param, param_range):
    """
    Filters any elements out of JSON who's parameters are not within range specified. 
    """
    filtered_json = []

    for element in json:
        if element[param]:
            try:
                value = int(element[param])
                if param_range[0] <= value <= param_range[1]:
                    filtered_json.append(element)
            except:
                pass


    return filtered_json