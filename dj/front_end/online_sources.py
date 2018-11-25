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
        return GS.search(self.query, pause=0.05)

class GoogleNews(Source):
    def __iter__(self):
        return GS.search_news(self.query, pause=0.05)
