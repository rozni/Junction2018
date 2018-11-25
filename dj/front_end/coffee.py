import itertools

from .entities import *
from .online_sources import *

# def search(query, limit_tags=50, limit_links=10):
#     return [dict(name='one', urls=['sth']), dict(name='two', urls=['A', 'B'])]

def search_sources(
        query,
        sources=[
            GoogleSearch,
            GoogleNews,
        ],
        limit=10
):

    results = ResultAcumulator()
    for source in sources:
        for url in itertools.islice(source(query), limit):
            results.process_url(url)

    return results


def order_results(results, min_urls):

    descending = sorted(results.entities, key=lambda ent: results.entities[ent].num_urls, reverse=True)

    extracted = (results.entities[entity] for entity in descending)
    filtered = [
        entity for entity in extracted
        if entity.num_urls > min_urls
    ]

    cves = (entity for entity in filtered if entity.type == 'CVE')
    other = (entity for entity in filtered if entity.type != 'CVE')

    return itertools.chain(cves, other)

def search(
        query,
        max_result_limit=50,
        min_result_urls=3,
        max_urls_per_source=10
):
    results = search_sources(query=query, limit=max_urls_per_source)
    return order_results(results=results, min_urls=min_result_urls)


def reverse_entities(results, min_urls):
    url_to_tags = dict()
    descending = sorted(results.entities, key=lambda ent: results.entities[ent].num_urls, reverse=True)

    extracted = (results.entities[entity] for entity in descending)
    filtered = [
        entity for entity in extracted
        if entity.num_urls > min_urls
    ]

    for entity in filtered:
        for url in entity.urls:
            url_to_tags.setdefault(url, set()).add(entity.name)

    for url in url_to_tags:
        url_to_tags[url] = sorted(url_to_tags[url])

    return url_to_tags

def search2(
        query,
        max_result_limit=50,
        min_result_urls=3,
        max_urls_per_source=10
):
    results = search_sources(query=query, limit=max_urls_per_source)
    return reverse_entities(results, min_urls=min_result_urls)
