from functools import reduce
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from JanusWikiTables.exceptions import NoTableFoundException, HTTPStatusError


def _get_tables(url: str) -> List[pd.DataFrame]:
    """Get all wikitables on page and convert them to dataframes.
    :param url: page url
    :return: list of dataframes representing tables
    :raises NoTableFoundException: when no wikitables found on page
    :raises HTTPStatusError: when request was unsuccessful
    """
    request = requests.get(url)
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        tables = soup.findAll("table", {"class": "wikitable"})
        if len(tables) == 0:
            raise NoTableFoundException()
        for sup in soup.find_all('sup'):
            sup.replaceWith('')  # remove footnotes
        dfs = []
        for table in tables:
            df = pd.read_html(table.prettify(), flavor="html5lib", header=0)[0]
            # df.columns = df.iloc[0] # manually set headers instead of header = 0
            dfs.append(df)
        return dfs
    else:
        raise HTTPStatusError(request.status_code)


def _merge_tables(tables: List[pd.DataFrame]) -> pd.DataFrame:
    """Merge tables.
    :param tables: list of tables as dataframes
    :return: merged table
    """
    left = tables.pop(0)[:-1]  # don't use last row as it contains headers
    for table in tables:
        right = table[:-1]
        lheaders = left.columns.tolist()
        rheaders = right.columns.tolist()
        headers = list(set(lheaders).intersection(rheaders))
        if len(lheaders) == len(rheaders) == len(headers):
            left = pd.concat([left, right])
        elif len(headers) == 1:
            # :TODO: case insensitive
            left = pd.merge(left, right, how='outer')
        else:
            raise NotImplementedError  # :TODO: what if header intersection results in multiple columns?
    return left


def get_table_html(url: str) -> 'html':
    """Convert merged tables to html.
    :param url: page url
    :return: html code as string
    """
    dfs = _get_tables(url)
    merged_table = _merge_tables(dfs)
    return merged_table.to_html(classes='display compact" id = "merged_table')  # double quote to close pandas' class

