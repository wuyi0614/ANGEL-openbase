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


def get_ipcc_terms_defined(route: Router, save: bool = True, encoding: str = 'utf8'):
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
    rows.columns = ['entityid', 'entity', 'description']
    if save:
        di = folder / f'ipcc-terms-ready-{get_timestamp(fmt)}.csv'
        rows.to_csv(di, index=False, encoding=encoding)

    return rows


def get_ipcc_acronyms(route: Router, save: bool = True, encoding: str = 'utf8'):
    """Load IPCC acronyms from a router file"""
    d = pd.read_csv(route.path, encoding=encoding)
    d = d.loc[d.entity != 'abb']

    # filter by duplicates and blanks
    # TODO: acronyms should be collected by chapters and working groups
    counts = d['entity'].value_counts()
    dup_ids = counts[counts > 1].index
    dedup_ids = d.loc[d.entity.isin(dup_ids), 'entity'].drop_duplicates().index
    pnl = pd.concat([d.loc[~d.entity.isin(dup_ids)], d.loc[dedup_ids]],
                    axis=0, ignore_index=True)
    pnl.reset_index(drop=False, inplace=True)
    pnl.columns = ['entityid', 'entity', 'description']
    if save:
        di = folder / f'ipcc-acronyms-{get_timestamp(fmt)}.csv'
        pnl.to_csv(di, index=False, encoding=encoding)

    return pnl


def get_ipcc_statement(route: Router, save: bool = True, encoding: str = 'utf8'):
    """Load scientific statements of IPCC in dataframe with a proper encoding"""
    d = pd.read_csv(route.path, sep='\t', encoding=encoding)
    pnl = d[['statement_idx', 'report', 'page_num', 'statement', 'confidence']]
    pnl.columns = ['statementid', 'group', 'page', 'statement', 'confidence']
    if save:
        di = folder / f'ipcc-statement-{get_timestamp(fmt)}.csv'
        pnl.to_csv(di, index=False, encoding=encoding)

    return pnl


if __name__ == "__main__":
    terms = get_ipcc_terms_defined(ipccdata_term_defined)
    stmts = get_ipcc_statement(ipccdata_statement, encoding='utf8')
    acron = get_ipcc_acronyms(ipccdata_acronym)
