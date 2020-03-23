import json
import requests
from pprint import pprint

import click
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
        result = es.search(index="sw", body={"query": {"prefix" : { "name" : word }}})
        if result:
            # could make this conditional on some score threshold (if hits['_score'] > thresh)
            top = [hit['_source']['name'] for hit in result['hits']['hits']]
            for name in top:
                if name.startswith(word):
                    yield Completion(name, start_position=-len(word))
        else:
            yield Completion('completion', start_position=-len(word))


def main():
    """
    """

    print('\nWelcome! This is a simulation of a search bar for our app.\n')

    prompting = True
    while prompting:

        user_input = prompt("(searchbar) | ", completer=FuzzyCompleter(CustomCompleter()))

        if user_input in ['q', 'quit', 'x', 'exit']:
            prompting = False
            print('\nQuitting. Thanks!\n')
        else:
            result = f'search:\t{user_input}\n{"-"*80}\n\nThese are the results for your search\n\n'
            click.echo_via_pager(result)


if __name__ == '__main__':
    main()
