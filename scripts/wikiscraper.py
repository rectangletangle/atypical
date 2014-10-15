
import concurrent.futures
import functools
import os

import requests
import bs4

from urllib.parse import urljoin

WIKI_URL = 'http://en.wikipedia.org/wiki/'

USER_AGENT = 'certainly-not-python'

def concurrent_get(urls, workers=10):
    with concurrent.futures.ThreadPoolExecutor(workers) as executor:
        yield from executor.map(functools.partial(requests.get, headers={'User-Agent': USER_AGENT}), urls)

def article_text(wikihtml):
    paragraphs = bs4.BeautifulSoup(wikihtml).find(id='content').find_all('p')
    return '\n'.join(paragraph.text for paragraph in paragraphs)

def wiki_scraper(articles):
    urls = (urljoin(WIKI_URL, article) for article in set(articles))

    htmls = (response.text for response in concurrent_get(urls)
             if str(response.status_code).startswith('2'))

    return '\n'.join(article_text(html) for html in htmls)

if __name__ == '__main__':
    articles = ['mammal',
                'reptile',
                'bird',
                'fish',
                'amphibian',
                'tunicate',
                'echinoderm',
                'chordate',
                'tardigrade',
                'aposematism',
                'insect',
                'crustacean',
                'arthropod',
                'tetrapod',
                'vertebrate']

    text = wiki_scraper(articles)

    pkg_root = os.path.dirname(os.path.dirname(__file__))
    output_filename = os.path.join(pkg_root, 'data', 'wikisample.txt')

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(text)

    print('wrote ~{count} words to {filename}'.format(count=len(text.split()), filename=output_filename))

