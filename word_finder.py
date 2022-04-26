from gettext import find
import urllib
import requests


def find_word_frequency(word):
    words = word.split()
    words = [w for w in words if len(w)>2]
    if len(words) == 0:
        return 0
    cnt = 0
    for word in words:
        encoded_query = urllib.parse.quote(word)
        params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 1}
        params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

        response = requests.get('https://api.phrasefinder.io/search?' + params)

        assert response.status_code == 200

        # print(response.json())

        if response.json()['phrases']:
            cnt += response.json()['phrases'][0]['mc']
    return cnt / len(words)

# print(find_word_frequency("Hypertension"))