import click
import requests 
import json


"""
Make a way to specify options based on fields for the starships.
Make an order by flag to order them by parameters of the starships

"""

class Config(object):
    def __init__(self):
        self.base_url = "https://swapi.co/api"

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@pass_config
def cli(config):
    pass


starship_params = ["MGLT",
"cargo_capacity",
"consumables",
"cost_in_credits",
"created",
"crew",
"edited",
"hyperdrive_rating",
"length",
"manufacturer",
"max_atmosphering_speed",
"model",
"name",
"passengers",
"films",
"pilots",
"starship_class",
"url"]

def filter_json(json, return_params):
    if return_params:
        json = json['results']

        filtered_json = []
        for element in json:
            new_element = {}
            for key in element:
                if key in return_params:
                    new_element[key] = element[key]
            filtered_json.append(new_element)
                    
        return filtered_json
    return json

def get_all_starships(starship_base_url):
    result_json = requests.get(starship_base_url).json()

    return result_json

@cli.command()
@click.option('--list', is_flag=True, help="Returns a list of all starships with data")
@click.option('--search', '-s',
                help="Search by Name or Model of Starship")
@click.option('--return-params', '-rp', multiple=True, type=click.Choice(starship_params), help="Filter result parameters returned")
@pass_config
def starships(config, list, search, return_params):
    """Main command to get information about Starships. """
    starship_base_url = config.base_url + '/starships/'
    search_url = ''

    if list:
        final_json = get_all_starships(starship_base_url)
        if return_params:
            final_json = filter_json(final_json, return_params)
        click.echo(json.dumps(final_json, indent=4))
    else:
        if search:
            search_url = starship_base_url + '?search={}'.format(search)
            result_json = requests.get(search_url).json()
        
        else:
            search_url = starship_base_url
            result_json = requests.get(search_url).json()

        result_json = filter_json(result_json, return_params)



        click.echo(json.dumps(result_json, indent=4))

