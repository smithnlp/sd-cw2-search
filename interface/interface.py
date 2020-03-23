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


def min_2_hr(mins):
    """
    Helper function for playing time
    """
    return f'{mins//60}hr {mins%60}min'


def comp_level(num):
    """
    Helper for complexity level out of five.
    """
    if num < 2.25:
        return "Low"
    elif num < 3.75:
        return "Medium"
    else:
        return "High"


def searchbar():
    """
    """

    print('\nWelcome! This is a simulation of a search bar for our app.\n')

    zero_results_count = 0
    search_count = 0

    prompting = True
    while prompting:

        user_input = prompt("(searchbar) | ",
                            history=FileHistory('history.txt'),
                            auto_suggest=AutoSuggestFromHistory(),
                            completer=FuzzyCompleter(CustomCompleter()),
                            complete_in_thread=True)

        if user_input == '':  # when just entering
            continue  # don't open a pager with nothing in it

        if user_input in ['q', 'quit', 'x', 'exit']:
            prompting = False
            print(f'\nQuitting. Thanks!\n\n{zero_results_count}/{search_count} searches returned zero results.\n')
        else:
            search_count += 1
            result = es.search(index="games_df", body={"size" : 10, "query": {"multi_match" : { "query" : user_input, "fields": ["name^2", "designer"]}}})
            if result:
                hits = [hit['_source'] for hit in result['hits']['hits']]
                num_results = f'\nDisplaying {len(hits)}/{len(hits)} results\n'
                results = f''
                for hit in hits:
                    results += f'\n{"-"*80}\n\n'
                    results += f'\n{hit["name"]} ({hit["version_published"]})\n'
                    results += f'\n\tCreated by {hit["designer"]}\n'

                    rated, players, pt, min, comp, votes = 'Rated:', 'Players:', 'Playing time:', 'Rec. minimum age:', 'Complexity:', 'Number of votes:'
                    results += f'\n\t|{rated:>20}\t {hit["avg_rating"]:.1f}/10.0'
                    results += f'\n\t|{players:>20}\t {hit["min_players"]}-{hit["max_players"]}'
                    results += f'\n\t|{pt:>20}\t~{min_2_hr(hit["playing_time"])}'
                    results += f'\n\t|'
                    results += f'\n\t|{comp:>20}\t {comp_level(hit["complexity_out_of_5"])} ({hit["complexity_out_of_5"]:.1f}/5.0)'
                    results += f'\n\t|{min:>20}\t {hit["recommended_min_age"]} years old'
                    results += f'\n\t|{votes:>20}\t {format(hit["num_votes"], ",")}\n'

                    results += f'\n\tCategory: {hit["category"]}'
                    results += f'\n\tGame-play: {hit["mechanic"]}\n\n'

                click.echo_via_pager(num_results + results)  # mega f-string!
            if len(hits) < 1:
                zero_results_count += 1


if __name__ == '__main__':
    # load_data()
    searchbar()
