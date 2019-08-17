# swcli - A Python3 Project _Written in a galaxy far... far away_
Star Wars ClI Project - Bryce Corey

# Install Instructions
## If not installed already
- Install pip
- run `$pip install virtualenv`

## Commands to get project up and running
`$ cd swcli`
`$ virtualenv venv` (May take a minute)
`$ venv\scripts\activate`
`$ pip install --editable .`


# Options
### List
`--list` or `-l` will return a list of all starships

### Search
`--search` or `-s` will search for starships containing the string provided

### Filtering
`-rf` Filters data by a given parameter as long as it is of type 'int'.
Special formatting is required - `-rf "{parameter-name} {low}:{high}"`

### Customized Returning
`-rp {parameter-name}` Returns a list of starships only containing that/those parameter name(s) provided.

# Example Commands

`$ starwars starships -s falcon` (Searches for name/model that contains 'falcon')
`$ starwars starships -s falcon -rp name` (Searches for name/model that contains 'falcon', and returns only the Name)
`$ starwars starships -l` (Returns a list of all starships)
`$ starwars starships -l -rp name -rp model -rp films` (Returns list of all starships, but only containing the Name, Model and Films))
`$ starwars starships -l -fp "crew 1:5"` (Returns all starships that have room for a crew size 1 to 5)



