import json
import metar
from datetime import datetime

# Abstraction for a list of airports and the current METARs for those airports.
# The airports member contains a list of dictionaries, keyed as:
#
# {
#   "metar": <metar.Metar object>, or None if there is no observation available
#   "icao_code":  "KBFI", capitalized airport code. Use "K9V9" for three-digit US airports without a K prefix
#   "offset":  <int>, where to display the weather color on the LED string, measured from zero
# }
#
# At init time, reads a json configuration file named airports.json in the form:
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

config_file_path = 'airports.json'

#CONFIG_FILE = "./data/config.json"
#__working_dir__ = os.path.dirname(os.path.abspath(__file__))
#__full_config__ = os.path.join(__working_dir__, os.path.normpath(CONFIG_FILE))


colors = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'LOW': (255, 0, 255),
    'OFF': (0, 0, 0),
    'GRAY': (50, 50, 50),
    'YELLOW': (255, 255, 0),
    'DARK_YELLOW': (20, 20, 0),
    'WHITE': (255, 255, 255)
}

color_by_category = {
    metar.IFR: colors['RED'],
    metar.VFR: colors['GREEN'],
    metar.MVFR: colors['BLUE'],
    metar.LIFR: colors['LOW'],
    metar.SMOKE: colors['GRAY'],
    metar.INVALID: colors['OFF']
}
    
def color_for_category(cond):
    global color_by_category
    return color_by_category[cond]



class AirportList(object):
    def __init__(self):
        self.metar_store = None
        self.fetched_at = None
        
        with open(config_file_path) as config_file:
            json_text = config_file.read()
            json_config = json.loads(json_text)
            self.airports = json_config['string1']

        # Transform into the metar_store
        metars = []
        for config_row in self.airports:
            # baroque python3 way to get first key, which will be only key
            airport_code = next(iter(config_row))
            offset = config_row[airport_code]['offset']
            metars.append({'icao_code': airport_code, 'metar': None, 'offset': offset})
        
        self.metar_store = metars

    def airport_codes_list(self):
        return [x['icao_code'] for x in self.metar_store]
        
    def retrieve_metars(self):
        """
        Retrieves fresh metars for the airport list.  If a metar cannot be fetched,
        the entry is still present but the metar field is set to None.
        """
        raw_metars = metar.fetch_metars(self.airport_codes_list())

        self.fetched_at = datetime.utcnow()
    
        # Assign Metar objects for each retrieved observation, or None
        for airport_record in self.metar_store:
            code = airport_record['icao_code']
            if code in raw_metars:
                airport_record['metar'] = metar.Metar(code, raw_metars[code], self.fetched_at)
            else:
                airport_record['metar'] = None

    def render_metars(self, led_string):
        global colors
        global color_for_category
        
        for obs in self.metar_store:
            metar = obs['metar']
            if metar is not None:
                color = color_for_category(metar.category())
            else:
                color = colors['OFF']

        led_string.set_pixel(obs['offset'], color)
        print('{}: {} {}'.format(obs['icao_code'], metar.category(), color))
