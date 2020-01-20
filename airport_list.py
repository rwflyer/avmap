import json
import metar
from datetime import datetime

# Accepts a json configuration file in the form:
#
# {
#   "string1": [
#     { "KORD": {"offset": 0} },
#     { "KBFI": {"offset": 1} }
#   ]
# }
#
# Where the airport code must be the capitalized ICAO code, and the offset indicates the
# pixel index in the string of pixels attached to the SPI bus.
#
#
# The configuration is stored in-memory.
#
# The latest metars are also saved for reference.  The reference is used to determine when
# a given station is off the air for whatever reason.
#


config_file_path = 'airports.json'

configured_airports = None

metar_store = None

def read_airports():
    global configured_airports
    global metar_store
    
    with open(config_file_path) as config_file:
        json_text = config_file.read()
        json_config = json.loads(json_text)
        airports = json_config['string1']

    configured_airports = airports

    # Create the in-memory metar store, which is an easier to access schema vs. the easier-for-humans
    # format of the JSON configuration.
    metar_store = []
    for config_row in airports:
        # baroque python3 way to get first key, which will be only key
        airport_code = next(iter(config_row))
        offset = config_row[airport_code]['offset']
        metar_store.append({'icao_code': airport_code, 'metar': None, 'offset': offset})


def retrieve_metars():
    """
    Retrieves fresh metars for the airport list.  If a metar cannot be fetched,
    the entry is still present but the metar field is set to None.
    """
    global metar_store

    airport_code_list = [x['icao_code'] for x in metar_store]
    raw_metars = metar.fetch_metars(airport_code_list)

    fetched_at = datetime.utcnow()
    
    # Assign Metar objects for each retrieved observation, or None
    for airport_record in metar_store:
        code = airport_record['icao_code']
        if code in raw_metars:
            airport_record['metar'] = metar.Metar(code, raw_metars[code], fetched_at)
        else:
            airport_record['metar'] = None

if __name__ == '__main__':
    read_airports()
    retrieve_metars()
    
