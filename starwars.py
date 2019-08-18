import click
import requests 
import json
import sys
import os

from json_helper import print_json, clean_json, filter_json, clean_value
from request_helper import get_request


starship_params = ["MGLT", "cargo_capacity", "consumables", "cost_in_credits", "created",
                    "crew", "edited", "hyperdrive_rating", "length", "manufacturer", "max_atmosphering_speed",
                    "model", "name", "passengers", "films", "pilots", "starship_class", "url"]
filterable_starship_params = ["cost_in_credits", "length", "crew", "passengers", "cargo_capacity"]
cache_file = "all_starships_json.txt"

class Config(object):
    def __init__(self):
        self.base_url = "https://swapi.co/api"

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@pass_config
def cli(config):
    pass

def get_filter_param_info(filter_params):
    """ Tries to parse text given for filtering by a parameter.
    Gives message if formatting is wrong, or if non-integers are used, and exits.
    returns the parameter to filter by, and the range if successful. 
    """

    try:
        filter_params = filter_params.split(' ')
        param = filter_params[0]
        param_range = filter_params[1].split(':')
    except:
        click.echo("Please correct filter parameter (-fp) format (-fp 'crew 0:5')")
        sys.exit(1)
    if param in filterable_starship_params:
        try:
            param_range = list(map(float, param_range))
        except:
            click.echo("Please use integers for parameter filtering (-fp)")
            sys.exit(1)

        return param, param_range
    else:
        click.echo("Parameter is unavailable for filtering in this version.")
        sys.exit(1)

def handle_list(starship_base_url, filter_params, return_params, use_cached):
    """ Function to handle if the user wants all starship data. 
        Will use cached data if available (Decreased runtime by ~10 seconds)
        If filtered parameters are given, results in the range will be returned.
        Prints prettified JSON.
    """

    if use_cached:
        with open(cache_file) as infile:
            return_json = json.load(infile) # Cached info contains ALL starship data, with names of films and people involved
    else:
        return_json = get_request(starship_base_url)['results']
        return_json = clean_json(return_json, None)
        with open(cache_file, 'w') as outfile:
            json.dump(return_json, outfile)

    if filter_params:
        param, param_range = get_filter_param_info(filter_params)

        """ If filtering by a parameter, make sure that parameter is returned. """
        if param not in return_params:
            return_params = list(return_params)
            return_params.append(param) 
            return_params = tuple(return_params)

        return_json = filter_json(return_json, param, param_range)

    final_json = clean_json(return_json, return_params)

    print_json(final_json)

def handle_search(starship_base_url, searchParam, return_params):
    """ Function to handle if the user wants to search by Name or Model of Starship
        Creates a search url based on search parameter, gets and cleans json from SWAPI.io
        Prints prettified JSON.
     """

    search_url = starship_base_url + '?search={}'.format(searchParam)
    return_json = get_request(search_url)['results']
    final_json = clean_json(return_json, return_params)

    print_json(final_json)


@cli.command()
@click.option('--list', '-l', is_flag=True, help="Returns a list of all starships with data")
@click.option('--filter-params', '-fp', help="Filter for parameters to be used with --list (Only supports integers). Ex. 'passengers 0:10'")
@click.option('--search', '-s',
                help="Search by Name or Model of Starship")
@click.option('--return-params', '-rp', multiple=True, type=click.Choice(starship_params), help="Specify result parameters returned for each Starship")
@pass_config
def starships(config, list, filter_params, search, return_params):
    """Main command to get information about Starships.
    --list to get all starships, but may filter based on one parameter with a range of integers (-fp).
    --search to search directly by Name or Model. 
    --rp to specify what parameters user would like returned for each Starship. 
     """

    
    starship_base_url = config.base_url + '/starships/'

    if list:
        """ If cache file is in directory, set flag to use it. """
        use_cached = os.path.exists(cache_file)
        handle_list(starship_base_url, filter_params, return_params, use_cached)

    elif search:
        handle_search(starship_base_url, search, return_params)

