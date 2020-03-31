"""The main program which runs the interactive search prototype.
"""
# standard library
import csv
import json
import time
# for opening the default pager with search results (Less)
import click
# https://python-prompt-toolkit.readthedocs.io/en/master/pages/getting_started.html
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion
from prompt_toolkit.completion import FuzzyCompleter

from elasticsearch import Elasticsearch


class CustomCompleter(Completer):
    """
    Auto-completion following the documentation for prompt_toolkit:
    https://python-prompt-toolkit.readthedocs.io/en/master/pages/asking_for_input.html#a-custom-completer
    """

    def get_completions(self, document, complete_event):

        # what's typed so far
        word = document.get_word_before_cursor()
        # on-the-fly search of elasticsearch to derive auto-complete suggestions
        result = es.search(index="games", body={"size" : 50, "query": {"prefix" : { "name" : word }}})
        if result:
            # could make this conditional on some score threshold (if hits['_score'] > thresh)
            # parse the ES result
            top = [hit['_source']['name'] for hit in result['hits']['hits']]
            for name in top:
                if name.startswith(word):
                    yield Completion(name, start_position=-len(word))
        else:
            yield Completion('completion', start_position=-len(word))


def load_data():
    """
    Add every game (row) from the csv database into the elasticsearch instance.
    """
    with open('games.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            es.index(index='games', doc_type='game', id=i, body=json.dumps(dict(row)))


def min_2_hr(mins):
    """
    Helper function for transforming playing time in minutes to and Hour+Min format.
    """
    return f'{mins//60}hr {mins%60}min'


def comp_level(num):
    """
    Helper function for translating complexity level out of five into a word rating.
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
    print('\nType a query and press enter. This will pop open a window displaying the results of your search. Press q to quit that window and return to the searchbar.\n')
    print('\nWhen you\'re done searching and ready to close the prototype, enter "exit" or "quit" as a search query to shut everything down.\n')

    zero_results_count = 0
    search_count = 0

    prompting = True
    while prompting:

        user_input = prompt("(searchbar) | ",
                            history=FileHistory('history.txt'),
                            auto_suggest=AutoSuggestFromHistory(),
                            completer=FuzzyCompleter(CustomCompleter()),
                            complete_in_thread=True)

        if user_input == '':  # when just pressing Enter
            continue  # don't open a pager with nothing in it or count it as a search

        if user_input in ['q', 'quit', 'x', 'exit']:
            prompting = False
            print(f'\nQuitting. Thanks!\n\n{zero_results_count}/{search_count} searches returned zero results.\n')
        else:
            search_count += 1

            # the actual searching within the search prototype
            result = es.search(index="games", body={"size" : 10, "query": {"multi_match" : { "query" : user_input, "fields": ["name^2", "designer"]}}})

            if result:
                # parse the ES response and accumulate into a giant string for output to less
                hits = [hit['_source'] for hit in result['hits']['hits']]
                num_results = f'\nDisplaying {len(hits)}/{len(hits)} results\n'
                results = f''
                for hit in hits:
                    results += f'\n{"-"*80}\n\n'
                    results += f'\n{hit["name"]} ({hit["version_published"]})\n'
                    results += f'\n\tCreated by {hit["designer"]}\n'

                    rated, players, pt, min, comp, votes = 'Rated:', 'Players:', 'Playing time:', 'Rec. minimum age:', 'Complexity:', 'Number of votes:'
                    results += f'\n\t|{rated:>20}\t {float(hit["avg_rating"]):.1f}/10.0'
                    results += f'\n\t|{players:>20}\t {hit["min_players"]}-{hit["max_players"]}'
                    results += f'\n\t|{pt:>20}\t~{min_2_hr(int(hit["playing_time"]))}'
                    results += f'\n\t|'
                    results += f'\n\t|{comp:>20}\t {comp_level(float(hit["complexity_out_of_5"]))} ({float(hit["complexity_out_of_5"]):.1f}/5.0)'
                    results += f'\n\t|{min:>20}\t {hit["recommended_min_age"]} years old'
                    results += f'\n\t|{votes:>20}\t {format(int(hit["num_votes"]), ",")}\n'

                    results += f'\n\tCategory: {hit["category"]}'
                    results += f'\n\tGame-play: {hit["mechanic"]}\n\n'

                click.echo_via_pager(num_results + results)  # mega f-string!

            if len(hits) < 1:
                # a "miss"
                zero_results_count += 1


if __name__ == '__main__':
    # To avoid error messages flooding the screen, wait for 45 seconds for
    # Elasticsearch to load before trying to connect to it
    time.sleep(45)
    es = Elasticsearch([{'host': 'esearch', 'port': 9200}])

    # load the csv data into ES
    load_data()
    # run the prototype
    searchbar()
