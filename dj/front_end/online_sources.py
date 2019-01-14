import googlesearch as GS

__all__ = ['GoogleSearch', 'GoogleNews']

class Source:

    def __init__(self, query):
        self.query = query

    def __iter__(self) -> 'url':
        """Iterates links from this source based on the querry"""
        raise NotImplementedError()

class GoogleSearch(Source):
    def __iter__(self):
        return (url for url in GS.search(self.query, pause=0.5) if not url.endswith('pdf'))

class GoogleNews(Source):
    def __iter__(self):
        return (url for url in GS.search_news(self.query, pause=0.5) if not url.endswith('pdf'))
