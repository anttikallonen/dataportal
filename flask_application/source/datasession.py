__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

class DataSession(object):
    """Data session for fetching data from source"""

    def __init__(self, session, logger):
        self.session = session
        self.logger = logger

    def get_data_json(self, dataurl):
        self.logger.debug("Fetching JSON data from url ({0})".format(dataurl))
        response = self.session.get(dataurl)
        response.raise_for_status()
        return response.json()
