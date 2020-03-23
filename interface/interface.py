"""
1. ES running (depends on)
2. Instantiate the wrapper and connect to running server
3. Load data from file into ES
4. Start the searchbar
"""
import json
import requests
from pprint import pprint
import sys

import click
import pandas as pd
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion, WordCompleter, FuzzyCompleter

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# TODO: maybe asynchronous
# text = prompt('> ', completer=MyCustomCompleter(), complete_in_thread=True)


class CustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        result = es.search(index="games_df", body={"size" : 50, "query": {"prefix" : { "name" : word }}})
        if result:
            # could make this conditional on some score threshold (if hits['_score'] > thresh)
            top = [hit['_source']['name'] for hit in result['hits']['hits']]
            for name in top:
                if name.startswith(word):
                    yield Completion(name, start_position=-len(word))
        else:
            yield Completion('completion', start_position=-len(word))


def rec_to_actions(df):
    """
    https://stackoverflow.com/questions/49726229/how-to-export-pandas-data-to-elasticsearch
    Helper for bulk loading
    """
    for record in df.to_dict(orient="records"):
        yield ('{ "index" : { "_index" : "games_df", "_type" : "game" }}')
        yield (json.dumps(record))


def load_data():
    """
    """
    df = pd.read_csv('games.csv')
    r = es.bulk(rec_to_actions(df))
    if r["errors"]:
        print(f'\nError loading data into elasticsearch.\n')
        sys.exit(1)


def searchbar():
    """
    """

    print('\nWelcome! This is a simulation of a search bar for our app.\n')

    prompting = True
    while prompting:

        user_input = prompt("(searchbar) | ", completer=FuzzyCompleter(CustomCompleter()))
        # user_input = prompt("(searchbar) | ", completer=CustomCompleter())

        if user_input in ['q', 'quit', 'x', 'exit']:
            prompting = False
            print('\nQuitting. Thanks!\n')
        else:
            # TODO: make actual results from es and format them very nicely
            header = f'search:\t{user_input}\n{"-"*80}\n\nThese are the results for your search\n\n'
            # this, this, that = es., es., es.
            # result = f''
            click.echo_via_pager(header)


if __name__ == '__main__':
    # load_data()
    # result = es.search(index="games_df", body={"query": {"prefix" : { "name" : "orl" }}})
    # result = es.search(index="games_df", body={"size" : 50, "query": {"match_all" : {}}})
    # top = [hit['_source']['name'] for hit in result['hits']['hits']]
    # pprint(top)
    # print(len(top))
    # result = es.search(index="games_df", body={"query": {"prefix" : { "name" : "orl" }}})
    # pprint(result)
    searchbar()
