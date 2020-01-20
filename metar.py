
import re
import urllib.request
from datetime import datetime


INVALID = 'INVALID'
INOP = 'INOP'
VFR = 'VFR'
MVFR = 'M' + VFR
IFR = 'IFR'
LIFR = 'L' + IFR
#NIGHT = 'NIGHT'
SMOKE = 'SMOKE'


def extract_metar_from_html_line(raw_metar_line):
    """
    Takes a raw line of HTML from the METAR report and extracts the METAR from it.
    NOTE: A "$" at the end of the line indicates a "maintainence check" and is part of the report.
    Arguments:
        metar {string} -- The raw HTML line that may include BReaks and other HTML elements.
    Returns:
        string -- The extracted METAR.
    """
    metar = re.sub('<[^<]+?>', '', raw_metar_line)
    metar = metar.replace('\n', '')
    metar = metar.strip()

    return metar


def get_metar_from_report_line(metar_report_line_from_webpage):
    """
    Extracts the METAR from the line in the webpage and sets
    the data into the cache.
    Returns None if an error occurs or nothing can be found.
    Arguments:
        metar_report_line_from_webpage {string} -- The line that contains the METAR from the web report.
    Returns:
        string,string -- The identifier and extracted METAR (if any), or None
    """

    identifier = None
    metar = None

    try:
        metar = extract_metar_from_html_line(metar_report_line_from_webpage)
        
        if len(metar) < 1:
            return (None, None)

        identifier = metar.split(' ')[0]

    except:
        metar = None

    return (identifier, metar)

def fetch_metars(airport_iaco_codes):
    """
    Calls to the web an attempts to gets the METARs for the requested station list.
    Arguments:
        airport_iaco_codes {string[]} -- Array of stations to get METARs for.
    Returns:
        dictionary -- Returns a map of METARs keyed by the station code.
    """
    metars = {}
    metar_list = "%20".join(airport_iaco_codes)
    request_url = 'https://www.aviationweather.gov/metar/data?ids={}&format=raw&hours=0&taf=off&layout=off&date=0'.format(
        metar_list)
    stream = urllib.request.urlopen(request_url, timeout=2)
    data_found = False
    stream_lines = stream.readlines()
    stream.close()

    for line in stream_lines:
        line_as_string = line.decode("utf-8")
        if '<!-- Data starts here -->' in line_as_string:
            data_found = True
            continue
        elif '<!-- Data ends here -->' in line_as_string:
            break
        elif data_found:
            identifier, metar = get_metar_from_report_line(line_as_string)

            if identifier is None:
                continue

            # If we get a good report, go ahead and shove it into the results.
            if metar is not None:
                metars[identifier] = metar

    return metars



class Metar(object):
    def __init__(self, icao_code, initial_raw_metar = '', fetched_at = None):
        self.icao_airport_code = icao_code
        self.raw_metar = initial_raw_metar
        self.fetched_datetime = fetched_at

    def fetch(self):
        metars = fetch_metars([self.icao_airport_code])
        if self.icao_airport_code in metars:
            self.raw_metar = metars[self.icao_airport_code]
            self.fetched_datetime = datetime.utcnow()
            return True
        else:
            self.raw_metar = ''
            self.fetched_datetime = None
            return False
        
    def ceiling(self):
        """
        Returns the height that clouds are above the ground, in feet
        """

        # Exclude the remarks from being parsed as the current
        # condition as they normally are for events that
        # are in the past.
        components = self.raw_metar.split('RMK')[0].split(' ')
        minimum_ceiling = 10000
        for component in components:
            if 'BKN' in component or 'OVC' in component:
                try:
                    ceiling = int(''.join(filter(str.isdigit, component))) * 100
                    if ceiling < minimum_ceiling:
                        minimum_ceiling = ceiling
                except Exception as ex:
                    # Unable to decode ceiling
                    return INVALID

        return minimum_ceiling

    def ceiling_category(self):
        """
        Returns the flight rules classification based on the cloud ceiling.
        Returns: string -- The flight rules classification.
        """

        c = self.ceiling()
        
        if c < 500:
            return LIFR
        if c < 1000:
            return IFR
        if c < 3000:
            return MVFR
        return VFR
    
    def visibility(self):
        """
        Returns the flight rules classification based on visibility from a RAW metar.
        Returns: string -- The flight rules classification, or INVALID in case of an error.
        """

        match = re.search('( [0-9] )?([0-9]/?[0-9]?SM)', self.raw_metar)
        is_smoke = re.search('.* FU .*', self.raw_metar) is not None
        # Not returning a visibility indicates UNLIMITED
        if(match == None):
            return VFR
        (g1, g2) = match.groups()
        if g2 is None:
            return INVALID
        if g1 != None:
            if is_smoke:
                return SMOKE
            return IFR
        if '/' in g2:
            if is_smoke:
                return SMOKE
            return LIFR
        vis = int(re.sub('SM', '', g2))
        if vis < 3:
            if is_smoke:
                return SMOKE
            return IFR
        if vis <= 5:
            if is_smoke:
                return SMOKE

            return MVFR
        return VFR


    def category(self):
        """
        Returns the flight rules classification based on the entire RAW metar.
        Arguments:
        Returns: string -- The flight rules classification, or INVALID in case of an error.
        """
        vis = self.visibility()
        ceiling_cat = self.ceiling_category()
        if ceiling_cat == INVALID or vis == INVALID:
            return INVALID
        if vis == SMOKE:
            return SMOKE
        if vis == LIFR or ceiling_cat == LIFR:
            return LIFR
        if vis == IFR or ceiling_cat == IFR:
            return IFR
        if vis == MVFR or ceiling_cat == MVFR:
            return MVFR

        return VFR


if __name__ == '__main__':
    m = Metar('KRNT')
    m.fetch()
    print('{}: {} {}'.format(m.icao_airport_code, m.category(), m.raw_metar))
