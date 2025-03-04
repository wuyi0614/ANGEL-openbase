# Replicable script for getting corpus ready for openbase project
#
# Created at 4 March 2025.
#

import pandas as pd

from bs4 import BeautifulSoup
from corpus.config import *


# top conf
fmt = '%m%d'
folder = Path('corpus') / RESULT_FOLDER.name


def get_ipcc_terms_defined(route: Router, save: bool=True):
    """Extract IPCC terms from a router file"""
    foo = route.path.read_text('utf-8')
    soup = BeautifulSoup(foo, 'lxml')

    key = soup.find_all(name='span', attrs={'class': 'gloss-term-all gloss-term'})
    desc = soup.find_all(name='span', attrs={'class': 'gloss-term-all gloss-definition'})
    rows = []
    for k, d in zip(key, desc):
        rows += [[k.get_text().strip(), d.get_text().strip()]]

    rows = pd.DataFrame(rows, columns=['entity', 'description'])
    rows.reset_index(drop=False, inplace=True)
    rows.columns = ['enetityid', 'entity', 'description']
    if save:
        di = folder / f'ipcc-terms-ready-{get_timestamp(fmt)}.csv'
        rows.to_csv(di, index=False)

    return rows


if __name__ == "__main__":
    terms = get_ipcc_terms_defined(ipccdata_term_defined)
