from gettext import find
import urllib
import requests


def find_word_frequency(word):
    encoded_query = urllib.parse.quote(word)
    params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 1}
    params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

    response = requests.get('https://api.phrasefinder.io/search?' + params)

    assert response.status_code == 200

    # print(response.json())

    if response.json()['phrases']:
        return response.json()['phrases'][0]['mc']
    return -1

# print(find_word_frequency("songs"))