# Configurations attached to the corpus building script
#
# Created at 4 March 2025.
#

from pathlib import Path
from datetime import datetime
from collections import namedtuple


# general
DATA_FOLDER = Path() / 'data'
RESULT_FOLDER = Path() / 'result'

Router = namedtuple('Router', ['source', 'path'])

# ipcc data routers
ipccdata_term_defined = Router('ipcc', DATA_FOLDER / 'ipcc-terms-raw-defined.txt')
ipccdata_term_listing = Router('ipcc', DATA_FOLDER / 'ipcc-terms-raw-listing.txt')
ipccdata_statement = Router('ipcc', DATA_FOLDER / 'ipcc-statement-climatex.tsv')
ipccdata_acronym = Router('ipcc', DATA_FOLDER / 'ipcc-acronyms-raw.csv')


# general config
def get_timestamp(fmt: str = '%m%d%H%M%S'):
    """Generalised timestamp"""
    return datetime.now().strftime(fmt)
